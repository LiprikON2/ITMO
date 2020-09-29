from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
# from django.conf.urls import url

from .views import RegisterView, activate

app_name = 'accounts'

urlpatterns = [
    # url(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {"next_page": reverse_lazy('accounts:login')}, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
