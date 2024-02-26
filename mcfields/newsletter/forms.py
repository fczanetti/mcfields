from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from mcfields.newsletter.models import Newsletter


class NewsletterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Newsletter
        fields = ['title', 'intro', 'content', 'author', 'slug']
        widgets = {
            'content': CKEditor5Widget(attrs={'class': 'django_ckeditor_5'})
        }
