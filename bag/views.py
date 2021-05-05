from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """A view to render the Shopping Bag contents"""

    return render(request, 'bag/bag.html')

# Add Products to the Shopping Basket


def add_to_bag(request, item_id):
    """ Add a quantity of the required product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'We have updated quantity of size {size.upper()} {product.name} to {bag[item_id]["items_by_size"][size]} in your basket')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'We have added size {size.upper()} {product.name} to your basket')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'We have added size {size.upper()} {product.name} to your basket')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated quantity of {product.name} to {bag[item_id]} in your basket')
        else:
            bag[item_id] = quantity
            messages.success(request, f'We have added {product.name} to your basket')

    request.session['bag'] = bag
    return redirect(redirect_url)


# Change the Product in the Shopping basket


def adjust_bag(request, item_id):
    """ Adjusts the quantity of the product in the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'We have updated quantity of size {size.upper()} {product.name} in your basket, to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'We have removed size {size.upper()} {product.name} from your basket')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated quantity of {product.name}  in your basket, to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'We have removed {product.name} from your basket')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


# Removes Items from the SHopping basket


def remove_from_bag(request, item_id):
    """ Removes item from the shopping bag """
    
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'We have removed size {size.upper()} {product.name} from your basket')
        else:
            bag.pop(item_id)
            messages.success(request, f'We have removed {product.name} from your basket')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)