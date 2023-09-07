from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone



# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser field is_active must be true')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser field is_staff must be true')
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser field is_admin must be True')
        
        return self.create_user(email=email, password=password, **extra_fields)




class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    username = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.PositiveBigIntegerField(null=True, validators=[phone_regex])
    profile_image = models.ImageField(upload_to='uploads', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_staffs = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    followers_count=models.PositiveIntegerField(default=0)
    following_count=models.PositiveIntegerField(default=0)
    
    subscription_expiration = models.DateTimeField(null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def is_subscription_active(self):
        if self.subscription_expiration:
            return self.subscription_expiration >= timezone.now()
        return False

    def save(self, *args, **kwargs):
        if self.subscription_expiration and self.subscription_expiration < timezone.now():
            self.is_staffs = False  # Set is_staff to False when subscription is expired
        else:
            self.is_staffs = self.is_subscription_active()  # Set is_staff to True if subscription is active
        super().save(*args, **kwargs)
        
        if not hasattr(self, 'wallet'):
            # Create a new wallet for the user
            Wallet.objects.create(user=self, balance=0)
        
        
class Category(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=50)

    class Meta:
        unique_together = ('category', 'sub_category')

    def __str__(self):
        return self.sub_category

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.db.models import Avg

class News(models.Model):
    CHOOSE = (
        ('Free', 'Free'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('30', '30'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    photo1 = models.ImageField(upload_to='uploads')
    photo2 = models.ImageField(upload_to='uploads')
    short_details = models.CharField(max_length=100)
    full_description = models.CharField(max_length=999)
    plan = models.CharField(choices=CHOOSE, max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    Date=models.DateTimeField(auto_now_add=True)
    view_count = models.BigIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_ratings = models.PositiveIntegerField(default=0)

    


    
    def crop_image(self, image_field_name, aspect_ratio=(14.5, 9)):
        img = Image.open(getattr(self, image_field_name))

        # Calculate the desired width and height based on the aspect ratio
        width, height = img.size
        target_width = height * aspect_ratio[0] // aspect_ratio[1]
        target_height = height

        # Calculate the cropping box coordinates
        left = (width - target_width) // 2
        top = 0
        right = left + target_width
        bottom = target_height

        # Perform the cropping
        cropped_img = img.crop((left, top, right, bottom))

        # Save the cropped image back to the model field
        output_buffer = BytesIO()
        cropped_img.save(output_buffer, format='JPEG')
        setattr(self, image_field_name, InMemoryUploadedFile(
            output_buffer,
            None,
            f"{image_field_name}.jpg",
            'image/jpeg',
            cropped_img.tell,
            None
        ))

    def save(self, *args, **kwargs):
        self.crop_image('photo1')
        self.crop_image('photo2')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.subject



from django_cleanup import cleanup
from django.db import models
from django.utils import timezone

#banner News

class Trending_News(models.Model):
    user = models.ForeignKey('user_side.User', on_delete=models.CASCADE)
    photo1 = models.ImageField(upload_to='uploads')
    
    short_banner = models.CharField(max_length=50)
    description = models.CharField(max_length=999)
    date = models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        # Calculate the expiration date (one week from creation)
        expiration_date = self.date + timezone.timedelta(days=2)

        # If the current date is greater than the expiration date, delete the instance
        if timezone.now() >= expiration_date:
            self.delete()
            return

        super().save(*args, **kwargs)

    def crop_image(self, image_field_name, aspect_ratio=(14.5, 9)):
        img = Image.open(getattr(self, image_field_name))

        # Calculate the desired width and height based on the aspect ratio
        width, height = img.size
        target_width = height * aspect_ratio[0] // aspect_ratio[1]
        target_height = height

        # Calculate the cropping box coordinates
        left = (width - target_width) // 2
        top = 0
        right = left + target_width
        bottom = target_height

        # Perform the cropping
        cropped_img = img.crop((left, top, right, bottom))

        # Save the cropped image back to the model field
        output_buffer = BytesIO()
        cropped_img.save(output_buffer, format='JPEG')
        setattr(self, image_field_name, InMemoryUploadedFile(
            output_buffer,
            None,
            f"{image_field_name}.jpg",
            'image/jpeg',
            cropped_img.tell,
            None
        ))
    def save(self, *args, **kwargs):
        self.crop_image('photo1')
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.subject

class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Add any additional fields specific to staff users here

    def __str__(self):
        return self.user.email





class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)  # Link the purchase to the News
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically deduct the amount from the user's wallet balance on purchase
        if self.user.is_staff:
            amount = int(self.news.plan)  # Extract the numeric part of the plan (e.g., 10 from '10rs')
            user_wallet = Wallet.objects.get(user=self.user)
            user_wallet.balance -= amount
            user_wallet.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email} purchased {self.news}'

# wallet

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)  # Set a default value of 0 for the balance field

    def __str__(self):
        return f"Wallet for {self.user.email}"


class WalletTransaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        sender_wallet = Wallet.objects.get(user=self.sender)
        receiver_wallet = Wallet.objects.get(user=self.receiver)
        sender_wallet.balance -= self.amount
        receiver_wallet.balance += self.amount
        sender_wallet.save()
        receiver_wallet.save()

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.sender.email} sent {self.amount} to {self.receiver.email}'
    
class Sub_Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)



##chat area
import string
import random


# Create your models here.

def generate_random_string(length):
    random_string = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return random_string

class Room(models.Model):
    token = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_random_string(20)
            
        return super(Room, self).save(*args, **kwargs)
    

class Message(models.Model):
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender_user'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
 
 
 # followers follow   
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver


class Follow(models.Model):
    following_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following_user_set')
    followed_user  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followed_user_set')

    class Meta:
        unique_together = ['following_user', 'followed_user']

    def _str_(self) -> str:
        return f"{self.following_user} followed {self.followed_user}"


    
    
@receiver(post_save, sender=Follow)
def update_follow_counts(sender, instance, created, **kwargs):
    print('etheeeeeeeeeeeee')
    if created:
        print('etheeeeeeeeeeeeeqqqqq')
        followed_user = instance.followed_user
        following_user = instance.following_user

        followed_user.followers_count += 1 
        followed_user.save()

        
        following_user.following_count += 1
        following_user.save()

@receiver(post_delete, sender=Follow)
def update_follow_counts_on_delete(sender, instance, **kwargs):
    print('etheeeeeeeeeeeeeooooooooooooo')
    followed_user = instance.followed_user
    following_user = instance.following_user

    
    followed_user.followers_count -= 1
    followed_user.save()

    
    following_user.following_count -= 1
    following_user.save()
    
## Notification


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(News, on_delete=models.CASCADE)  # Assuming you have a News model
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} at {self.time}"
    


@receiver(post_save, sender=News)
def create_news_notification(sender, instance, created, **kwargs):
    if created:
        author = instance.user
        followers_of_author = Follow.objects.filter(followed_user=author)
        print(followers_of_author,'jhjyhgyufyfty')

        for follower in followers_of_author:
            notification = Notification.objects.create(
                user=follower.following_user,
                message=instance,  # Use the correct field name
            )



#commants

class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    news=models.ForeignKey(News,on_delete=models.CASCADE)
    text = models.CharField( max_length=255)
    time=models.TimeField( auto_now_add=True)
    


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)


    


@receiver(post_save, sender=Rating)
def update_average_rating(sender, instance, **kwargs):
    news_article = instance.news
    ratings = Rating.objects.filter(news=news_article)
    
    # Calculate the average rating for the news article
    if ratings.exists():
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    else:
        average_rating = 0
    
    # Update the news article's average rating and total ratings
    news_article.average_rating = average_rating
    news_article.total_ratings = ratings.count()
    news_article.save()
