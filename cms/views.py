from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, Entry
from .forms import PostForm

class EntryListView(ListView):
    model = Entry
    template_name = 'writing/entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        return context

class EntryDetailView(DetailView):
    model = Entry
    template_name = 'writing/entry_single.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['object_list'] = Post.objects.all()
        return context

@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render(request, 'writing/add_post.html', 
                              { 'form': form })

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'writing/post_single.html',
                              {
                                  'post': post,
                              })
