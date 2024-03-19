from django.forms import ModelForm
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from mcfields.newsletter.models import Newsletter


class NewsletterForm(ModelForm):
    criar_rascunho = forms.ChoiceField(
        choices=(('YES', 'Sim'), ('NO', 'Não')),
        widget=forms.RadioSelect,
        label='Criar rascunho de email:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Newsletter
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'})
        }
