from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from posts.models import Posts, Users
from django.contrib.auth.models import User


class Genre(MPTTModel):
    blog = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment')
    name = models.ForeignKey(Users, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def __str__(self):
        return self.body


    class MPTTMeta:
        order_insertion_by = ['name']
