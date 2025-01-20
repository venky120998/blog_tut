from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # check if user is authenticated
        if request.user.is_authenticated:
            # list of to restricted path
            restricted_path = [reverse(viewname='my_blog:login'), reverse(viewname='my_blog:register_url')]

            if request.path in restricted_path:
                return redirect(to=reverse(viewname='my_blog:index'))
            
        response = self.get_response(request)
        return response

class RedirectUnAuthenticatedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        restricted_path = [reverse(viewname='my_blog:dashboard')]

        if not request.user.is_authenticated and request.path in restricted_path:
            return redirect(to=reverse(viewname='my_blog:login'))
        
        response = self.get_response(request)
        return response