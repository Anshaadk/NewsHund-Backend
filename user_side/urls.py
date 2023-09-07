from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'wallet-transactions', WalletTransactionViewSet)
router.register(r'commanting',NewsCommants)
router.register(r'categories_viewset', CategoryViewSet)
router.register(r'subcategories_viewset', SubcategoryViewSet)






urlpatterns = [
    #login register
    path('sendotp/', SendOtpView.as_view(), name='sendotp'),
    path('register/', SignUpView.as_view(), name='register'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('api/token/', AuthView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   
    
    #staff news adding and editing
    path('api/news/', NewsCreateView.as_view(), name='news-create'),  # POST request for creating news
    path('api/news/<int:pk>/', NewsRetrieveUpdateDeleteView.as_view(), name='news-retrieve-update-delete'),  # GET, PUT, PATCH, DELETE requests for a specific news item
    path('api/newsedit/<int:pk>/', NewsUpdateView.as_view(), name='news-edit'),  # PUT and PATCH requests for updating news
    path('api/news/<int:pk>/block/', NewsBlockView.as_view(), name='news-block'),  # DELETE request for blocking news
    path('api/news/user/', NewsListByUserView.as_view(), name='news-list-by-user'),
    
    #category subcategory
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryListViews.as_view(), name='categorys-list'),
    path('api/subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('api/subcategories/<int:pk>/', SubcategoryListViews.as_view(), name='subcategorys-list'),
    
    
    #staff subcribption aria
    path('api/user/<int:user_id>/subscribe/',SubscriptionView.as_view(), name='subscription_api_view'),
    path('api/create_order/', create_order, name='create_order'),
    
    #staff Trend news adding and editing aria
    path('api/trend_news/create/', Trend_NewsCreateView.as_view(), name='trend-news-create'),
    path('api/trend_news/<int:pk>/', Trend_NewsRetrieveView.as_view(), name='trend-news-retrieve'),
    path('api/trend_newsedit/<int:pk>/', Trend_NewsUpdateView.as_view(), name='trend-news-update'),
    path('api/trend_news/', Trend_NewsListView.as_view(), name='trend-news-list'),
    
    #Profile aria edit update change all
    path('api/user-profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('api/change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password'),
    path('api/viewprofile/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/userlisting/',UserListing.as_view(),name='userlisting'),
    
    #wallet aria transation codes
    path('api/walletsadd/<int:user_id>/', WalletListCreateView.as_view(), name='wallet-list-create'),
    path('api/wallets/<int:pk>/', WalletDetailAPIView.as_view(), name='wallet-detail'),
    path('api/transactions/<int:user_pk>/', WalletTransactionListCreateView.as_view(), name='transaction-list-create'),
    path('api/topupcreate_order/', topupcreate_order, name='create_order'),
    
    
    #user News listing
    path('api/user_newslisting/',User_NewsListing.as_view(),name='user-newslisting'),
    path('api/user_newslisting/<int:pk>/',User_NewsSigleListing.as_view(),name='user-newslisting'),
    path('api/user_trendnewslisting/',User_TrendnewsListing.as_view(),name='user-trendnewslisting'),
    
    #payment listing
    # path('api/purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('api/purchases/create/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('api/purchases/<int:user_id>/', PurchaseListViews.as_view(), name='purchases-list'),
    path('api/', include(router.urls)),
    
    
    #chat api 
    path('api/chat/<str:room_name>/', ChatRoomAPIView.as_view(), name='chat-room-api'),


    #follow and unfollow
    path("follow/<int:user1>/<int:user2>/", FollowView.as_view()),
    path('followings/<int:user_id>/', FollowingListView.as_view(), name='following-list'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='followers-list'),
    
    #notification
    path('api/notification/<int:pk>/', NotificationDetailAPIView.as_view()),
    
    #news commanting
    
    path('api/comments/<int:news_id>/', CommentListView.as_view(), name='comment-list'),
    
    #dashboards
    
    path('api/admin_dashboard1/',admin_dashboard.as_view(),name='admin_dashboard'),
    path('api/staff_paymentdashbord/<int:pk>/',staff_paymentdashboard.as_view()),
    path('api/staff_newsearnning_dashboard/<int:pk>/',Staff_Earning_wallet_dashboard.as_view()),
    
    
    #rating
    path('api/ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('api/ratings/<int:user_id>/', RatingUserList.as_view(), name='rating-create'),
    path('api/ratingslist/', RatingListing.as_view(), name='rating-create'),
    
    #block ublock
    # path('api/users/', UserListView.as_view(), name='user-list'),
    # path('api/block-user/', BlockUserView.as_view(), name='block-user'),
    # path('api/unblock-user/', UnblockUserView.as_view(), name='unblock-user')
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

