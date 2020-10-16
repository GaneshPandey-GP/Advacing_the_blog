from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, Http404,reverse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post
from .forms import PostForm,UserLoginForm,UserRegisterForm
from Comment.models import Comments
from Comment.forms import CommentForm
from .utils import get_read_time

def Login_view(request):
    print(request.user.is_authenticated)
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("usernsme")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('home')
    context = {"form":form,"title":title}
    return render(request,"login.html",context)

def Logout_view(request):
    logout(request)
    return redirect('login')

def Register_view(request):
    print(request.user.is_authenticated)
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        return redirect("login")
    context = {"form":form,"title":title}
    return render(request,"login.html",context)


def create_post(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Successfully created!!")
            return redirect("/")

    contaxt = {"form": form}
    return render(request, 'create.html', contaxt)


def List_post(request):
    post = Post.objects.all().order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        post = post.filter(Q(title__icontains=query) |
                           Q(content__icontains=query) |
                           Q(user__username__icontains=query)).distinct()

    paginator = Paginator(post, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginator_queryset = paginator.page(page)

    except PageNotAnInteger:
        paginator_queryset = paginator.page(1)

    except EmptyPage:
        paginator_queryset = paginator.page(paginator.num_pages)

    context = {"post": paginator_queryset, "title": 'List',
               'page_request_var': page_request_var}
    return render(request, 'index.html', context)


def details_post(request, slug):
    instance = Post.objects.get(slug=slug)
    comments = instance.get_comment
    print(get_read_time(instance.get_markdown()))
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id":instance.id
    }
    form = CommentForm(initial=initial_data)
    if request.method =="POST":
        form = CommentForm(request.POST or None,initial=initial_data)
        if form.is_valid():
            print('yes')
            c_type = form.cleaned_data.get("content_type")
            print(c_type)
            content_type = ContentType.objects.get(model=c_type)
            print(content_type)
            obj_id = form.cleaned_data.get("object_id")
            print(obj_id)
            content_data = form.cleaned_data.get("content")
            #print(content_data)
            ##replies
            parent_obj = None

            try:
                parent_id  = int(request.POST.get("parent_id"))
            except:
                parent_id = None
           
            if parent_id:
                parent_qs = Comments.objects.filter(id=parent_id)
                if parent_qs.exists() :
                    parent_obj = parent_qs.first()   
            new_comment,created = Comments.objects.get_or_create(
                                   user = request.user,
                                   content_type=content_type,
                                   object_id= obj_id,
                                   content = content_data,   
                                   parent = parent_obj, 
                                )
            return HttpResponseRedirect(new_comment.content_object.get_absoulte_url())                    
            
            
    context = {"posts": instance,"comments":comments,"form":form}
    return render(request, 'details.html', context)


def update_post(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    obj = Post.objects.get(slug=slug)
    form = PostForm(request.FILES or None, instance=obj)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated!!")
            return redirect("/")
    contaxt = {"form": form}
    return render(request, 'update.html', contaxt)


def delete_post(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    obj = Post.objects.get(slug=slug)
    if request.method == "POST":
        obj .delete()
        messages.success(request, "Successfully deleted !!")
        return redirect("/")

    contaxt = {"title": "Delete"}
    return render(request, 'delete.html', contaxt)
