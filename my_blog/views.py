from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
from my_blog.models import Post, AboutUs, Category
from my_blog.forms import ContactForm, RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, PostForm
from django.http import Http404
import logging
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

# static demo data
#posts = [{'id': 1, 'title': 'Post 1', 'content': 'Content of post 1'},
#         {'id': 2, 'title': 'Post 2', 'content': 'Content of post 2'},
#         {'id': 3, 'title': 'Post 3', 'content': 'Content of post 3'},
#         {'id': 4, 'title': 'Post 4', 'content': 'Content of post 4'},]

def index(request):
    blog_title = "Venky's Blog"
    # getting data from post model
    all_posts = Post.objects.filter(is_published=True).order_by("created_at")
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

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash the password
            user.save()  # user data is created
            messages.success(request, 'Registration successful! You can now log in.')
            print("Registration Successful")
            return redirect(to='my_blog:login')
    return render(request=request, template_name='blog/register.html', context={'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request=request, user=user)
                return redirect(to='my_blog:dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def dashboard(request):
    blog_title = "My Posts"
    #getting user posts
    all_posts = Post.objects.filter(user=request.user)

    # paginate
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/dashboard.html', {'blog_title': blog_title, 'page_obj': page_obj})

def logout_view(request):
    logout(request=request)
    return redirect(to="my_blog:index")

def forgot_password(request):
    # Initialize an empty form for the forgot password page
    form = ForgotPasswordForm()

    # Check if the request is a POST request (form submission)
    if request.method == 'POST':
        # Reinitialize the form with data from the request (submitted form data)
        form = ForgotPasswordForm(request.POST)

        # Validate the form to ensure all required fields are filled and correct
        if form.is_valid():
            # Extract the email address submitted by the user
            email = form.cleaned_data['email']

            # Fetch the user object corresponding to the email address
            user = User.objects.get(email=email)

            # Generate a secure token for the user to reset their password
            token = default_token_generator.make_token(user)

            # Encode the user's primary key (ID) in a secure format
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Get the current site (domain name) for including in the email
            current_site = get_current_site(request)
            domain = current_site.domain

            # Define the subject of the email
            subject = "Reset Password Requested"

            # Render the email template with required context (domain, uid, token)
            message = render_to_string('blog/reset_password_email.html', {
                'domain': domain,  # Website domain (e.g., example.com)
                'uid': uid,        # Encoded user ID
                'token': token     # Password reset token
            })

            # Send the reset password email to the user
            send_mail(subject, message, '"no_reply@venky.com"', [email])

            # Display a success message to the user
            messages.success(request, 'Email has been sent')

    # Render the forgot password page with the form (either empty or pre-filled on error)
    return render(request, 'blog/forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('my_blog:login')
            else :
                messages.error(request,'The password reset link is invalid')

    return render(request,'blog/reset_password.html', {'form': form})

@login_required
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        #form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('my_blog:dashboard')
    return render(request,'blog/new_post.html', {'categories': categories, 'form': form})

@login_required
def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()
    if request.method == "POST":
        #form
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated Succesfully!')
            return redirect('my_blog:dashboard')

    return render(request,'blog/edit_post.html', {'categories': categories, 'post': post, 'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted Succesfully!')
    return redirect('my_blog:dashboard')

@login_required
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request, 'Post Published Succesfully!')
    return redirect('my_blog:dashboard')
