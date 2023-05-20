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
from django.urls import reverse




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
    user_posts = Post.objects.filter(user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'users/create_post.html', {'form': form, 'user_posts': user_posts})


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

from .forms import UserSearchForm
from .models import UserProfile
from django.db.models import Q, Value
from django.db.models.functions import Concat

def search_results(request):
    form = UserSearchForm(request.GET)
    if form.is_valid():
        search = form.cleaned_data['search']
        results = UserProfile.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(full_name__icontains=search)
        )
    else:
        results = UserProfile.objects.none()
    
    return render(request, 'users/search_results_partial.html', {'results': results})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import FriendRequest

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user=user)
    user_posts = Post.objects.filter(user=user)  # Get the posts of the user
    friend_request_sent = FriendRequest.objects.filter(
        sender=request.user,
        receiver=user).first()
    are_friends = request.user.userprofile in user_profile.friends.all()  # Check if they are friends
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'posts': user_posts, 'friend_request_sent': friend_request_sent, 'are_friends': are_friends})



def send_friend_request(request, username):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=user)
        return redirect(request.META.get('HTTP_REFERER', 'default_if_none'))

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if request.user == friend_request.receiver:
        friend_request.receiver.userprofile.friends.add(friend_request.sender.userprofile)
        friend_request.delete()
        return redirect(reverse('profile', args=[friend_request.sender.username])) 
    else:
        # Handle case of someone trying to accept a friend request that is not for them
        return redirect('...') # Redirect to a suitable error page



def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if request.user == friend_request.receiver:
        friend_request.delete()
        return redirect('...')  # redirect to some page
    else:
        # Handle case of someone trying to reject a friend request that is not for them
        return redirect('...')

def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if request.user == friend_request.sender:
        friend_request.delete()
        return redirect(request.META.get('HTTP_REFERER', 'default_if_none'))  # redirect to some page
    else:
        # Handle case of someone trying to cancel a friend request that is not for them
        return redirect('...')

def friend_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')  # or whatever your login route is
    incoming_requests = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'users/friend_requests.html', {'friend_requests': incoming_requests})



