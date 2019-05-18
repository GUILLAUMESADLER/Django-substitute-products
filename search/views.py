from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import SearchForm
from .models import Product
from users.models import Profile
import re


def index(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        research = form.cleaned_data['research']
    return render(request, 'search/index.html', locals())

def results(request):

    if request.method == 'POST':
        research = request.POST.get("product-name")
    else:
        research = request.GET.get('name')

    product_list = Product.objects.filter(product_name__icontains=research)

    paginator = Paginator(product_list, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'search/result.html', {'products': products, 'product_name': research})

@login_required(login_url='/login/')
def favorites(request):

    favorites_list = request.user.profile.favorites.all()

    """favorites = Favorite.objects.all()\
        .filter(profile=profile.id)\
        .filter()"""

    paginator = Paginator(favorites_list, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        favorites = paginator.page(page)
    except (EmptyPage, InvalidPage):
        favorites = paginator.page(paginator.num_pages)

    return render(request, 'search/favorites.html', {'favorites': favorites})

@login_required(login_url='/login/')
def add_favorite(request, id):

    profile = request.user.profile
    product = Product.objects.get(id=id)
    profile.favorites.add(product)

    return favorites(request)

@login_required(login_url='/login/')
def del_favorite(request, id):

    product = Product.objects.get(id=id)

    request.user.profile.favorites.remove(product)

    return favorites(request)

def product(request, id):

    try:
        product = Product.objects.get(id=id)
        categories = product.product_categories.split(",")
        return render(request, 'search/product.html', {'product': product, 'categories': categories})

    except:
        return render(request, 'search/product.html', {
            'error': 'Oups !',
            'error_messages': 'Le produit rechercher n\'existe pas !'
            })

def substitutes(request, id):

    try:
        product = Product.objects.get(id=id)
        products = Product.objects\
            .filter(product_nutriscore__lt=product.product_nutriscore).order_by("product_nutriscore")
        product_list = []

        product_categories = product.product_categories.split(",")
        for product_to_compare in products:

            categories_count = 0
            categories = product_to_compare.product_categories.split(",")

            for category in categories:

                if category in product_categories:

                    categories_count += 1

            if categories_count >= 5:

                product_list.append(product_to_compare)

    except Product.DoesNotExists:
        pass

    paginator = Paginator(product_list, 6)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'search/substitutes.html', {'product': product, 'products': products})

def legales_notices(request):
    return render(request, 'search/legales_notices.html')