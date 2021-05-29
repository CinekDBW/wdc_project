from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import Topic, Post
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def home(request):
    context = {
        'public_topics': Topic.objects.filter(is_public=True),
        'private_topics': Topic.objects.filter(is_public=False)
    }
    return render(request, 'forum/home.html', context)


class TopicDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Topic

    def test_func(self):
        topic = self.get_object()
        if topic.is_public or self.request.user.has_perm('forum.can_view_private_topics'):
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.has_perm('forum.can_delete_every_post'):
            return True
        return False