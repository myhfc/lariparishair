import pytz
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from orders.models import STATUS_ORDER, AnonymousOrder, Cart, ClassicOrder

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def successView(request):
    #order, _ = ClassicOrder.objects.get_or_create()
    #order.ordered=True
    #order.
    #article_list = order.cart.articles.all()
    return render(request,
                'payments/success.html',
                )

def cancelView(request):
    return render(request,
                'payments/cancel.html',
                )
@csrf_exempt
def CreateCheckoutSessionView(request, order_id):
    
    if request.user.is_authenticated:
        customer_email = request.user.email
        order = get_object_or_404(ClassicOrder, pk = order_id)

    elif not request.user.is_authenticated:
        order = get_object_or_404(AnonymousOrder,pk = order_id)
        customer_email =order.delivery_adress.email
    #price = Price.objects.get(id=self.kwargs["pk"])
    
    articles_list = order.articles.all()
    cart_items=[]; #metadata_list = []
    for cartItem in articles_list:
        prix_unitaire = cartItem.product.price * 100
        print(f"prix_unitaire en centimes : {int(prix_unitaire)} €")
        cart_items.append({
            'price_data':{
                'currency':"eur",
                'unit_amount': int(prix_unitaire),
                'product_data':{
                    'name' : cartItem.product.name,
                },
            },
            'quantity': cartItem.quantity,
        })
        #metadata_list.append(cartItem.id)

    metadata={'order_id': order.id,
              #"cart_id":order.cart.id,
              #"cart_item_id":metadata_list,
              "is_user_connected": request.user.is_authenticated}
        
    #cart = order.cart
    domain = "my-holy-father-company.software" #"https://yourdomain.com"
    if settings.DEBUG:
        domain = "http://127.0.0.1:8080"
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card','paypal'],
            line_items=cart_items,
            metadata = metadata,
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
            customer_email = customer_email,
        )
        return redirect(checkout_session.url, code=303)
        #return JsonResponse({ 'id': checkout_session.id})
    except Exception as e :
        return str(e)
    

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Obtenez l'objet de fuseau horaire pour Paris
        timezone_paris = pytz.timezone('Europe/Paris')
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        #payment_intent = session["payment_intent"]
        if session["payment_status"]=='paid':
            metadata = session["metadata"]
            if metadata["is_user_connected"]:
                order = get_object_or_404(ClassicOrder, pk = int(metadata["order_id"]))
            elif not metadata["is_user_connected"]:
                order = get_object_or_404(AnonymousOrder,pk = int(metadata["order_id"]))
            
            articles_list = order.articles.all()
            mess = "LariParisHair vous remercions pour votre commande. "+" \n"
            for cartItem in articles_list:
                cartItem.order=True
                cartItem.ordered_date = timezone.now().astimezone(timezone_paris)
                cartItem.save()
                mess= mess + f'Votre {cartItem.product.categorie.name} dont {cartItem.product.name} acheté en {cartItem.quantity} examplaire. '+"\n"
        
            order.cart.ordered =True
            order.cart.ordered_date = timezone.now().astimezone(timezone_paris)
            order.ordered_date = timezone.now().astimezone(timezone_paris)
            order.cart.save()
            order.ordered = True
            order.ordered_date = timezone.now().astimezone(timezone_paris)
            order.status = STATUS_ORDER.PAIEMENT_VALIDE.value
            order.save()
            
            cart = Cart.objects.create()
            cart.save()

            # send an email to the customer
            send_mail(
            subject="LariParisHair - Votre commande",
            message= mess,
                recipient_list=[customer_email],
                from_email="Lariparis.prestaservice@gmail.com"
            )

    return HttpResponse(status=200)
