from django import forms
from .models import resort,room,signup

class resortform(forms.ModelForm):
   class Meta:
        model = resort
        fields = ['name', 'locality', 'email', 'phone', 'address', 'land_mark', 'parking', 'image']
        
   
    
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'land_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'parking': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name':'Name Of Resort',
            'email':'Email ID',
            'phone':'Phone Number',
             'image': 'Resort Image'
           
            
        }
        
        

class ResorteditForm(forms.ModelForm):
    class Meta:
        model = resort
        exclude = ['image']  # Exclude the image field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'land_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'parking': forms.Select(attrs={'class': 'form-control'}),
        }

       
       

 
class roomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = ['room_type', 'wifi_number', 'tv_number', 'food', 'price']
        widgets = {
        
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'wifi_number': forms.Select(attrs={'class': 'form-control'}),
            'tv_number': forms.Select(attrs={'class': 'form-control'}),
            'food': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'resort_name': 'Name of Hotel',
        }     
        
        
class signupForm(forms.ModelForm):
    class Meta:
        model = signup
        fields = ['name', 'email', 'gender', 'phone', 'username', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name of person',
        }          
        
        
class availableForm(forms.Form):
   
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    adults = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    children = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rooms = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    room_type = forms.ChoiceField(choices=room.ROOM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    labels = {
            'name': 'Name of Hotel',
        }

    
        
        
        
class BookingForm(forms.Form):
    number_of_rooms = forms.IntegerField(label="Number of Rooms", min_value=1)
    number_of_adults = forms.IntegerField(label="Number of Adults", min_value=1)
    number_of_children = forms.IntegerField(label="Number of Children", min_value=0)
    from_date = forms.DateField(label="From Date", widget=forms.SelectDateWidget())
    to_date = forms.DateField(label="To Date", widget=forms.SelectDateWidget()) 
    
    
class CardPaymentForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)   

from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'from_date', 'to_date', 'adults', 'children']
   