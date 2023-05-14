from django.http import HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404



def user_list(request):
    users = User.objects.all()
    output = ', '.join([user.name for user in users])
    return HttpResponse(output)

def home(request):
    if request.user.is_authenticated:
        return redirect('create_post')  # Replace 'create_post' with your actual view name for creating posts.
    else:
        return render(request, 'users/home.html')

# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('create_post')  # Assuming you have a view and URL pattern with this name
    template_name = 'users/register.html'

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'users/edit_profile.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_posts = Post.objects.filter(user=user)  # Get the posts of the user
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'posts': user_posts})


