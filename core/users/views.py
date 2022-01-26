from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from core.cart.models import Order

from django_email_verification import send_email


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

        returnVal = super(UserCreateView, self).form_valid(form)

        send_email(new_user)

        return returnVal


class OrderListView(ListView):
    model = Order
    template_name = 'users/my_purchases.html'

    def get_queryset(self):
        return Order.objects.filter(ordered=True)
