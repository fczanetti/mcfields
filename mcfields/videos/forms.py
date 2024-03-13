from django.forms import ModelForm
from django import forms
from mcfields.videos.models import Video


class VideoForm(ModelForm):
    criar_rascunho = forms.ChoiceField(
        choices=(('YES', 'Sim'), ('NO', 'Não')),
        widget=forms.RadioSelect,
        label='Criar rascunho de email:')

    class Meta:
        model = Video
        fields = '__all__'
