from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orders.forms import ArticleForm, deliveryForm
from orders.models import (Article, Cart, ClassicOrder, Delivery,
                           userDeliveryAdress)
from store.models import Finition, Lace, Product, Taille


def compute_total_price(cart):
    #cart = get_object_or_404(Cart)
    article_list = cart.articles.all()
    pr=0.0
    for article in article_list:
        pr += article.product.price * article.quantity
    cart.total_price = pr
    return(cart)

def compute_total_quantity(cart):
    article_list = cart.articles.all()
    qt=0
    for article in article_list:
        qt += article.quantity
    cart.quantity_total = qt
    return(cart)

def update_cart_instance(cart):
    cart_1 = compute_total_price(cart)
    cart_2 = compute_total_quantity(cart_1)
    return(cart_2)

def get_a_cart():
    cart,_ = Cart.objects.get_or_create()
    cart.update_cart_instance() #cart1 = update_cart(cart)
    article_list = cart.articles.all()
    return ((cart, article_list))

def get_an_order(user_auth=True):
    if user_auth:
        order,_ = ClassicOrder.objects.get_or_create()
    """elif not user_auth:
        order,_ = AnonymousOrder.objects.get_or_create()
    """

    #cart.update_cart_instance() #cart1 = update_cart(cart)
    #article_list = cart.articles.all()
    return (order)

def remove_article_from_cart(request, article_id):
    """ Supprimer un article from the cart. """
    cart, article_list = get_a_cart()
    article = article_list.filter(id = article_id)
    articles = article_list.exclude(id=article_id)
    article.delete() # effacer definitivement de la base de données
    #cart.articles.all().delete()
    cart.articles.set(articles)
    cart.update_cart_instance()
    return render(request,
                'orders/shop-cart.html',
                context={"article_list":articles,
                         "cart":cart})


def shop_cart(request):
    cart, _ = Cart.objects.get_or_create()
    cart.compute_total_price()
    article_list = cart.articles.all()
    return render(request,
                'orders/shop-cart.html',
                context={"article_list":article_list,
                         "cart":cart})


def shop_order_delivery(request):
    cart, article_list = get_a_cart()
    country_list = ["France", "Allemagne", "Angleterre", "Espagne"]
    if request.method =="POST":

        # retrieve data form delivery page
        customer_firstname = request.POST.get("firstName")
        client_lastname = request.POST.get("lastName")
        client_email = request.POST.get("email")
        client_phone = request.POST.get("phone")
        customer_adresse = request.POST.get("address")
        customer_adresse_comp = request.POST.get("address_comp")
        customer_country = request.POST.get("country")
        customer_ville = request.POST.get("ville")
        customer_zipcode = request.POST.get("codepostal")
        is_same_address_facturation = request.POST.get("same-address")
        print(is_same_address_facturation)

        # create a delivery adress
        delivery_address = Delivery.objects.create(firstname=customer_firstname, lastname = client_lastname,
                                                  phone_number=client_phone, email = client_email,
                                                  Adresse = customer_adresse,
                                                  adresse_complementaire=customer_adresse_comp,
                                                  country = customer_country, Ville = customer_ville,
                                                  zip_code=customer_zipcode
                                                )
        # create classic order
        if request.user.is_authenticated:
            # User is authenticated, perform actions accordingly
            user = request.user
            userDeliveryAdress.objects.create(user=user, delivery_address = delivery_address).save()
            order = ClassicOrder.objects.create(user=user, articles=article_list, cart=cart,
                                                delivery_address=delivery_address) #defaults={'status': 10.0})
            order.save()
        """elif not request.user.is_authenticated:
            order,_ = AnonymousOrder.objects.get_or_create(cart=cart, articles=article_list,  
                                                           delivery_address=delivery_address) #defaults={'status': 10.0})
            order.save()
        """
        
        return render(request,
                'payments/checkout.html',
                {"order":order,
                'cart':cart,
                'article_list':article_list,
                #"STRIPE_PUBLIC_KEY": 
                })
        

    if request.method == "GET":
        return render(request,
                        'orders/shop-delivery.html',
                        {'country_list':country_list,
                        "cart":cart,
                        'article_list':article_list})

