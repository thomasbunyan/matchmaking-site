from django.db import models
from django.contrib.auth.models import User


class Hobby(models.Model):
    name = models.CharField(default="hobbyName", max_length=100)
    description = models.TextField(default="hobbyDesc", max_length=100)

    class Meta:
        verbose_name_plural = "hobbies"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to='profile_pics')
    GENDERS = (
        ('M', 'M'),
        ('F', 'F')
    )
    gender = models.CharField(default="?", choices=GENDERS, max_length=1)
    description = models.TextField(
        default="Something about yourself", max_length=200)
    location = models.CharField(default="Town/City", max_length=100)
    dob = models.DateField(null=True)
    hobbies = models.ManyToManyField(
        Hobby, blank=True, related_name='categories')
    adjectives = models.TextField(default="adjective", max_length=401)
    views = models.IntegerField(default=0)
    prevHeat = models.IntegerField(default=0)
    newMatches = models.IntegerField(default=0)
    heat = models.ManyToManyField(
        related_name='user_heat',
        to='self',
        blank=True,
        symmetrical=False
    )

    def __str__(self):
        return self.user.username + "'s profile"
