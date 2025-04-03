# from django.shortcuts import render
# from store.models import PCategory, Product

# def home(request):

#     products = Product.objects.all().filter(is_available=True)
#     context = {
#         'products': products,
#     }

#     return render(request, 'home.html', context)
from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
    products = Product.objects.filter(is_available=True).order_by('created_date')

    # Get reviews for all products
    reviews_dict = {product.id: ReviewRating.objects.filter(product_id=product.id, status=True) for product in products}

    context = {
        'products': products,
        'reviews': reviews_dict,
    }
    return render(request, 'home.html', context)
