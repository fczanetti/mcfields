from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from mcfields.servicos.models import Servico


class ServicoForm(ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'})
        }
