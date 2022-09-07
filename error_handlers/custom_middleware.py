from django.shortcuts import redirect
from django.urls import reverse


class DevelopmentErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        page_404 = reverse('error_handlers:custom_handler404')
        page_500 = reverse('error_handlers:custom_handler500')
        
        if not request.path == page_404 or request.path == page_500:
            if response.status_code == 404:
                return redirect(page_404)

            elif response.status_code == 500:
                return redirect(page_500)

        return response