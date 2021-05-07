from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your shopping basket at the moment!")
        return redirect(reverse, ('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IoPygIf8Aq7ELWBW9NKtqBl6DQgNEwgJ9Y7cOSG2wfawwmGQVqnhKHxxG4rQV46SPculD75PIjJHpWF14YZdgbx00v2JuOrGf',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
