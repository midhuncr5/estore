from django.shortcuts import render,redirect
from django.views import View
from store.forms import SignupForm,SiginForm,UserProfileForm,ProductForm,UserDetailConfirmForm,ReviewForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from store.models import Product
from django.urls import reverse_lazy,reverse
from store.models import UserProfile,User,WishListItems,OrderSummary,UserDetail,Review
from django.db.models import Sum,Avg
from decouple import config
from django.utils import timezone
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from store.decorators import signin_required


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

@method_decorator(signin_required,name="dispatch")                 
class SignOutView(View):
    def get(self,request,*args,**kwargs):

        logout(request)


        return redirect("login")
    

@method_decorator(signin_required,name="dispatch")     
#index page-----------
class HomePageView(View):
    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"store/index.html",{"product":qs})
    

@method_decorator(signin_required,name="dispatch")     
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
        

        
@method_decorator(signin_required,name="dispatch")     
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        
        review=Review.objects.filter(product_object=product_obj)

       

        if review:

            rating_sum=Review.objects.filter(product_object=product_obj).aggregate(sum=Sum("rating")).get("sum")

            rating_count=Review.objects.filter(product_object=product_obj).count()

            avg_rating=rating_sum/rating_count


            return render(request,"store/product_detail.html",{"product":product_obj,"review":review,"rating":avg_rating})
        
        else:
            return render(request,"store/product_detail.html",{"product":product_obj,})





        
    
@method_decorator(signin_required,name="dispatch")     
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


        
@method_decorator(signin_required,name="dispatch")     
class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        print(request.user.cart)

        WishListItems.objects.create(product_object=product_obj,WishList_object=request.user.cart)
        
        return redirect("home")



@method_decorator(signin_required,name="dispatch")     
class CartListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cart_items.filter(is_order_placed=False)

        total=request.user.cart.cart_items.filter(is_order_placed=False).values("product_object__price").aggregate(total= Sum("product_object__price"))

        t=total.get("total")

        return render(request,"store/cart_summary.html",{"cart_items":qs,"total":t})
    

       
@method_decorator(signin_required,name="dispatch")     
class CustomerDetailConfirmView(View):

    def get(self,request,*args,**kwrgs):

        return render(request,"store/customer_detail.html")
    
    def post(self,request,*args,**kwargs):
    
        name=request.POST.get("name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")

        cart_items=request.user.cart.cart_items.filter(is_order_placed=False)
        t=request.user.cart.cart_items.filter(is_order_placed=False).values("product_object__price").aggregate(total= Sum("product_object__price")).get("total")

        # ----------------------------------------------

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        total=t*100

        data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)
           
        order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get("id"),total=t,name=name,address=address,phone=phone)

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

        return render(request,"store/checkout.html",{"cart":cart_items,"total":total,"context":context,"name":name,"address":address,"phone":phone})
        
 

@method_decorator(signin_required,name="dispatch")         
class ProductListView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)
        
        return render(request,"store/product_list.html",{"product":product_obj})
    

@method_decorator(signin_required,name="dispatch")         
class ChangeAddressView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_id=kwargs.get("mk")
        product_obj=Product.objects.get(id=product_id)

        user_obj=UserDetail.objects.get(id=id)

        form_instance=UserDetailConfirmForm(instance=user_obj)

        return render(request,"store/user_confirm.html",{"user":form_instance})
    
    def post(self,request,*args,**kwargs):

        product_id=kwargs.get("mk")

        product_obj=Product.objects.get(id=product_id)

        id=kwargs.get("pk")
        user_obj=UserDetail.objects.get(id=id)
        print(id)

        form_instance=UserDetailConfirmForm(request.POST,instance=user_obj)

        if form_instance.is_valid():

           form_instance.save()

           return render(request,"store/product_list.html",{"user":user_obj,"product":product_obj})
        
        else:

            return render(request,"store/user_confirm.html",{"user":form_instance})
        

KEY_ID=config("KEY_ID")
KEY_SECRET=config("KEY_SECRET")
import razorpay  

@method_decorator(signin_required,name="dispatch")     
class SingleCheckoutView(View):

    def get(self,request,*args,**kwargs):


        return render(request,"store/customer_detail.html")

    def post(self,request,*args,**kwargs):

        name=request.POST.get("name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")



        id=kwargs.get("pk")


        product_obj=Product.objects.get(id=id)

        print("==================",product_obj)
        t=product_obj.price

    
         
        # ----------------------------------------------

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        total=t*100

        data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

    
           
        order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get("id"),total=t,name=name,address=address,phone=phone)

        if order_summary_obj:

            order_summary_obj.product_object.add(product_obj)

           

        order_summary_obj.save()
        

        print(payment)

        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id")
        }

        # ================================================

        return render(request,"store/checkout.html",{"product":product_obj,"total":total,"context":context,"name":name,"address":address,"phone":phone})


@method_decorator(signin_required,name="dispatch")     
class CartRemoveView(View):
    
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        print(id)


        WishListItems.objects.get(id=id).delete()

        return redirect("cart-summary")
    
       
        

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")
@method_decorator(signin_required,name="dispatch")     
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):

       
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
    

@method_decorator(signin_required,name="dispatch")     
class MyPurchaseView(View):
    def get(self,request,*args,**kwargs):

        order_obj=OrderSummary.objects.filter(is_paid=True,user_object=request.user)

        order=reversed(order_obj)

        return render(request,"store/order_summary.html",{"orders":order})


@method_decorator(signin_required,name="dispatch")     
class ReviewCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ReviewForm()

        return render(request,"store/review_add.html",{"review":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        print("=============",id)

        product_obj=Product.objects.get(id=id)

        print("=================",product_obj)

        form_instance=ReviewForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.product_object=product_obj

            form_instance.instance.user_object=request.user

            form_instance.save()

            return redirect("my-orders")
        
        return render(request,"store/review_add.html",{"review":form_instance})













            
        





       

      


    
    



    
    
       



        
        

        






        
            




        
            

