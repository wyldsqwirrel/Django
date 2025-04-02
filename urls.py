# Django/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mycrm import views as mycrm_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Homepage
    path("", mycrm_views.home, name="home"),

    # Admin Panel
    path("admin/", admin.site.urls),

    # App URLs
    path("mycrm/", include("mycrm.urls", namespace="mycrm")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("recruitment/", include("recruitment.urls", namespace="recruitment")),
    path("productivity/", include("productivity.urls", namespace="productivity")),

    # Authentication URLs (updated to use mycrm.views)
    path("login/", mycrm_views.login, name="login"),
    path("logout/", mycrm_views.logout_view, name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    # Signup
    path("signup/", mycrm_views.signup, name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
