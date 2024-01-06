from django.shortcuts import get_object_or_404, render
from orders.views import get_a_cart
from store.models import (Categorie, Finition, Images_site_lariparis, Lace,
                          Product, Taille)


def index(request):
    categories = Categorie.objects.all()
    imgs_accueil = get_object_or_404(Images_site_lariparis, pk=1)
    products = Product.objects.all()
    cart, article_list = get_a_cart()
    return render(request,
                'store/index.html',
                context={'categories': categories,
                         'imgs_accueil':imgs_accueil,
                         'products':products,
                         'cart':cart,
                         'article_list':article_list})

def catalogue(request):
    products = Product.objects.all()
    cat = "Boutique LARIPARIS HAIR"
    cart, article_list = get_a_cart()
    return render(request,
                'store/categorie.html',
                {'products': products,
                 'cat':cat,
                 'cart':cart,
                 'article_list':article_list})

def categorie(request, categorie_id):
    products = Product.objects.filter(categorie_id=categorie_id)
    cat = products[0].categorie.name
    cart, article_list = get_a_cart()
    return render(request,
                'store/categorie.html',
                {'products': products,
                 'cat':cat,
                 'cart':cart,
                 'article_list':article_list})

"""def categorie_slug(request, categorie_slug):
    categorie = Categorie.objects.filter(slug=categorie_slug)
    products = Product.objects.filter(categorie=categorie)
    cat = products[0].categorie.name
    cart,_ = Cart.objects.get_or_create()
    return render(request,
                'store/categorie.html',
                {'products': products,
                'cat':cat,
                'cart':cart})
"""
def categorie_perruque(request, categorie_id, lace_id):
    #products = Product.objects.filter(categorie_id=categorie_id)
    products = Product.objects.filter(categorie_id=categorie_id,choix_lace_id= lace_id)
    cat = products[0].categorie.name
    cart, article_list = get_a_cart()
    return render(request,
                'store/categorie.html',
                {'products': products,
                 'cat':cat,
                 'cart':cart,
                 'article_list':article_list})

def product_detail(request, product_id):
    cart, article_list = get_a_cart()
    product = get_object_or_404(Product, pk=product_id)
    #product_similaires = Product.objects.filter(categorie_id=product.categorie_id,choix_lace= product.choix_lace)
    product_similaires = Product.objects.filter(categorie_id=product.categorie_id)
    categorie = get_object_or_404(Categorie, pk=product.categorie_id)
    taille_list = Taille.objects.all()
    #taille_list = taille_list.exclude(name=product.taille.name)

    if categorie.name == "PERRUQUES":
        finition_list = Finition.objects.all()
        #finition_list = finition_list.exclude(name=product.finition.name)
        lace_list = Lace.objects.all()
        #lace_list = lace_list.exclude(name=product.choix_lace.name)
        
        return render(request,
            'store/shop-product-detail.html',
            {'product': product,
            'product_similaires':product_similaires,
            'taille_list':taille_list,
            'finition_list':finition_list,
            'lace_list':lace_list,
            'taille_list':taille_list,
            'quantity_list': [i for i in range(2,16)],
            'cart':cart,
            'article_list':article_list})
    
    return render(request,
            'store/shop-product-detail.html',
            {'product': product,
            'product_similaires':product_similaires,
            'taille_list':taille_list,
            'quantity_list': [i for i in range(2,16)],
            'cart':cart,
            'article_list':article_list})



