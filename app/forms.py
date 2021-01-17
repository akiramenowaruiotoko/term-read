from django import forms


class PostForm(forms.Form):
  term = forms.CharField(max_length=30, label='用語')
  content = forms.CharField(label='読み方', widget=forms.Textarea())