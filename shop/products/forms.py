from django import forms
from django.contrib.auth import get_user_model

from .models import Comments


#class EmailPostForm(forms.Form):
#    name = forms.CharField(max_length=25, widget=forms.HiddenInput)
#    email = forms.EmailField()
#    comments = forms.CharField(required=False,
#                               widget=forms.HiddenInput)


class EmailPostForm(forms.ModelForm):

    email = forms.EmailField(label='Email', disabled=False, widget=forms.EmailInput)

    class Meta:
        model = get_user_model()
        fields = ['email']


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body', 'rating']

        def clean_rating(self):
            rating_comment = self.cleaned_data['rating']
            if rating_comment > 5:
                raise forms.ValidationError('Оценка не должна превышать 5')
            return rating_comment
