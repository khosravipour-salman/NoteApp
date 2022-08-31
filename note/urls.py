from django.urls import path
from note import views


urlpatterns = [
	path('home/', views.home, name='home'),
	path('create_note/', views.create_note, name='create_note'),	
	path('create_note/inherit/', views.create_note_with_inheritance, name='create_note_with_inheritance'),
]