from django.db import models
from tags.models import Tag
from django.contrib.auth.models import User


class Bug(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="created_by", null=True, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(User, related_name="assigned_to")
    tag = models.ManyToManyField(Tag)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
