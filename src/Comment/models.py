from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from Posts.models import Post

# Create your models here.
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager,self).filter(parent=None)
        return qs

    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager,self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs

class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    #post = models.ForeignKey(Post,on_delete=models.CASCADE ,null=True, blank=True)

    #GENERIC FOREIGN_KEY
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True,blank=True)
    object_id = models.PositiveIntegerField() 
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey("self",on_delete=models.CASCADE, blank=True,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True            

    @property
    def get_content_type(self):    
        instance  = self 
        content_type = ContentType.objects.get_for_model(instance.__class__).model
        return content_type

    def get_Delete_comment_absoulte_url(self):
        return reverse("comment_delete",kwargs={"id":self.id})     
 
    def get_absoulte_url(self):
        return reverse("thread",kwargs={"id":self.id})    

    class Meta:
        verbose_name = "comment"
