from django import forms
from accounts.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number',)

