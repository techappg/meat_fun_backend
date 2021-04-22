from django.urls import path
from rest_framework import routers

from rocapi.api.admin_api import UserAPIView, User_View
from rocapi.api.admin_profile_update_api import adminProfileUpdateApi
from rocapi.api.login_token_api import LoginView
from rocapi.api.admin_register_api import adminVerifyEmailOtpRegisterApi
from rocapi.api.send_admin_otp_email import adminSendOTPEmailApi
from rocapi.api.send_otp_email_api import SendOTPEmailApi
from rocapi.api.admin_login_api import adminLoginView
from rocapi.api.admin_logout_api import LogoutApi
from rocapi.api.admin_reset_password_api import admin_reset_passwordApi
from rocapi.api.admin_change_password_api import ChangePasswordView
from django.urls import include, path

urlpatterns = [
    path('login/', LoginView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'users', UserAPIView)

urlpatterns=[
	path('admin-register/', adminVerifyEmailOtpRegisterApi.as_view()),
    path('admin-login/', adminLoginView.as_view()),
    path('admin-logout/', LogoutApi.as_view()),
    path('admin-change-password/', ChangePasswordView.as_view()),
    path('send-email-otp/', SendOTPEmailApi.as_view()),
    path('reset-password/', admin_reset_passwordApi.as_view()),
    path('admin-profile/', adminProfileUpdateApi.as_view()),
    path('admin-otp/', adminSendOTPEmailApi.as_view()),
    path('User-list-data/', User_View.as_view()),

]+router.urls
