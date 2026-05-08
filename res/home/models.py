from django.db import models

from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class reg(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
# username :admin@gmail.in
# password :admin    
    
class card(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username    

# username :gpay
# password:gpay1234@

class resort(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    locality=models.CharField(max_length=500)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=500)
    land_mark=models.CharField(max_length=100)
    parking_choices=[
        ('YES','YES'),
        ('NO','NO'),
    ]
    parking=models.CharField(max_length=100,choices=parking_choices)
    image=models.ImageField(upload_to='resort_images/')
    
    def __str__(self):
        return self.name
    

class room(models.Model):
    resort = models.ForeignKey(resort, related_name='rooms', on_delete=models.CASCADE) 
    
    ROOM_CHOICES = [
        ('single room', 'Single Room'),
        ('double room', 'Double Room'),
        ('special room', 'Special Room'),
    ]
    room_type = models.CharField(max_length=100, choices=ROOM_CHOICES)
    
    WIFI_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    wifi_number = models.CharField(max_length=100, choices=WIFI_CHOICES)
    
    TV_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    tv_number = models.CharField(max_length=100, choices=TV_CHOICES)
    
    FOOD_CHOICES = [
        ('free', 'Free'),
        ('non-free', 'Non-Free'),
    ]
    food = models.CharField(max_length=100, choices=FOOD_CHOICES)
    
    price = models.IntegerField()
    
    
class signup(models.Model): 
    
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255, unique=True)  # Unique email
    GENDER = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    ]
    gender = models.CharField(max_length=100, choices=GENDER)
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)  # Unique username
    password = models.CharField(max_length=128)  # Change


class Booking(models.Model):
    user = models.ForeignKey(signup, on_delete=models.CASCADE)
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    rooms=models.IntegerField()
    adults = models.IntegerField()
    children = models.IntegerField()
    total_days = models.IntegerField()
    booked_amount = models.IntegerField()
    date_of_booking = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.room} at {self.room.resort.name}"
  
        


    
      