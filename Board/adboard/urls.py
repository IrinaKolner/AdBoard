from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ReplyCreate, Replies, ReplyUpdate, ReplyDelete, CategoryList, subscribe, RepliesSorted


urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/reply/', ReplyCreate.as_view(), name='reply_create'),

   path('my_replies/', Replies.as_view(), name='my_replies'),
   path('reply/<int:pk>/update/', ReplyUpdate.as_view(), name='reply_update'),
   path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),

   path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

   path('replies_sorted/<int:pk>/', RepliesSorted.as_view(), name='replies_sorted_list'),
]