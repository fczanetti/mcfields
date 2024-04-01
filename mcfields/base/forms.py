from django import forms
from django.core.exceptions import ValidationError

from mcfields.base.models import Subject, Contact


class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=128,
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
                             error_messages={'required': 'É necessário informar um email para cadastro.',
                                             'invalid': 'Informe um endereço de email válido.'})
    policy_agreement = forms.BooleanField(error_messages={
        'required': 'É necessário concordar com nossa política de privacidade.'})


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def clean_agree_with_policy(self):
        data = self.cleaned_data['agree_with_policy']
        if not data:
            raise ValidationError('Você deve concordar com nossa política de privacidade.')
        return data
