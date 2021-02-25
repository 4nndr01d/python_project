from django.shortcuts import render
from django.contrib import messages
from trains.models import Train
from .forms import *

def dfs_path(graph, start, goal):

    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_] ))

def get_graph():
    query = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in query)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp

    return graph


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})

def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
        #    assert False
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            traveling_time = data['travel_time']
            graph = get_graph()
            all_ways = list(dfs_path(graph, from_city.id, to_city.id))
            if not len(all_ways):
                messages.error(request, 'Routes not found.')
                return render(request, 'routes/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(request, 'Route across that cities not exist')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            for route in right_ways:
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route)-1):
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index+1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= traveling_time:
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Travel time longer than specified')
                return render(request, 'routes/home.html',  {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                routes.append({'routes': tr['trains'],
                               'total_time': tr['total_time'],
                               'from_sity': from_city.name,
                               'to_city': to_city.name})
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            context = {}
            form = RouteForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities

            return render(request, 'routes/home.html',context)


        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Route list is empty')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})
