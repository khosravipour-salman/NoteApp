from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import Http404

from datetime import datetime

from note.models import Note, Category
from note.forms import NoteForm, CategoryForm
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


def delete(request, note_slug):
	obj = get_object_or_404(Note, slug=note_slug)
	if request.method == 'POST':
		obj.delete()
		return redirect('note:home')

	return render(request, 'snippets/delete_confirm.html', {'obj': obj})


def note_categories(request, note_slug):
	obj = get_object_or_404(Note, slug=note_slug)
	obj_categories = obj.categories.all()
	category_object_list = Category.objects.all()	

	form = CategoryForm(initial={'add': obj.slug})

	context = {
		'obj': obj,
		'obj_categories': obj_categories,
		'category_list': category_object_list,
		'form': form,
	}
	return render(request, 'note/category_list.html', context)


def remove_category_from_note(request, note_slug, category_id):
	note_obj = get_object_or_404(Note, slug=note_slug)
	category_obj = get_object_or_404(Category, id=category_id)

	note_obj.categories.remove(category_obj)
	return redirect(request.META.get('HTTP_REFERER'))


def add_category_list_to_note(request, note_slug):
	note_obj = get_object_or_404(Note, slug=note_slug)

	if request.method == 'POST':
		categories = request.POST.getlist('categories', None)
		obj_list = [get_object_or_404(Category, id=category_id) for category_id in categories]
		note_obj.categories.add(*obj_list)
			
	return redirect(request.META.get('HTTP_REFERER'))


def create_category(request, note_slug):
	if request.method == 'GET':
		raise Http404

	form = CategoryForm(request.POST)
		
	if form.is_valid():
		form.save(note_slug=note_slug)
		return redirect(reverse('note:detail', kwargs={'note_slug': note_slug}))
		
	else:
		return render(request.META.get('HTTP_REFERER'))