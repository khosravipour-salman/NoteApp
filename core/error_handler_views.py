from django.shortcuts import render


def custom_handler404(request, exception=None):
	return render(request, 'error_handlers/404.html')


def custom_handler500(request, exception=None):
	return render(request, 'error_handlers/500.html')