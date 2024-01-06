"""
URL configuration for siteLariParis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import accounts.views as accounts_views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from orders import views as orders_views
from payments import views as payments_views
from store import views as store_views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.index, name="index"),
    path('store/', store_views.catalogue, name="catalogue"),
    path('store/categorie_<int:categorie_id>/', store_views.categorie, name="product_categorie"),
    path('store/categorie_<int:categorie_id>/lace_<int:lace_id>', store_views.categorie_perruque, name="perruque_lace"),
    #path('shop-products/<slug:categorie_slug>/', store_views.categorie_slug, name="product_categorie"),
    path('store/<int:product_id>/', store_views.product_detail, name="product_detail"),
    path('store/<int:product_id>/process-cart-data/', orders_views.process_add_to_cart, name="process_add_to_cart"),

    path('signup/', accounts_views.signup, name="signup"),
    path('login/', accounts_views.login_user, name="login"),
    path('logout/', accounts_views.logout_user, name="logout"),
    
    path('shop-cart/', orders_views.shop_cart, name='shop_cart'),
    path('shop-cart/process-cart/', orders_views.process_cart, name="process_cart"),
    path('shop-cart/delete/', orders_views.shop_cart_delete, name='shop_cart_delete'),
    path('shop-cart/delete-article/article_<int:article_id>/', orders_views.remove_article_from_cart, name='cart_delete_an_article_from_cart'),
    path('shop-delivery/', orders_views.shop_order_delivery, name = 'shop_delivery'),
    
    path('webhooks/stripe/', payments_views.stripe_webhook, name="stripe-webhook"),
    path('cancel/', payments_views.cancelView, name='cancel'),
    path('success/', payments_views.successView, name='success'),
    path('create-checkout-session/order_<int:order_id>/', payments_views.CreateCheckoutSessionView, name='create_checkout_session'),

    #path('shop-products/<int:product_id>/get_to_checkout/', orders_views.get_to_checkout, name="get_to_checkout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
