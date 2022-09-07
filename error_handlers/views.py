from django.shortcuts import render
from django.http import HttpResponse


def custom_handler404(request, exception=None):
	return render(request, 'error_handlers/technical_404.html')


def custom_handler500(request, exception=None):
	return render(request, 'error_handlers/technical_500.html')
