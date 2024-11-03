# messaging/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect

def redirect_to_inbox(request):
    return redirect('inbox' if request.user.is_authenticated else 'login')

urlpatterns = [
    # Root URL pattern that redirects to inbox if logged in, otherwise to login
    path('', redirect_to_inbox, name='home'),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='messaging/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # Messaging URLs
    path('inbox/', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
]