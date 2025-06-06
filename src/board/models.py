
from django.db import models


class Like(models.Model):

    like = models.IntegerField(default=0)

    def __str__(self):
        return f"Like count: {self.like}"
