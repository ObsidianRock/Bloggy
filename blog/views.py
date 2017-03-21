from django.shortcuts import render, get_object_or_404

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm



'''
def post_list(request):
    all_posts = Post.published.all()
    paginator = Paginator(all_posts, 3)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})
'''


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = 'Hey, {} ({}) recommends you reading "{}"'.format(formdata['name'],
                                                                        formdata['email'],
                                                                        post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     formdata['name'],
                                                                     formdata['comments'])
            #send_mail(subject, message, 'admin@myblog.com', [formdata['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
