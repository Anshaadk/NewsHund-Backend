from django.contrib import admin
from .models import *
from django import forms

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(News)
admin.site.register(StaffUser)
admin.site.register(Follow)
admin.site.register(Notification)

admin.site.register(Purchase)
admin.site.register(WalletTransaction)
admin.site.register(Wallet)
admin.site.register(Sub_Payment)
admin.site.register(Trending_News)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(Rating)