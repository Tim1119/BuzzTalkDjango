from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image

# Create your models here.
class UserPostModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    image = models.ImageField(upload_to='posts',validators=[FileExtensionValidator(['png','jpg','jpeg'])],blank=True,null=True)
    likes = models.ManyToManyField(User,related_name = "likes",blank=True)
    profile = models.ForeignKey('profiles.Profile',on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.text[:30]
    
    def count_likes(self):
        return self.likes.count()

    def count_comment(self):
        return self.comment_set.count()
    
    def all_comments(self):
        return self.comment_set.all()

    @property
    def get_image_url(self):
        try:
            url =self.image.url
        except:
            url=''
        return url
    
    def save(self,force_insert=False,force_update=False,using=None,update_fields=None):
        super().save()
        if self.image:
            img =Image.open(self.image.path)
            if img.height>300 or img.width>300:
                output_size= (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)


    class Meta:
        verbose_name = 'All Posts'
        verbose_name_plural = 'All Posts'
    