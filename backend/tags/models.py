from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(max_length=140)

    def __str__(self):
        return self.name
