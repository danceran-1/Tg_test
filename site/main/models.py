from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255,unique=True)

class CalculationResult(models.Model):
    A = models.IntegerField()
    B = models.IntegerField()
    K1 = models.FloatField()
    mark = models.IntegerField()
    A1 = models.IntegerField()
    B1 = models.IntegerField()
    K2 = models.FloatField()
    mark1 = models.IntegerField()
class Criterion(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/')


class Task(models.Model):
    user_id = models.IntegerField()  # ID пользователя Telegram
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} for user {self.user_id}"