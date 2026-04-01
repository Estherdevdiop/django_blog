from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'statut', 'date_publication']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre de l'article..."
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Rédigez votre article ici...'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_publication': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date_publication:
            self.initial['date_publication'] = self.instance.date_publication.strftime('%Y-%m-%dT%H:%M')