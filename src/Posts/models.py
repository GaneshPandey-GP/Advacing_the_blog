from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User 
#from Comment.models import Comments
import Comment.models
from .utils import get_read_time


# Create your models here.
def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)
class Post(models.Model):
    title =  models.CharField(max_length=150)
    slug  = models.SlugField(unique=True)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    width_field =  models.IntegerField(default=0)
    height_field  = models.IntegerField(default=0)
    image  = models.ImageField(upload_to=upload_location,
             null=True,
             blank=True,
             width_field='width_field',
             height_field ='height_field')
    content  = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False)
    reading_time  = models.IntegerField(default=0) 
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp  = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.title
    
    def get_absoulte_url(self):
        return reverse("detail",kwargs={"slug":self.slug})

    def get_Update_absoulte_url(self):
        return reverse("Update",kwargs={"slug":self.slug})

    def get_Delete_absoulte_url(self):
        return reverse("delete",kwargs={"slug":self.slug})        

    def get_markdown(self):
        content = self.content
        safe_content = mark_safe(content)
        return safe_content

    class Meta:
        verbose_name = "post"
        ordering = ["-timestamp","-update"]    
     
    @property
    def get_comment(self):
        instance = self
        qs =  Comment.models.Comments.objects.filter_by_instance(instance).order_by("-timestamp")
        return qs   
    
    @property
    def get_content_type(self):    
        instance  = self 
        content_type = ContentType.objects.get_for_model(instance.__class__).model
        return content_type


#Create Slug
def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receive(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var =  get_read_time(html_string)
        instance.reading_time = read_time_var


pre_save.connect(pre_save_post_receive,sender=Post)                         

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     Comment =  models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE,blank=True,null=True)
#     Messege   =  models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         #return str(self.Comment)
#         return self.user.username