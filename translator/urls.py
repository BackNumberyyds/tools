from django.urls import path
from translator import views

urlpatterns = [
    path('<slug:word>/', views.index, name='index'),
]
