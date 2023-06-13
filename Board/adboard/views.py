from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Reply, Author, Categories
from django.contrib.auth.models import User
from .forms import PostForm, ReplyForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


class PostsList(ListView):
    model = Post
    # ordering = 'name'
    ordering = '-time_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # success_url = reverse_lazy('your_success_url')

    def form_valid(self, form):
        # kek
        kek = form.save(commit=False)
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            author = Author.objects.create(user=user)
        post = form.save(commit=False)
        post.author = author
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_create.html'

    # # сделать проверку на то, является ли тот, кто откликается автором этого поста
    # # если да, то кнопка не должна будет показаться
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(*kwargs)
    #     author = self.request.user
    #     sender = Post.objects.get()
    #     return context

    def form_valid(self, form):
        reply = form.save(commit=False)
        if self.request.method == 'POST':
            pk = self.request.path.split('/')[-3]
            sender = self.request.user
            reply.post = Post.objects.get(id=pk)
            reply.sender = User.objects.get(username=sender)
        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        # таким образом отправляет на страницу с объявлением, по которому составлялся отклик
        url = '/'.join(self.request.path.split('/')[0:-2])
        return url


class Replies(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'my_replies.html'
    context_object_name = 'replies'
    ordering = '-date_created'
    paginate_by = 5

    # сделать проверку не на то - не должен отправитель и автор совпадать
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(sender_id=self.request.user.id)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post__author_id=self.request.user.id)


class CategoryList(ListView):
    model = Post
    template_name = 'categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Categories, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Categories.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


# принимать и удалять отклики
# не работает
class ReplyUpdate(LoginRequiredMixin, UpdateView):
    model = Reply
    fields = ['text', 'confirmed']
    template_name = "reply_confirmed.html"
    # success_url = reverse_lazy('my_replies')

    def form_valid(self, form):
        reply = form.save(commit=False)
        if reply.confirmed:
            subject = 'Ваш отклик на объявление был принят'
            message = f'Ваш отклик "{reply.text}" на объявление "{reply.post.title}" был принят.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [reply.sender.email]
            # recipient_list = ['forstbooksstudents@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
        return super().form_valid(form)

class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_confirm_delete.html'
    success_url = reverse_lazy('my_replies')


# фильтрация откликов по объявлениям
class RepliesSorted(ListView):
    model = Reply
    template_name = 'sorted_replies.html'
    context_object_name = 'sorted_replies'
    paginate_by = 5

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post.replies.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
