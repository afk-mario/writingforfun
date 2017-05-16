from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext

from .models import Post
from .forms import PostForm

@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render(request, 'writting/add_post.html', 
                              { 'form': form })

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'writting/blog_post.html',
                              {
                                  'post': post,
                              })
