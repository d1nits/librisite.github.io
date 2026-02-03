from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Review, Book, Selection


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title',
            'content',
            'rating',
            'image',
            'video',
            'audio',
        ]
        labels = {
            'title': _('Заголовок'),
            'content': _('Текст рецензії'),
            'rating': _('Оцінка'),
            'image': _('Зображення'),
            'video': _('Відео'),
            'audio': _('Аудіо'),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'cover',
        ]
        labels = {
            'title': _('Назва книги'),
            'author': _('Автор'),
            'description': _('Опис'),
            'cover': _('Обкладинка'),
        }

class SelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        fields = ['name', 'description', 'books']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Назва добірки',
            'description': 'Опис',
            'books': 'Оберіть книги',
        }
