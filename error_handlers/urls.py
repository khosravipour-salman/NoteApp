from django.urls import path
from error_handlers import views

app_name = 'error_handlers'

urlpatterns = [
	path('404/', views.custom_handler404, name='custom_handler404'),	
	path('500/', views.custom_handler500, name='custom_handler500'),	
]
