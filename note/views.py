from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from note.models import Note, Category
from note.forms import NoteForm


def home(request):
	queryset = Note.objects.all().order_by('-create')
	object_per_page_limit = request.GET.get('object_per_page_limit', 6) 
	p = Paginator(queryset, object_per_page_limit)
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


def create_note(request):
	form = NoteForm()

	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('note:home')

	context = {
		'form': form,
	}
	return render(request, 'note/create.html', context)


def create_note_with_inheritance(request):
	instance_title = request.GET.get('instance', None)
	instance_obj = get_object_or_404(Note, title=instance_title)

	form = NoteForm(initial={'title': instance_obj.title, 'content': instance_obj.content})
	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('note:home')

	context = {
		'form': form,
	}
	return render(request, 'note/create.html', context)


def bulk_delete(request):
	obj_list = [
		value 
		for name, value in request.GET.items()
		if name.startswith('bd---')
	]
	for obj in obj_list:
		Note.objects.get(title=obj).delete()
	
	return redirect('note:home')
