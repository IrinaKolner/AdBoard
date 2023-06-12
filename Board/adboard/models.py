from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний
# потом разобрать этот бардак
tank = 'Танк'
healer = 'Хил'
damager = 'ДД'
guild_master = 'Гилдмастер'
quest_giver = 'Квестгивер'
smith = 'Кузнец'
tanner = 'Кожевник'
potion_maker = 'Зельевар'
spell_master = 'Мастер заклинаний'

CATEGORIES = [
    (tank, 'Танк'),
    (healer, 'Хил'),
    (damager, 'ДД'),
    (guild_master, 'Гилдмастер'),
    (quest_giver, 'Квестгивер'),
    (smith, 'Кузнец'),
    (tanner, 'Кожевник'),
    (potion_maker, 'Зельевар'),
    (spell_master, 'Мастер заклинаний'),
]

class Categories(models.Model):
    name = models.CharField(max_length=17, choices=CATEGORIES, default=tank)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Название")
    text = RichTextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


    # Метод preview() модели Post, который возвращает начало статьи
    # (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    # def preview(self):
    #     return f'{self.text[0:124]}...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False) # это понадобится для подтверждения отклика


# # это нужно для новостей, но возможно можно будет убрать и как-то по-другому реализовать рассылку новостей
# class News(models.Model):
#     title = models.CharField(max_length=100, default="Default value")
#     text = models.TextField()
#     time_created = models.DateTimeField(auto_now_add=True)

