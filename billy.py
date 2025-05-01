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


    #if the cart count is less than or equal to 0 then redirect back to the store
    cart_items = CartItem.objects.filter(user=current_date)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    else:
        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_count.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/ 100
        grand_total = total + tax

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                data = Order() #instance
                data.user = current_user
                data.first_name = form.cleaned_data['first_name'],
                data.last_name = form.cleaned_data['last_name'],
                data.phone = form.cleaned_data['phone'],
                data.email = form.cleaned_data['email'],
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.order_note = form.cleaned_data['order_note']
                data.order_total = grand_total
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR') #TO GET THE CURRENT IP
                data.save()

               # generate order number
                current_date = date.today().strftime('%Y%m%d')  # e.g. 20250422
                order_number = current_date + str(data.id)      # e.g. 20250422105
                data.order_number = order_number
                data.save()

                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total
                }
                return render(request, 'orders/payments.html', context)



                class payments(request):
                    body = json.loads(request.body)
                    order = Order.objects.get(user=current_user, is_ordered=False, order_number=body['orderID'])

                    #store transaction detail inside payment model
                    payment = Payment(
                        user = request.user,
                        payment_id = body['payment_method'],
                        #in order to get the amount paid is inside the order model, you
                        #should make a query
                        amount_paid = order.order_total,
                        status = body['status'],
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()
                    #move the cart items to order product table
                    cart_items = cart_items.objects.filter(user=request.user)
                    for item in cart_items:
                        orderproduct=OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.order_id = 


                

