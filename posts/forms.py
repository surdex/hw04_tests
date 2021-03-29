from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {
            'text': 'Текст Вашего поста',
        }
        help_texts = {
            'text': 'Здесь Вы можете рассказать, что у Вас нового.',
            'group': 'Выберите группу, которая лучше всего '
                     'подходит к теме Вашего поста.'
        }
        error_messages = {
            'text': {
                'required': 'Посты без текста мало кому интересны, '
                            'пожалуйста, поделитесь своей историей!',
            },
        }
