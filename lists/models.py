from django.conf import settings
from django.db import models
from django.urls import reverse


class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    class Meta:
        unique_together = ("list", "text")
        ordering = ("id",)

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
