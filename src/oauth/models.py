# from django.db import models


# class User(models.Model):
#     email = models.EmailField(unique=True)

#     class Meta:
#         db_table = 'auth_user'
#         indexes = [
#             models.Index(fields=['email'], name='user_email_idx'),
#         ]

#     def __str__(self):
#         return f'User {self.pk}'

#     def save(self, request) -> None:
#         email = request.data.get('email')
#         User(email=email).save()
