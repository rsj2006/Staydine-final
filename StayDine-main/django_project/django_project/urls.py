
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.account.views import EmailView
from django.contrib.auth.decorators import user_passes_test


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('change-password/', user_views.change_password, name='change_password'),
    path('accounts/email/', user_views.email_redirect_view, name='account_email_redirect'),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/login/', OAuth2LoginView.as_view(), name='google_login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('logout/', user_views.logout_view, name='logout'),
    path('', include('staydine.urls')),
    path('payment/', include('users.urls')),
    path('delete_account/', user_views.delete_account, name='delete_account'),
    # path('verify-payment/', verify_payment, name='verify_payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)