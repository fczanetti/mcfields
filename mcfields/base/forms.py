from django import forms
from mcfields.base.models import Subject


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=128,
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
