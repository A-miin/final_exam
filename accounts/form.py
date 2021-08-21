from django import forms
from accounts.models import User
from phonenumber_field.formfields import PhoneNumberField
class UserUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        error_messages={"invalid": "Формат телефона только в виде +996 XXX XXX XXX"})
    class Meta:
        model = User
        fields = ('phone_number',)

