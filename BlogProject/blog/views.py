from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from blog.forms import EmailSendForm
# Create your views here.
from blog.forms import CommentForm
from taggit.models import Tag


class post_list_view(ListView):
    model = Post
    paginate_by = 1


def post_list(request, tag_slug = None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list,2)
    page_no = request.GET.get('page')
    try:
        post_list = paginator.page(page_no)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'blog/post_list.html',{'post_list':post_list, 'tag':tag})

def post_detail(request,year,month,day,post):
    post_match = get_object_or_404(Post,slug=post,status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day
                                   )

    comments = post_match.comments.filter(active=True)
    csubmit = False
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)   # get new coment but dont save in db
            new_comment.post = post_match
            new_comment.save()
            csubmit = True
    else:
         form = CommentForm()

    return render(request,'blog/post_detail.html',{'post':post_match,'form':form,'csubmit':csubmit,'comments':comments})

from django.core.mail import send_mail

def EmailSendView(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({}) recommends you to read {}'.format(cd['name'],cd['email'],post.title)
            url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read Post At : \n {}\n\n {}\'s Comments: \n {} '.format(url,cd['name'],cd['Comments'])
            send_mail(subject,message,'pythononlineclasses1@gmail.com',[cd['to']])
            sent = True
    else:
        print('else')
        form = EmailSendForm()
    return render(request,'blog/sharebyemail.html',{'form':form,'post':post,'sent':sent})