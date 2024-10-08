from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from store.models import UserProfile,Product,UserDetail,Review



class SignupForm(UserCreationForm):

    password1=forms.CharField(widget=(forms.TextInput(attrs={"class":"form-control"})))
    password2=forms.CharField(widget=(forms.PasswordInput(attrs={"class":"form-control"})))

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control "}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
           
        }


class SiginForm(forms.Form):

    username=forms.CharField(widget=(forms.TextInput(attrs={"class":"form-control"})))
    password=forms.CharField(widget=(forms.TextInput(attrs={"class":"form-control"})))

class UserProfileForm(forms.ModelForm):
    class Meta:

        model=UserProfile
        fields=["bio","profile_pic"]
        widgets={
            "bio":forms.TextInput(attrs={"class":"form-control"}),

            "profile_pic":forms.FileInput(attrs={"class":'form-control'}),

        }

class ProductForm(forms.ModelForm):

    class Meta:
        model=Product
        fields=["title","description","product_pic","brand_object","memory_object","colour_object","price","battery_capacity"]

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":5}),
            "product_pic":forms.FileInput(attrs={"class":"form-control"}),
            "brand_object":forms.Select(attrs={"class":"form-control form-select"}),
            "memory_object":forms.Select(attrs={"class":"form-control form-select"}),
            "colour_object":forms.Select(attrs={"class":"form-control form-select"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "battery_capacity":forms.TextInput(attrs={"class":"form-control form-select"})

        }


class UserDetailConfirmForm(forms.ModelForm):
    class Meta:
        model=UserDetail
        fields=["name","address","phone"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.Textarea(attrs={"class":"form-control ","rows":5}),
            "phone":forms.NumberInput(attrs={"class":"form-control"})
        }


class ReviewForm(forms.ModelForm):

    class Meta:

        model=Review

        fields=["comment","rating"]

        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control"}),
            "rating":forms.NumberInput(attrs={"class":"form-control"})
        }


    