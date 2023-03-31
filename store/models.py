from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

# Create your models here.
class category(models.Model):
    title=models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)

    def __str__(self):
        return self.title



class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELECTED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT,'Draft'),
        (WAITING_APPROVAL,'Waitingaprroval'),
        (ACTIVE,'Active'),
        (DELECTED,'Delected'),
    )

    user= models.ForeignKey(User,related_name='products',on_delete=models.CASCADE)
    category=models.ForeignKey(category,related_name='products',on_delete=models.CASCADE)
    title= models.CharField(max_length=50)
    slug= models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price= models.IntegerField()
    image = models.ImageField(upload_to='uploads/product_images/',blank=True,null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_image/thumbnail/',blank =True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,default=ACTIVE)


    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price/ 100

    class Meta:
        ordering =('-created_at',)
#MAKING tHUMBUNAILS
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumnbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://photographylife.com/wp-content/uploads/2018/11/Moeraki-Boulders-New-Zealand.jpg'

    def make_thumnbnail(self,image,size=(300,300)):
        img = Image.open(image)
        img.thumbnail(size)
        thumb_io = BytesIO()
        if img.mode == "JPEG":
            img.save(thumb_io, format='JPEG',quality=85)
        elif img.mode in ['RGBA',"P"]:
            img= img.convert("RGB")
        name= image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io,name=name)

        return thumbnail
    

class Order(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    address= models.CharField(max_length=255)
    email  = models.EmailField()
    city = models.CharField(max_length=255,default=False)
    zip_code = models.CharField(max_length=225)
    phone_contact = models.IntegerField()
    paid_amount= models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default= False)
    payment_intent =models.CharField(max_length=255)
    created_by = models.ForeignKey(User,related_name='orders', on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


   

class OrderItem(models.Model):
    order  = models.ForeignKey(Order,related_name='items',on_delete = models.CASCADE)
    product = models.ForeignKey(Product,related_name='items',on_delete = models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def get_display_price(self):
        return self.price/ 100

    







    
    





