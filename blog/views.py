from django.shortcuts import render
from .models import blogpost
from django.http import HttpResponse

# Create your views here.
def index(request):
    myposts = blogpost.objects.all()
    return render(request,'blog/index.html',{'mypost':myposts})


def Blogpost(request,id):
    myposts = blogpost.objects.all()
    post = blogpost.objects.filter(post_id = id)[0]
    if id>1:
        postpre = blogpost.objects.filter(post_id = id-1)[0]
    else:
        postpre = blogpost.objects.filter(post_id = id)[0]
    if id+1>len(myposts):
        postnext = blogpost.objects.filter(post_id = id)[0]
    else:
        postnext = blogpost.objects.filter(post_id = id+1)[0]
    return render(request, 'blog/blogpost.html',{'post':post,'pre':postpre,'next':postnext})
