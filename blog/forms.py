from django import forms
from .models import Blog, Author, Tag


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = "__all__"
        exclude = ["slug"]
        # widget = {
        #     "date": "SelectDateWidget()",
        # }


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = "__all__"


class CommentForm(forms.Form):
    comment = forms.CharField(
        label="any comments!",
        widget=forms.Textarea(
            attrs={"name": "feel free to write anything", "rows": "2"}
        ),
        required=True,
    )


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, required=True)
    password = forms.CharField(label="password", max_length=40, required=True)
