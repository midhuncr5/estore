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
    path("product/detail/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/add/<int:pk>/wishlist/",views.AddToCartView.as_view(),name="cart-add"),
    path("cart/summary/",views.CartListView.as_view(),name="cart-summary"),
    path("remove/cartitem/<int:pk>/",views.CartRemoveView.as_view(),name="cart-remove"),
    path("customer/detail/",views.CustomerDetailConfirmView.as_view(),name="customer-detail"),
    path("payment/verification/",views.PaymentVerificationView.as_view(),name="payment-verify"),
    path("order/summary",views.MyPurchaseView.as_view(),name="my-orders"),
    path('results/',views.SearchView.as_view(), name='search'),
    path("product/<int:pk>/list/",views.ProductListView.as_view(),name="product-list"),
    path("change/address/<int:pk>/<int:mk>",views.ChangeAddressView.as_view(),name="change-address"),
    path("single/checkout/<int:pk>/",views.SingleCheckoutView.as_view(),name="single-checkout"),
    path("review/add/<int:pk>/",views.ReviewCreateView.as_view(),name="review-add")
    
     
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

