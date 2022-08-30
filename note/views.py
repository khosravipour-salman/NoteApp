from django.shortcuts import render
from django.core.paginator import Paginator

from note.models import Note, Category


def home(request):
	object_per_page_limit = request.GET.get('object_per_page_limit', 6) 
	p = Paginator(Note.objects.all(), object_per_page_limit)
	page = request.GET.get('page')
	
	try:
		note_list = p.get_page(page)

	except Paginator.PageNotAnInteger:
		note_list = p.start_index()

	except Paginator.EmptyPage:
		note_list = p.end_index()

	context = {
		'note_list': note_list,
		'object_per_page_limit': object_per_page_limit,
	}
	return render(request, 'note/home.html', context)