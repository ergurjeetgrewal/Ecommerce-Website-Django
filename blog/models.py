from django.db import models

# Create your models here.


class blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50,default='')
    title = models.CharField(max_length=50)
    head0 = models.CharField(max_length=50, default="")
    head0highlight = models.CharField(max_length=500, default="")
    head0content = models.CharField(max_length=500, default="")
    head1 = models.CharField(max_length=50, default="")
    head1content = models.CharField(max_length=500, default="")
    head2 = models.CharField(max_length=50, default="")
    head2content = models.CharField(max_length=500, default="")
    pub_date = models.DateField()
    thumnail = models.ImageField(upload_to="blog/images", default="")

    def __str__(self):
        return self.title

