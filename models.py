from django.db import models

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class user_reg(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True, null=True)
    phno = models.IntegerField()
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    idproof = models.IntegerField()
    last_login = models.CharField(max_length=100,blank=True, null=True)  # If you added this field

    def __str__(self):
        return self.name

    def get_email_field_name(self):
        return 'email'

class Muncipality(models.Model):
    muncipality_name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.IntegerField()
    muncipality_email=models.EmailField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.username


from django.db import models
from django.core.files import File
from django.urls import reverse
from io import BytesIO

import qrcode  

class Pet(models.Model):
    muncipality=models.ForeignKey(Muncipality, on_delete=models.CASCADE, related_name="addpet")
    dogname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dog_image/',)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.dogname

    def save(self, *args, **kwargs):
        # First, save the pet object if it does not have an ID yet
        if not self.id:
            super().save(*args, **kwargs)

        # Generate the QR code link using the pet detail page URL
        pet_url = f"http://127.0.0.1:8000{reverse('pet_detail', args=[self.id])}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pet_url)  # Add the pet detail URL to the QR code
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code image to a file in memory
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)

        # Save the QR code image to the model's qr_code field
        self.qr_code.save(f'qr_code_{self.id}.png', File(buffer), save=False)

        # Call super().save() again to save the model with the QR code image
        super().save(*args, **kwargs)

   

class trainer_reg(models.Model):
    muncipality = models.ForeignKey(Muncipality, on_delete=models.CASCADE, related_name="trainer_reg")
    Name = models.CharField(max_length=20)
    place = models.CharField(max_length=100,blank=True, null=True)
    address = models.CharField(max_length=200, default='no address provide')
    email = models.CharField(max_length=100)
    certificate = models.FileField(upload_to='certificate/')
    phno = models.IntegerField()
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.Name

class Timetable(models.Model):
    trainer = models.ForeignKey(trainer_reg, on_delete=models.CASCADE, related_name="timetable")
    muncipality_name = models.CharField(max_length=100)
    date = models.CharField(max_length=100) 
    start_time = models.TimeField()  
    end_time = models.TimeField() 
    location = models.CharField(max_length=200) 
    details = models.TextField(null=True, blank=True) 



    

class Adopt(models.Model):
    dogname = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField() 
    muncipality_name = models.ForeignKey(Muncipality, on_delete=models.CASCADE, related_name="adopt")
    idproof=models.IntegerField()
    name=models.CharField(max_length=199)
    email=models.CharField(max_length=200)
    place=models.CharField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return self.name


    
class Donation_amount(models.Model):
    name =models.CharField(max_length=50)
    idproof=models.IntegerField()
    email = models.CharField(max_length=100)
    phno= models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)   
    date = models.CharField(max_length=100)

class Pay(models.Model):
    phno= models.CharField(max_length=20)
    idproof=models.IntegerField()
    email = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)   
    date = models.CharField(max_length=100)

class Vaccinations(models.Model):
    dog = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccine")
    muncipality_name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    batchnumber = models.CharField(max_length=100)
    due = models.CharField(max_length=100)
    veterinarian =models.ImageField(upload_to='veterinarian', blank=True, null=True)

class Dog_feddback(models.Model):
    dogname = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dog_image/',)
    feedback_text = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)