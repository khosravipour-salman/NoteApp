from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from note.models import Note, Category
from note.forms import NoteForm
from note.helper_functions import get_queryset_fields


def home(request):
	if not request.session.get('search_result'):
		queryset = Note.objects.all().order_by('-create')
	else:
		queryset = request.session.get('search_result')

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
			return redirect('note:detail')

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
			return redirect('note:detail')

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


def search(request):
	search_text = request.GET.get('search_text', '')
	search_field = request.GET.get('search_in', 'all')
	search_dict = get_queryset_fields(search_field, search_text)

	q_obj_list = [Q(**{search_dict[key]: key}) for key, value in search_dict.items()]
	
	res = Note.objects.filter(
		*q_obj_list
	)

	default_start_date = request.user.date_joined
	default_end_date = timezone.datetime.today() + timezone.timedelta(days=1)

	start_date = request.GET.get('from') if request.GET.get('from') else default_start_date
	end_date = request.GET.get('to') if request.GET.get('to') else default_end_date
	
	res = res.filter(create__range=[start_date, end_date]).distinct().order_by('-create')	
	serialized_result = [obj for obj in res]
	request.session["search_result"] = serialized_result

	return redirect('note:home')


def detail(request, note_slug):
	obj = get_object_or_404(Note, slug=note_slug)
	return render(request, 'note/detail.html', {'obj': obj})


def edit(request, note_slug):
	instance_obj = get_object_or_404(Note, slug=note_slug)

	form = NoteForm(instance=instance_obj)
	if request.method == 'POST':
		form = NoteForm(request.POST, instance=instance_obj)
		if form.is_valid():
			form.save()
			return redirect(reverse('note:detail', kwargs={'note_slug': note_slug}))

	context = {
		'form': form,
	}
	return render(request, 'note/create.html', context)
