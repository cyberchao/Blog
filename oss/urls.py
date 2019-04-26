
from django.urls import path
from .views import tem

urlpatterns = [
    path('', tem, name='tem'),
]

