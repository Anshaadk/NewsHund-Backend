from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .utilites import genarate_otp
from .serializer import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions 

import razorpay
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import User
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from razorpay import Client
from .models import *
    

class SignUpView(APIView):
    def post(self, request):
        print(request.data['email'],"------------------------in-------------------------")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Check if email already exists
            user = serializer.save()
            print(user,'---------------------------------------user----------------------------------')

            response_data = {
                'message': 'User registered successfully',
                'user_id': user.id,
                'email': user.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendOtpView(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            return Response({'message': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)
        otp = genarate_otp(request.data['email'],request.data['name'])
        if otp:
            return Response(otp, status=status.HTTP_201_CREATED)
        elif not otp:
            return Response({'message': 'Email is Not Found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)


class AuthView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['access']
        response.data['token'] = token
        response.data.pop('access', None)
        response.data.pop('refresh', None)
        email = request.data.get('email')
        user = User.objects.get(email=email)
        
        response.data['user'] = {
            "username" : str(user.username),
            "email" : str(user.email) ,
            "is_staffs":bool(user.is_staffs),
            "is_admin":bool(user.is_admin),
            "is_staff":bool(user.is_staff),
            'userID':int(user.id),
            'phone': (user.phone),         
                 
            
            
        }
        return response
 




class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer  # Use your ProfileSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, User.DoesNotExist):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)





class NewsCreateView(generics.CreateAPIView):

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [IsAuthenticated]  # Requires authentication for creating news

 
    

class NewsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
    # permission_classes = [IsAuthenticated]  # Requires authentication for retrieving, updating, and deleting news

class NewsUpdateView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [IsAuthenticated]  # Requires authentication for updating news

class NewsBlockView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [IsAuthenticated]  # Requires authentication for blocking news
    
    
from django.http import Http404

class NewsListByUserView(generics.ListAPIView):
    serializer_class = NewsSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('id')
        if user_id is None:
            raise Http404('User ID parameter is required.')

        try:
            user_id = int(user_id)
        except ValueError:
            raise Http404('Invalid user ID.')

        return News.objects.filter(user_id=user_id)
    

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class CategoryListViews(generics.RetrieveAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class SubcategoryListView(APIView):
    def get(self, request):
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)

class SubcategoryListViews(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class=SubcategorySerializer


class SubscriptionView(APIView):
    def post(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
       
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the subscription plan from the request data
        plan = request.data.get('plan')
        payment=request.data.get('paymentId')
        print(payment)
        print(plan)
       
        # )
        if not plan:
            return Response({"error": "Subscription plan is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Subscription plan durations in days
        durations = {
            'monthly': 30,
            'six_months': 30 * 6,
            'yearly': 30 * 12,
        }
        if plan == 'monthly':
            
            m=199
        elif plan =='six_months':
            
            m=499
        elif plan =='yearly':
            
            m=899
        
        
        
        pay=Sub_Payment.objects.create(
            user=user,plan=str(plan),amount=m
        )
        pay.save()
    
        print('_____workaye___annnnn______')
        
        # Check if the plan is valid and set the subscription_expiration accordingly
        if plan in durations:
            user.subscription_expiration = timezone.now() + timezone.timedelta(days=durations[plan])
        else:
            return Response({"error": "Invalid subscription plan."}, status=status.HTTP_400_BAD_REQUEST)

        # # Set is_staff to True for all subscription plans
        user.is_staffs = True

        # # Save the user instance
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)




@csrf_exempt  # This decorator is used to exempt CSRF protection for this view (for testing purposes only)
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_plan = data.get('plan')

        # Initialize Razorpay client with your API keys
        razorpay_client = Client(auth=('rzp_test_aCOPLFUFmC265M', 'xOMWffWBSmuJi5y06YT3aq4N'))

        try:
            # Create a new order with Razorpay
            
            print(selected_plan,'___________ugftrere45e4________')
            k=None
            if selected_plan == 'monthly':
                k=199
            elif selected_plan =='six_months':
                k=499
            elif selected_plan == 'yearly':
                k=899
            print(k,'________kjugyug')
            response = razorpay_client.order.create(dict(amount=k * 100, currency='INR', payment_capture=1))

            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


class Trend_NewsCreateView(generics.CreateAPIView):
    queryset = Trending_News.objects.all()
    serializer_class = TrendNewsSerializer

# Retrieve a specific trending news entry
class Trend_NewsRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trending_News.objects.all()
    serializer_class = TrendNewsSerializer


# Update an existing trending news entry
class Trend_NewsUpdateView(generics.UpdateAPIView):
    
    queryset = Trending_News.objects.all()
    serializer_class = TrendNewsSerializer
    # permission_classes = [IsAuthenticated]  # Requires authentication for retrieving, updating, and deleting news
    
    
    

# List all trending news entries
class Trend_NewsListView(generics.ListAPIView):
    serializer_class = TrendNewsSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('id')
        if user_id is None:
            raise Http404('User ID parameter is required.')

        try:
            user_id = int(user_id)
        except ValueError:
            raise Http404('Invalid user ID.')

        return Trending_News.objects.filter(user_id=user_id)
    

import bcrypt 
 
class UserProfileView(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # Don't forget to import get_object_or_404
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.contrib.auth.hashers import make_password

class ChangePasswordView(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
        confirm_new_password = request.data.get('confirm_new_password', '')

        # Check if the current password matches the user's password
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the new password and confirm new password match
        if new_password != confirm_new_password:
            return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password with the new password
        user.password = make_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

class WalletListCreateView(ListCreateAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Wallet.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        k=request.data.get('balance')
        print(k)
        k=int(k)
        amount = request.data.get('balance', 0)
        amount=int(amount)
        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user's wallet or create a new one if it doesn't exist
        user_wallet, created = Wallet.objects.get_or_create(user=user)

        # If the wallet is created or balance is not set, set the balance to the provided amount
        if created or user_wallet.balance is None:
            user_wallet.balance = amount
        else:
            # If the wallet already exists and balance is set, add the amount to the existing balance
            user_wallet.balance += amount

        user_wallet.save()

        serializer = self.get_serializer(user_wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class WalletDetailAPIView(RetrieveAPIView):
    serializer_class = WalletDetailSerializer

    def get_object(self):
        # Get the user ID from the URL
        user_id = self.kwargs['pk']

        # Filter the queryset based on the user ID
        queryset = Wallet.objects.filter(user_id=user_id)

        # Retrieve the wallet object or return a 404 response if not found
        wallet = get_object_or_404(queryset)
        return wallet
    
class WalletTransactionListCreateView(ListCreateAPIView):
    serializer_class = WalletTransactionSerializer

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']  # Get the user PK from the URL
        return WalletTransaction.objects.filter(sender_id=user_pk) | WalletTransaction.objects.filter(receiver_id=user_pk)


class User_NewsListing(generics.ListAPIView):
    queryset=News.objects.all()
    serializer_class=User_NewsListSerializer
    
class User_NewsSigleListing(generics.RetrieveAPIView):
    queryset=News.objects.all()
    serializer_class=User_NewsListSerializer
    
class User_TrendnewsListing(generics.ListAPIView):
    queryset=Trending_News.objects.all()
    serializer_class=User_TrendnewsSerializer



class PurchaseCreateView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer



class PurchaseListView(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    
class PurchaseListViews(generics.ListAPIView):
    serializer_class = PurchaseSerializer  # Add the serializer_class attribute

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Purchase.objects.filter(user_id=user_id)
 
from rest_framework import viewsets

class WalletTransactionViewSet(viewsets.ModelViewSet):
    queryset = WalletTransaction.objects.all()
    serializer_class = WalletTransactionSerializer
    
@csrf_exempt  # This decorator is used to exempt CSRF protection for this view (for testing purposes only)
def topupcreate_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('topUpAmount')
        print(amount)

        # Initialize Razorpay client with your API keys
        razorpay_client = Client(auth=('rzp_test_aCOPLFUFmC265M', 'xOMWffWBSmuJi5y06YT3aq4N'))

        try:
            # Create a new order with Razorpay
            
            print(amount,'___________ugftrere45e4________')
           
            response = razorpay_client.order.create(dict(amount=amount * 100, currency='INR', payment_capture=1))

            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


class UserListing(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=ProfileSerializer
    # permission_classes = [IsAuthenticated] 
    

#chat 


class ChatRoomAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        other_user = get_object_or_404(User, id=room_name)
        room = Room.objects.filter(users=other_user)

        if room.exists():
            return Message.objects.filter(room=room.first()).order_by('timestamp')

        return Message.objects.none()

    def perform_create(self, serializer):
        room_name = self.kwargs['room_name']
        other_user = get_object_or_404(User, username=room_name)
        room = Room.objects.filter(users=other_user).first()

        if room:
            serializer.save(room=room, sender=None)  # You can set sender as None or handle it differently



# views.py


class FollowView(APIView):
    def get(self, request, user1, user2):
        instance = Follow.objects.filter(
            following_user_id=user1, followed_user_id=user2
        )
        is_followed = True if instance.exists() else False
        
        status_code = 200 if is_followed else 404
        print('status == ',status_code)
        return Response(data={"is_followed": is_followed}, status=status_code)

    def post(self, request, user1, user2):
        try:
            following_user = User.objects.get(id=user1)
            followed_user = User.objects.get(id=user2)
            Follow.objects.create(
                following_user=following_user, followed_user=followed_user
            )
        except:
            return Response(status=400)
        return Response(status=201)

    def delete(self, request, user1, user2):
        instance = Follow.objects.filter(
            following_user_id=user1, followed_user_id=user2
        )
        if instance.exists():
            instance.delete()
            return Response(status=204)


##notification

class NotificationDetailAPIView(APIView):
   
    def get_object(self, pk):
        try:
            return Notification.objects.filter(user=pk).order_by('-time')
        except Notification.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        notifications = self.get_object(pk)
        if notifications is not None:
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        notifications = self.get_object(pk)
        if notifications is not None:
            notifications.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


from .models import Comments
from rest_framework.decorators import action

class NewsCommants(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommantSerializer

    # Custom action to handle commenting on a specific use
    
class CommentListView(generics.ListAPIView):
    serializer_class = CommantSerializer

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        news = get_object_or_404(News, id=news_id)
        queryset = Comments.objects.filter(news=news)
        return queryset
    
    
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(following_user_id=user_id)

class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(followed_user_id=user_id)
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializers
    
    
class admin_dashboard(generics.ListAPIView):
    queryset=Sub_Payment.objects.all()
    serializer_class = admin_dashboardserilizer
    
class staff_paymentdashboard(generics.ListAPIView):
    serializer_class = staff_pay_dashbord_serilizer
    
    def get_queryset(self):
        user = self.kwargs['pk']
        queryset =Sub_Payment.objects.filter(user=user)
        return queryset
    
class Staff_Earning_wallet_dashboard(generics.ListAPIView):
    serializer_class = WalletTransactionSerializer
    
    def get_queryset(self):
        user = self.kwargs['pk']
        queryset =WalletTransaction.objects.filter(receiver=user)
        return queryset