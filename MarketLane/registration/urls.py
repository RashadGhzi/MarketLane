from django.urls import path
from registration import views

urlpatterns = [
    path('user/registration/', views.RegistrationView.as_view(), name='user_registration'),
    path('user/login/', views.LogInView.as_view(), name="user_login"),
    path('user/logout/', views.LogOutView.as_view(), name='user_logout'),
    path('password/reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
