from django.shortcuts import render,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect,Http404,HttpResponse
from .models import Comments
from django.contrib import messages
from Posts.models import Post
from Comment.forms import CommentForm

@login_required(login_url="login/")
def comment_delete(request,id):
    try:
        obj = Comments.objects.get(id=id)
    except:
        raise Http404    

    if request.user != obj.user:
        #raise Http404
        response = HttpResponse("You do not have permission to view this page.")
        response.status_code = 403
        return response

    if request.method =="POST":
        obj.delete()
        messages.success(request,"Deleted successfully!")
        return HttpResponseRedirect(obj.content_object.get_absoulte_url())

    context = {"object":obj}
    return render(request,"comment_delete.html", context)     
        

def comment_thread(request,id):
    obj = Comments.objects.get(id=id)
    try:
        obj = Comments.objects.get(id=id)
    except:
        raise Http404    

    if not obj.is_parent:
        obj = obj.parent

    initial_data = {
        "content_type": obj.content_type,
        "object_id":obj.id
    }
    form = CommentForm(initial=initial_data)
    if request.method =="POST":
        form = CommentForm(request.POST or None,initial=initial_data)
        if form.is_valid():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get_for_model(obj)
            obj_id = form.cleaned_data.get("object_id")
            content_data = form.cleaned_data.get("content")
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
    context = {
        "comment":obj,
        'form':form
    }
    return render(request,"comment_thread.html",context)