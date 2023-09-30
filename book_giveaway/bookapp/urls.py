from django.urls import path
from .views import UserRegistration, ExpressInterest, OwnershipDecision

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def swagger_info(request):
    schema_view = get_schema_view(
        openapi.Info(
            title="Your API",
            default_version='v1',
            description="Your API description",
            terms_of_service="https://www.example.com/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="Your License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    return schema_view(request)



router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('', include(router.urls)),
    path('express-interest/<int:book_id>/', ExpressInterest.as_view(), name='express-interest'),
    path('ownership-decision/<int:book_id>/', OwnershipDecision.as_view(), name='ownership-decision'),
    path('swagger/', swagger_info),
]
