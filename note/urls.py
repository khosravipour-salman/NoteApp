from django.urls import path
from note import views


urlpatterns = [
	path('home/', views.home, name='home'),
]