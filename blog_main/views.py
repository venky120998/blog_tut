from django.shortcuts import render

def custom_page_not_found(request, exception):
    return render(request=request, template_name='404.html', status=404)