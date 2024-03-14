from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from mcfields.servicos.models import Service


class ServiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'})
        }
