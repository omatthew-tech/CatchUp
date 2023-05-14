# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        help_texts = {
            'username': None,
        }
        error_messages = {
            'password1': {
                'password_too_similar': None,
                'password_too_short': None,
                'password_too_common': None,
                'password_numeric': None,
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

from django import forms
from .models import UserProfile

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'location', 'occupation', 'profile_picture',)