def process_cart(request):
    cart, article_list = get_a_cart()
    cart.update_cart_instance()

    if request.method == "GET":
        return(render(request,
                    'orders/shop-cart.html',
                    context={"article_list":article_list,
                            "cart":cart}))
    if request.method == "POST":
        action = request.POST.get("action")
        if (action == "update-cart") or (action == "update-validate-cart") :
            index=1
            for cartArticle in article_list:
                quantity = request.POST.get("quantity_"+str(index))
                cartArticle.quantity = int(quantity)
                cartArticle.price = int(quantity) * cartArticle.product.price
                cartArticle.save()
                index+=1
            cart.update_cart_instance()
            cart.save()
            article_list = cart.articles.all()
        
        if action == "update-cart" :
            return(render(request,
                    'orders/shop-cart.html',
                    context={"article_list":article_list,
                            "cart":cart}))
        
        elif action == "update-validate-cart" :
            if request.user.is_authenticated:
                # User is authenticated, perform actions accordingly
                #user = request.user
                #order = ClassicOrder.objects.get_or_create(user=user, cart=cart) #defaults={'status': 10.0})
                country_list = ["France", "Allemagne", "Angleterre", "Espagne"]
                return render(request,
                        'orders/shop-delivery.html',
                        {'country_list':country_list,
                        "cart":cart,
                        'article_list':article_list})
            elif not request.user.is_authenticated:
                return(render(request,'orders/redirection_auth_order.html'))
                # User is not authenticated, handle the case
                #return HttpResponse("User is not authenticated.")

def shop_cart_delete(request):
    """
    Cette fonction supprime tout le panier existant.
    Il est également supprimé dans la base de données.
    """
    cart, _ = get_a_cart()
    if cart :
        cart.articles.all().delete()
        cart.delete()

    request.session['cart'] = []
    """ ---- OR ----
    if cart:=request.cart:
            cart.articles.all().delete()
            cart.delete()
    """
    return(redirect('catalogue'))

