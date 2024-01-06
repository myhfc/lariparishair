from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from orders.views import get_a_cart

User = get_user_model()

def signup(request):
    if request.method == "POST" :
        # Traiter le formulaire
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        user_password = request.POST.get("password")
        user_email = request.POST.get("email")

        user = User.objects.create_user( username = username,
                                        last_name = lastname,
                                        first_name = firstname,
                                        password = user_password,
                                        email = user_email
                                        )
        login(request, user)
        if "next" in request.GET : # car le lien url passe le paramètre "next" dans une requête de type GET
            return redirect(request.POST.get('next', 'shop_delivery'))
        else:
            return(redirect('index'))
        
    elif request.method=="GET":
        return render(request,
                    'accounts/signup.html')

def login_user(request):

    if request.method == "POST" :
        # Traiter le formulaire
        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(username=username,
                            email=user_email,
                            password=user_password)
        # TO DO : retrieve cart from either : request.session or database non-validated orders

        # redirection after user authentication
        if (user) :
            login(request, user)
            if "next" in request.GET : # car le lien url passe le paramètre "next" dans une requête de type GET
                return redirect(request.POST.get('next', 'shop_delivery'))
            else:
                return (redirect('catalogue'))
    else:
        next_page = request.GET.get('next', '')
        return render(request,
                    'accounts/connexion.html',
                    {'next_page': next_page})

def logout_user(request):
    _, article_list = get_a_cart()
    if 'cart' not in request.session:
        request.session['cart'] = []

    for newcartItem in article_list:
        request.session['cart'].append({"id_product":newcartItem.product.id,
                                        "id_cartitem": newcartItem.id,
                                        "quantity": newcartItem.quantity
        })
    logout(request)
    return redirect('index')
