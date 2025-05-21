from django.shortcuts import redirect, render
from django.http import  HttpResponse, jsonResponse
from .forms  import OrderForm
from .models import CartItem
import json
from datetime import date
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader render_to_string


def place_order(request, total=0, quantity=0):

    current_user = request.user
    #if the cart count is less than or equal to 0 redirect to the user
    cart_item = cart_items.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total  += (cart_item.product.price * cart_item.quantity)
        quantity = 


    


