from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.safestring import mark_safe
from autoslug import AutoSlugField


class SkinUser(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField('Gender', max_length=20, choices=GENDER_CHOICES)
    profile_image = models.ImageField('Profile image', upload_to='users_profile/', blank=True, null=True)
    address = models.CharField('Address', max_length=200, blank=True)
    country = models.CharField('Country', max_length=200, blank=True)
    city = models.CharField('City', max_length=200, blank=True)
    contact = models.CharField('Contact', max_length=20)
    status = models.BooleanField('Status',default=True)
    
    def profile_img(self):
        try:
            return mark_safe(f'<img src="{self.profile_image.url}" style="border-radius: 50%;" width="40px" height="40px" />')
        except:
            default_image_url = 'media/user.png'
            return mark_safe(f'<img src="{default_image_url}" style="border-radius: 50%;" width="40px" height="40px" />')
    
  
    def __str__(self):
        return self.user.username
    

class SkinData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skin_image = models.ImageField('Skin image', upload_to='skin_images/', blank=True, null=True)
    is_benign = models.BooleanField(default=False)
    is_malignant = models.BooleanField(default=False)
    status = models.BooleanField('Status',default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def skin_img(self):
        return mark_safe(f'<img src="{self.skin_image.url}" style="border-radius: 50%;" width="40px" height="40px" />')
    
    def user_img(self):
        try:
            return mark_safe(f'<img src="{self.user.skinuser.profile_image.url}" style="border-radius: 50%;" width="40px" height="40px" />')
        except:
            default_image_url = 'media/user.png'
            return mark_safe(f'<img src="{default_image_url}" style="border-radius: 50%;" width="40px" height="40px" />')
        
    def __str__(self):
        return str(self.user.username)


class PredictiveModel(models.Model):
    model_name = models.CharField(max_length=200, blank=False)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.model_name)
    
    