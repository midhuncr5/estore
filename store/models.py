from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):

    bio=models.CharField(max_length=260,null=True)

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.user_object.username



class UserDetail(models.Model):

    name=models.CharField(max_length=200)        

    address=models.TextField()

    phone=models.CharField(max_length=100,null=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    




class Tag(models.Model):

    title=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
     
    def __str__(self):

        return self.title
    
class Brand(models.Model):
    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.title
    
class memory(models.Model):
    title=models.CharField(max_length=200)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Colour(models.Model):
    title=models.CharField(max_length=200)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    def __str__(self):

        return self.title

class Product(models.Model):
    
    title=models.CharField(max_length=200)

    description=models.TextField()

    product_pic=models.ImageField(upload_to="product_pictures",default="/product_pictures/default.png")

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="produts")

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)

    tag_object=models.ManyToManyField(Tag)
    
    memory_object=models.ForeignKey(memory,on_delete=models.CASCADE,null=True)

    colour_object=models.ForeignKey(Colour,on_delete=models.CASCADE)

    battery_capacity=models.CharField(max_length=200)          
    
    price=models.PositiveIntegerField()
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    # @property
    # def avg_rating(self):

    #     return Review.objects.filter(product_object=self).count()





class WishList(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

class WishListItems(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    WishList_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="cart_items")
    
    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


    
class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    name=models.CharField(max_length=200)

    address=models.CharField(max_length=300)

    phone=models.CharField(max_length=100)

    product_object=models.ManyToManyField(Product)

    order_id=models.CharField(max_length=200,null=True)

    STATUS =(
        ('order placed','order placed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'), )
      
    status=models.CharField(max_length=50,null=True,choices=STATUS)


    is_paid=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField(null=True) 

    def __str__(self):

        return self.order_id
    


      
     

   


from django.db.models.signals import post_save


def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)

post_save.connect(sender=User,receiver=create_profile)


def create_cart(sender,instance,created,*args,**kwargs):
    print(instance)
    if created:
        WishList.objects.create(owner=instance)
post_save.connect(sender=User,receiver=create_cart)



def create_profile_detail(sender,instance,created,*args,**kwargs):

    if created:
        UserDetail.objects.create(user_profile_object=instance)
post_save.connect(sender=User,receiver=create_profile_detail)


from django.core.validators import MaxValueValidator,MinValueValidator
class Review(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="project_review")

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    comment=models.TextField()

    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)



    












  

    



    


    



    
    




