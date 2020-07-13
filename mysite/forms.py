from django import forms
from .models import MyComment
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = MyComment
        fields = { 'msg'}
