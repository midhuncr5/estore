"""
URL configuration for estore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.SignUpView.as_view(),name="sign-up"),
    path("",views.SignInView.as_view(),name="login"),
    path("signout/",views.SignOutView.as_view(),name="sign-out"),
    path("index/",views.HomePageView.as_view(),name="home"),
    path("profile/<int:pk>/change",views.UserProfileUpdateView.as_view(),name="profile-edit"),
    path("products/add/",views.ProductCreateView.as_view(),name="product-add"),
    path("product/detail/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/add/<int:pk>/wishlist/",views.AddToCartView.as_view(),name="cart-add"),
    path("cart/summary/",views.CartListView.as_view(),name="cart-summary"),
    path("remove/cartitem/<int:pk>/",views.CartRemoveView.as_view(),name="cart-remove"),
    # path("buy/now/",views.BuyNowView.as_view(),name="buy-now"),
    path("userdetail/<int:pk>/confirm/",views.UserDetailConfirmView.as_view(),name="user-detail"),
    path("checkout/",views.CheckoutView.as_view(),name="checkout"),
    path("payment/verification/",views.PaymentVerificationView.as_view(),name="payment-verify"),
    path("order/summary",views.MyPurchaseView.as_view(),name="my-orders"),
    path('results/',views.SearchView.as_view(), name='search'),
    
    
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

