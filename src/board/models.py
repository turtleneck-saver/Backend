
from django.db import models


class Like(models.Model):
    board_id = models.CharField(primary_key=True, max_length=64, default=1)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"Like count: {self.like}"
