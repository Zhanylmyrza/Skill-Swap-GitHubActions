from django.conf import settings
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

# from accounts.views import CustomTokenObtainPairView
# from accounts.views import CustomUserCreateAPIView


urlpatterns = [
    # re_path(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    # path("auth/jwt/create/", CustomUserCreateAPIView.as_view(), name="user-create"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls")),
    path("person/", include("accounts.urls")),
    path("media/<path:path>", serve, kwargs={"document_root": settings.MEDIA_ROOT}),
    path("chat/", include("chat.urls")),
]


urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name="index.html"))]
