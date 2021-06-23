from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages


from core.users.models import CustomUser


from core.users.forms import RegisterForm

# Create your views here.


class UserCreateView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_user = form.save()
        messages.success(self.request, 'Account Created successfully')

        return super().form_valid(form)
