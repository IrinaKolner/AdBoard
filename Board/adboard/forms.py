from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Reply



class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']