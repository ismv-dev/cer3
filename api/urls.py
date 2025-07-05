from rest_framework import routers
from django.urls import path, include
from .views import TallerViewSet

router = routers.DefaultRouter()
router.register('Talleres',TallerViewSet)

urlpatterns =[
    path('',include(router.urls), name='apiTalleres')
]