from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView

from .models import UserProfile, Feedback
from .forms import UserProfileForm, FeedbackForm

from checkout.models import Order


def user(request):
    """ Display the user's profile. """
    user = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=user)
    orders = user.orders.all()

    template = 'users/user.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


class FeedbackView(ListView):
    model = Feedback
    template_name = 'users/user_feedback.html'


class SubmitFeedback(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "users/add_feedback.html"
