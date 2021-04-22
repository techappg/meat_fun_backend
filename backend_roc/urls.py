from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from oauth2_provider.views import AuthorizationView
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

from rocapi.api.logout_api import LogoutApi
from rocapi.api.send_otp_email_api import SendOTPEmailApi
from rocapi.api.send_otp_sms_api import SendOTPSMSApi
from rocapi.api.social_auth_api import SocialConvertTokenView
from rocapi.api.user_profile_update_api import UserProfileUpdateApi
from rocapi.api.verify_email_otp_login_api import VerifyEmailOtpLoginApi
from rocapi.api.verify_email_otp_register_api import VerifyEmailOtpRegisterApi
from rocapi.api.verify_otp_only import VerifyMobileOnlyOtpLoginApi
from rocapi.api.verify_otp_sms_login_api import VerifyOTPSMSLoginApi
from rocapi.api.verify_otp_sms_register_api import VerifyOtpSMSRegisterApi
from django.conf import settings
from django.conf.urls.static import static
from rocapi.api.check_email_sent_before_otp_api import checkSendOTPEmailApi

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='ROC Backend', permission_classes=[AllowAny])),
]

urlpatterns += [
    path('google-auth/convert-token/', SocialConvertTokenView.as_view(), name='auth_create'),
    url(r"google-auth/", include("social_django.urls", namespace="social")),
    url(r"fb-auth/authorize/?$", AuthorizationView.as_view(), name="authorize"),
]

urlpatterns += [
    path('users/verify-email-otp-register/', VerifyEmailOtpRegisterApi.as_view()),
    path('users/verify-email-otp-login/', VerifyEmailOtpLoginApi.as_view()),
    path('users/send-otp-email/', SendOTPEmailApi.as_view()),
    path('users/send-otp-sms/', SendOTPSMSApi.as_view()),
    path('users/verify-otp-sms-login/', VerifyOTPSMSLoginApi.as_view()),
    path('users/verify-otp-sms-register/', VerifyOtpSMSRegisterApi.as_view()),
    path('users/profile-update/', UserProfileUpdateApi.as_view()),
    path('users/logout/', LogoutApi.as_view()),
    path('users/check-email-before-send-OTP/', checkSendOTPEmailApi.as_view()),
    path('users/verify-mobile-otp', VerifyMobileOnlyOtpLoginApi.as_view()),

    path('administrator/', include('rocapi.urls')),
    path('product/', include('product.urls')),
    path('blog/', include('blog.urls')),
    path('store-header-images/', include('storeheaderimages.urls')),
    path('feedback/', include('feedback.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




