from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UNIT_CHOICE


# Profile settings Form
class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    child_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control'}))
    feed_goal = forms.IntegerField(initial=0,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    units = forms.CharField(max_length=8,widget=forms.Select(choices=UNIT_CHOICE,attrs={'class': 'form-control'}))
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'child_name', 'feed_goal', 'units']


# User Change Password Form
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2 = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    def clean(self):
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError("New password and password confirmation don't match. Please try again.")
            return self.cleaned_data

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