def process_add_to_cart (request, product_id):
    if request.method == "POST":
        cart, _ = Cart.objects.get_or_create()
        article_list = cart.articles.all()

        # Check if the cart already exists in the session
        #if 'cart' not in request.session:
        #    request.session['cart'] = []
        
        # Produit
        product = get_object_or_404(Product, pk=int(product_id)) #Product.objects.filter(product_name=product_name)
        
        # caractéristiques du cart Item
        quantity = request.POST.get('quantity')
        taille_id = request.POST.get('taille')
        product.taille = get_object_or_404(Taille, pk=taille_id)
        
        if product.categorie.name =="PERRUQUES":
            finition_id = request.POST.get("finition")
            lace_id = request.POST.get("lace")
            product.finition = get_object_or_404(Finition, pk=int(finition_id))
            product.choix_lace = get_object_or_404(Lace, pk=int(lace_id))
        
        # If the product is not in the cart, add it
        newcartItem = Article()
        newcartItem.product = product
        newcartItem.quantity = int(quantity)
        newcartItem.price = int(newcartItem.quantity) * product.price
        newcartItem.save()
        
        action = request.POST.get("action")
        if action == "add-to-cart" :
            # Check if there is a cart object
            if article_list.count()<1:
                print(article_list.count())
                cart.articles.add(newcartItem)
                cart = update_cart_instance(cart)
                """request.session['cart'].append({"id_product":newcartItem.product.id,
                                                "id_cartitem": newcartItem.id,
                                                "quantity": newcartItem.quantity,
                                                "price" : newcartItem.price})
                """
            else :
                product_in_cart_object = False
                for cartArticle in article_list :
                    if cartArticle.product.id == newcartItem.product.id:
                        taille_eq = cartArticle.product.taille_id == newcartItem.product.taille.id
                        if (product.categorie.name =="PERRUQUES"):
                            lace_eq = cartArticle.product.choix_lace_id == newcartItem.product.choix_lace.id
                            finition_eq = cartArticle.product.finition_id == newcartItem.product.finition.id
                            print(f"finition_eq : {finition_eq}")
                            print(f"lace_eq : {lace_eq}")
                            print(f"taille_eq : {taille_eq}")
                            #if (taille_eq and finition_eq and lace_eq) :
                            if (taille_eq and finition_eq and finition_eq ):
                                product_in_cart_object = True
                                cartArticle.quantity += int(quantity)
                                cartArticle.price = cartArticle.product.price * cartArticle.quantity
                                cartArticle.save()
                                cart = update_cart_instance(cart)
                                cart.save()
                                continue
                            
                        else :
                            #if True:
                            if (taille_eq):
                                product_in_cart_object = True
                                cartArticle.quantity += int(quantity)
                                cartArticle.price = cartArticle.product.price * cartArticle.quantity
                                cartArticle.save()
                                cart = update_cart_instance(cart)
                                cart.save()
                                product_in_cart_object = True
                                continue

                if not product_in_cart_object:
                    cart.articles.add(newcartItem)
                    cart = update_cart_instance(cart)
                    cart.save()
                    """request.session['cart'].append({"id_product":newcartItem.product.id,
                                                    "id_cartitem": newcartItem.id,
                                                    "quantity": newcartItem.quantity,
                                                    "price" : newcartItem.price})
                    """
            cart = update_cart_instance(cart)
            cart.save()

            """
            # Check if the cart already exists in the session
            if 'cart' not in request.session:
                request.session['cart'] = []
            # Check if the product is already in the cart (request.session)
            if len(request.session['cart'])>=1:
                product_in_session_cart = False
                for cartItem in request.session['cart']:
                    
                    if cartItem["id_product"] == product.id:
                        pr_cartitem = get_object_or_404(pk=cartItem["id_product"])
                        taille_eq = (pr_cartitem.taille.id == product.taille.id)
                        print(f"taille_id: {pr_cartitem.taille.id} / {taille_eq}")
                        if (product.categorie.name =="PERRUQUES"):
                            finition_eq = pr_cartitem.finition.id == product.finition.id
                            lace_eq = pr_cartitem.choix_lace.id == product.choix_lace.id
                            if (taille_eq and finition_eq and lace_eq) :
                                cartItem.quantity += int(quantity)
                                product_in_session_cart = True
                                break
                        else :
                            if (taille_eq):
                                cartItem.quantity += int(quantity)
                                product_in_session_cart = True
                                break
            #
            elif (len(request.session['cart'])<1) or (not product_in_session_cart):
                request.session['cart'].append({"id_product":newcartItem.product.id,
                                                "id_cartitem": newcartItem.id,
                                                "quantity": newcartItem.quantity,})                                                "price" : newcartItem.price})
            """
            
            #return(redirect('shop_cart'))
            return(redirect(reverse("product_detail",kwargs={"product_id":product_id})))

        elif action == "go-to-checkout" :
            
            # Check if the cart already exists in the session
            if 'cart' not in request.session:
                request.session['cart'] = []
            # Sauvegarder le panier actuel dans la session pour le recupérer
            # après l'achet express.
            for cartItem in article_list :
                request.session['cart'].append({"id_product":cartItem.product.id,
                                                "id_cartitem": cartItem.id,
                                                "quantity": cartItem.quantity,
                                                "price" : cartItem.price})
            
            # Creation of new cart Item
            cart.articles.all().delete()
            cart.articles.add(newcartItem)
            cart.save()
            cart.update_cart_instance()
            cart.save()
            #cart = update_cart_instance(cart)
            
            return(render(request,'orders/shop-delivery.html',
                          context={"cart":cart,
                                   'article_list':cart.articles.all()}))

        
def add_to_cart(request):
    
    if request.method == "POST":

        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name")
        taille = request.POST.get("taille")
        quantity = request.POST.get("quantity")
        form = ArticleForm()
        dataf = form.cleaned_data
        dataf
    pass

def get_to_checkout(request):
    pass