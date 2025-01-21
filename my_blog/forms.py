from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from my_blog.models import Category, Post

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    message = forms.CharField(label='Message', required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='username_form', required=True)
    email = forms.EmailField(max_length=100, label='email_form', required=True)
    password = forms.CharField(max_length=100, label='password_form', required=True)
    confirm_password = forms.CharField(max_length=100, label='confirm_password_form', required=True)

    # make a connection between register form and auth_user table(prebuilt)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!!!")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='username', required=True)
    password = forms.CharField(max_length=100, label='password', required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username and password")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No User Registered with this email.")

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError(message="Password does not match !!")


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200, required=True)
    content = forms.CharField(label='Content', required=True)
    category =  forms.ModelChoiceField(label='Category', required=True, queryset=Category.objects.all())
    image_url = forms.ImageField(label='image_url', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        #custom validation
        if title and len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 Characters long.')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content must be at least 10 Characters long.')
    
    def save(self, commit = ...):

        post =  super().save(commit)
        cleaned_data = super().clean()
        if cleaned_data.get('image_url'):
            post.image_url = cleaned_data.get('image_url')
        else:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
            post.image_url = img_url    

        if commit:
            post.save()
        return post

