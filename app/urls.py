from django.urls import path
from . import views

urlpatterns = [
    # Frontend pages
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('chat/', views.chat_page, name='chat'),
    
    # API endpoints
    path('api/signup/', views.signup_api, name='signup_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/user/', views.current_user_api, name='current_user_api'),
    path('api/conversations/', views.conversations_api, name='conversations_api'),
    path('api/conversations/<int:conversation_id>/', views.conversation_detail_api, name='conversation_detail_api'),
    path('api/conversations/<int:conversation_id>/messages/', views.send_message_api, name='send_message_api'),
]

