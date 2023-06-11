from django.contrib import admin
from .models import Categories, Post, Author, Reply

admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Reply)

# admin.site.register(News)


