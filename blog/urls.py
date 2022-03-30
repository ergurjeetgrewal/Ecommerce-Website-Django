from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="BlogHome"),
    path('Blogpost/<int:id>', views.Blogpost,name="Blogpost")
]
