from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

from .models import Topic, Post
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def home(request):
    context = {
        'topics': Topic.objects.filter(is_public=True, is_verified=True),
    }
    return render(request, 'forum/home.html', context)


def private_topics(request):
    context = {
        'topics': Topic.objects.filter(is_public=False, is_verified=True),
    }
    return render(request, 'forum/topic_private.html', context)


class TopicDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Topic

    def test_func(self):
        topic = self.get_object()
        if topic.is_public or self.request.user == topic.author or self.request.user in topic.allowed_users.all() or self.request.user.has_perm('forum.can_view_all_topics'):
            return True
        return False


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['title', 'is_public', 'allowed_users']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic

    def test_func(self):
        post = self.get_object()
        if self.request.user.has_perm('forum.can_verify_topics'):
            return True
        return

    def get_success_url(self):
        return reverse('verify-topics')


class TopicConfirmView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    fields = ['is_verified']
    template_name_suffix = '_confirm_form'

    def test_func(self):
        post = self.get_object()
        if self.request.user.has_perm('forum.can_verify_topics'):
            return True
        return

    def get_success_url(self):
        return reverse('verify-topics')



def topicVerifyView(request):

    context = {
        'topics': Topic.objects.filter(is_verified=False)
    }
    return render(request, 'forum/topic_verify.html', context)


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