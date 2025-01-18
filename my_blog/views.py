from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from my_blog.models import Post, AboutUs
from my_blog.forms import ContactForm
from django.http import Http404
import logging
from django.core.paginator import Paginator

# Create your views here.

# static demo data
#posts = [{'id': 1, 'title': 'Post 1', 'content': 'Content of post 1'},
#         {'id': 2, 'title': 'Post 2', 'content': 'Content of post 2'},
#         {'id': 3, 'title': 'Post 3', 'content': 'Content of post 3'},
#         {'id': 4, 'title': 'Post 4', 'content': 'Content of post 4'},]

def index(request):
    blog_title = "Venky's Blog"
    # getting data from post model
    all_posts = Post.objects.all().order_by("created_at")
    # pagenate
    paginator = Paginator(object_list=all_posts, per_page=5)
    page_no = request.GET.get('page')
    page_object = paginator.get_page(number=page_no)
    return render(request=request, template_name='blog/index.html', context={'blog_title': blog_title, 'page_obj': page_object})

def detail(requset, slug):
    # static data
    #post = next((item for item in posts if item['id'] == int(post_id)), None)
    
    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    #logger = logging.getLogger("TESTING")
    #logger.debug(f"Post variable is {post}")
    return render(request=requset, template_name='blog/details.html', context={'post': post, 'related_posts': related_posts})

def old_url_redirect(request):
    return redirect(to=reverse(viewname='my_blog:new_page'))      # name from url page

def new_url_page(request):
    return HttpResponse("New Url page")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'blog/contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
    return render(request,'blog/contact.html')

def about(request):

    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default Content goes here!!!"
    else:
        about_content = about_content.content
    return render(request=request, template_name='blog/about.html', context={'about_content': about_content})