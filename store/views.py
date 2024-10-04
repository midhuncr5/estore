from django.shortcuts import render,redirect
from django.views import View
from store.forms import SignupForm,SiginForm,UserProfileForm,ProductForm,UserDetailConfirmForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from store.models import Product
from django.urls import reverse_lazy,reverse
from store.models import UserProfile,User,WishListItems,OrderSummary,UserDetail
from django.db.models import Sum
from decouple import config
from django.utils import timezone
from django.views.generic import ListView


# Create your views here.


class SignUpView(View):
    def get(self,request,*args,**kwargs):

        form_instance=SignupForm()

        return render(request,"store/register.html",{"register":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignupForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            messages.success(request,"successfuly created account")
            return redirect("login")

        else:
            return render(request,"store/register.html",{"register":form_instance})

class SignInView(View):
    def get(self,request,*args,**kwargs):

        form_instance=SiginForm()

        return render(request,"store/login.html",{"login":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SiginForm(request.POST)

        if form_instance.is_valid():
            data=form_instance.cleaned_data

            user_obj=authenticate(**data)

            if user_obj:

                login(request,user_obj)

                messages.success(request,"successfully login")
                

                return redirect("home")
            else:
                return render(request,"store/login.html",{"login":form_instance})
            
class SignOutView(View):
    def get(self,request,*args,**kwargs):

        logout(request)


        return redirect("login")
    

class HomePageView(View):
    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"store/index.html",{"product":qs})
    
class UserProfileUpdateView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        obj=UserProfile.objects.get(id=id)

        

        form_instance=UserProfileForm(instance=obj)

        

        return render(request,"store/profile_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        user_obj=UserProfile.objects.get(id=id)

        form_instance=UserProfileForm(request.POST,files=request.FILES,instance=user_obj)

        if form_instance.is_valid():
            form_instance.instance.user_object=request.user
   

            form_instance.save()

            return redirect("home")
        else:
            return render(request,"store/profile_edit.html",{"form":form_instance})
        

class ProductCreateView(View):
    def get(self,request,*args,**kwargs):

        form_instance=ProductForm()

        return render(request,"store/product_add.html",{"product":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=ProductForm(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("home")
        else:
            return render(request,"store/product_add.html",{"product":form_instance})
        

class ProductDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)


        return render(request,"store/product_detail.html",{"product":product_obj})
    

class SearchView(ListView):
    model = Product
    template_name = 'store/result.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            product = Product.objects.filter(title__contains=query)
            result = product
        else:
            result = None

        return result


    


        

class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        print(request.user.cart)

        WishListItems.objects.create(product_object=product_obj,WishList_object=request.user.cart)
        
        return redirect("home")


class CartListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cart_items.filter(is_order_placed=False)

        total=request.user.cart.cart_items.filter(is_order_placed=False).values("product_object__price").aggregate(total= Sum("product_object__price"))

        t=total.get("total")

        return render(request,"store/cart_summary.html",{"cart_items":qs,"total":t})
    
class ProductListView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        
        user_detail=UserDetail.objects.get(user_profile_object=request.user)

        

        product_obj=Product.objects.get(id=id)

        

        

        return render(request,"store/product_list.html",{"product":product_obj,"user":user_detail})


class CartRemoveView(View):
    
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        print(id)


        WishListItems.objects.get(id=id).delete()

        return redirect("cart-summary")
    



class UserDetailConfirmView(View):
    def get(self,request,*args,**kwargs):

        # user_obj=UserDetail.objects.get(id=id)

        id=kwargs.get("pk")
        user_obj=UserDetail.objects.get(id=id)
        print("---------------------------",user_obj)

        form_instance=UserDetailConfirmForm(instance=user_obj)


        return render(request,"store/user_confirm.html",{"user":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        user_obj=UserDetail.objects.get(id=id)
        print(id)

        form_instance=UserDetailConfirmForm(request.POST,instance=user_obj)

        if form_instance.is_valid():
           form_instance.instance.user_profile_object=request.user

           form_instance.save()

           return redirect("checkout")
        
        else:

            return render(request,"store/user_confirm.html",{"user":form_instance})
        



KEY_ID=config("KEY_ID")
KEY_SECRET=config("KEY_SECRET")
import razorpay        
class CheckoutView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        
        cart_items=request.user.cart.cart_items.filter(is_order_placed=False)
        t=request.user.cart.cart_items.filter(is_order_placed=False).values("product_object__price").aggregate(total= Sum("product_object__price")).get("total")

        detail=UserDetail.objects.get(user_profile_object=request.user)
        print(detail)

        # ----------------------------------------------

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        total=t*100

        data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

    
           
        order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get("id"),total=t)

        for ci in cart_items:

            order_summary_obj.product_object.add(ci.product_object)

            print("==========================",order_summary_obj)

        order_summary_obj.save()
        

        print(payment)

        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }

        # ================================================

        return render(request,"store/checkout.html",{"cart":cart_items,"total":total,"detail":detail,"context":context})



        
        

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")

class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        order_summary_obj=OrderSummary.objects.get(order_id=request.POST.get("razorpay_order_id"))

        login(request,order_summary_obj.user_object)

        # 'razorpay_payment_id': ['pay_Osc4W3SzwsS9D4'], 'razorpay_order_id': ['order_Osc45PLWmmuS2r'], 'razorpay_signature': ['0ddd337bace49384729e5bb28dcb3b115e6b41df29bd0d4e6ef189d81748931d'

        try:
            client.utility.verify_payment_signature(request.POST)

            print("payment success")

            order_id=request.POST.get("razorpay_order_id")


            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True,status="order placed")


            cart_items=request.user.cart.cart_items.filter(is_order_placed=False)

            for ci in cart_items:
                ci.is_order_placed=True

                ci.save()

        except:
            print("payment failed")

        
        return redirect("home") 
    

class MyPurchaseView(View):
    def get(self,request,*args,**kwargs):

        order_obj=OrderSummary.objects.filter(is_paid=True,user_object=request.user)

        order=reversed(order_obj)


        # print("====================",product_obj)


        return render(request,"store/order_summary.html",{"orders":order})
















            
        





       

      


    
    



    
    
       



        
        

        






        
            




        
            

