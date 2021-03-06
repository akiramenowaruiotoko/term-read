from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_


class IndexView(View):
  def get(self, request, *args, **kwargs):
    post_data = Post.objects.order_by('-id')
    return render(request, 'app/index.html', {
        'post_data': post_data
    })

  
class PostDetailView(View):
  def get(self, request, *args, **kwargs):
    post_data = Post.objects.get(id=self.kwargs['pk'])
    return render(request, 'app/post_detail.html', {
        'post_data': post_data
    })

class CreatePostView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    form = PostForm(request.POST or None)

    return render(request, 'app/post_form.html', {
      'form': form
    })

  def post(self, request, *args, **kwargs):
    form = PostForm(request.POST or None)

    if form.is_valid():
      post_data = Post()
      post_data.author = request.user
      post_data.term = form.cleaned_data['term']
      post_data.content = form.cleaned_data['content']
      post_data.save()
      return redirect('post_detail', post_data.id)

    return render(request, 'app/post_form.html', {
      'form': form
    })


class PostEditView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    post_data = Post.objects.get(id=self.kwargs['pk'])
    form = PostForm(
      request.POST or None,
      initial= {
        'term': post_data.term,
        'content': post_data.content
      }
    )

    return render(request, 'app/post_form.html', {
      'form': form
    })

  def post(self, request, *args, **kwargs):
    form = PostForm(request.POST or None)

    if form.is_valid():
      post_data = Post.objects.get(id=self.kwargs['pk'])
      post_data.term = form.cleaned_data['term']
      post_data.content = form.cleaned_data['content']
      post_data.save()
      return redirect('post_detail', self.kwargs['pk'])

    return render(request, 'app/post_form.html', {
      'form': form
    })


class PostDeleteView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    post_data = Post.objects.get(id=self.kwargs['pk'])
    return render(request, 'app/post_delete.html', {
      'post_data': post_data
    })

  def post(self, request, *args, **kwargs):
    post_data = Post.objects.get(id=self.kwargs['pk'])
    post_data.delete()
    return redirect('index')


class SearchView(View):
  def get(self, request, *args, **kwargs):
    post_data = Post.objects.order_by('-id')
    keyword = request.GET.get('keyword')

    if keyword:
      exclusion_list = set([' ', ' '])
      query_list = ''
      for word in keyword:
        if not word in exclusion_list:
          query_list += word
      query = reduce(and_, [Q(term__icontains=q) | Q(content__icontains=q) for q in query_list ])
      post_data = post_data.filter(query)

    return render(request, 'app/index.html', {
      'keyword': keyword,
      'post_data': post_data
    })