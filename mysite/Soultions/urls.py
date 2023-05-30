from django.urls import include, path
from . import views

urlpatterns = [
path('', views.main , name='main'),
path('slove',views.sloved,name = "sloved")
]
