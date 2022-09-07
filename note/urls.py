from django.urls import path
from note import views


app_name = 'note'

urlpatterns = [
	path('home/', views.home, name='home'),
	path('search/', views.search, name='search'),
	
	path('create-note/', views.create_note, name='create_note'),	
	path('create-note/inherit/', views.create_note_with_inheritance, name='create_note_with_inheritance'),
	
	path('delete/bulk/', views.bulk_delete, name='bulk_delete'),
]