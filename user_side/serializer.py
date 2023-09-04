from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate





User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.is_active = True
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = User
        fields = '__all__'

  
class PaymentResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    payment_order_id = serializers.CharField()
    is_staff = serializers.BooleanField()
        
class NewsSerializer(serializers.ModelSerializer):
    photo1 = serializers.ImageField(max_length=None, use_url=True)
    photo2 = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = News
        fields = '__all__'
        
class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class TrendNewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trending_News
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subcategory
        fields = '__all__'
        
                
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


        
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)

class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = '__all__'
        
class User_NewsListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.cat_name', read_only=True)
    
    class Meta:
        model = News
        fields = '__all__'  # Include all fields, including category_name

        
class User_TrendnewsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trending_News
        fields= '__all__'
        
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
        
class WalletTransactionSerializer(serializers.ModelSerializer):
    senders = serializers.SerializerMethodField()
    receivers = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = ('sender', 'receiver', 'amount', 'transaction_date', 'senders', 'receivers')

    def get_senders(self, obj):
        # Customize the serialized representation of the sender field
        return UserSerializer(obj.sender).data

    def get_receivers(self, obj):
        # Customize the serialized representation of the receiver field
        return UserSerializer(obj.receiver).data

        




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

        
class CommantSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ('id', 'user', 'text', 'time','news', 'user_profile_image', 'user_username')

    def get_user_profile_image(self, comment):
        return comment.user.profile_image.url if comment.user.profile_image else None

    def get_user_username(self, comment):
        return comment.user.username
    

class FollowSerializer(serializers.ModelSerializer):
    followed_user_username = serializers.ReadOnlyField(source='followed_user.username',read_only=True)
    followed_user_profile_photo = serializers.ImageField(source='followed_user.profile_image', read_only=True)
    following_user_username = serializers.ReadOnlyField(source='following_user.username',read_only=True)
    following_user_profile_photo = serializers.ImageField(source='following_user.profile_image', read_only=True)
    following_user_email = serializers.ReadOnlyField(source='following_user.email',read_only=True)
    
    
    class Meta:
        model = Follow
        fields = "__all__"
        
    
        
class SubcategorySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Subcategory
        fields = '__all__'
        
                
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class admin_dashboardserilizer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = Sub_Payment
        fields = '__all__'
        
    def get_user_details(self, obj):
        user = obj.user  # Assuming Sub_Payment has a ForeignKey to User
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            
            # Add more fields as needed
        }
        
        
class staff_pay_dashbord_serilizer(serializers.ModelSerializer):
    class Meta:
        model =Sub_Payment
        fields = '__all__'
        
        
        

