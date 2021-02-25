from django.shortcuts import render
from .models import Train
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import TrainForm

def home(request):
    trains = Train.objects.all()
    paginator = Paginator(trains, 5)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'object_list': trains, })

class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy("train:home")
    success_message = 'City successfully create'

class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object'
    template_name = 'trains/detail.html'

class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy("train:home")
    success_message = 'Train successfully update'


class TrainDeleteView(SuccessMessageMixin, DeleteView):
    model = Train
    success_url = reverse_lazy("train:home")

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Train successfuly deleted')
        return self.post(self, request, *args, **kwargs)