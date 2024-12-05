from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils.timezone import now
from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name="movie_category")
    avarage_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey(Movie,  on_delete=models.CASCADE, related_name="comments",)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie.title} - {self.user.name}"

class Favorite(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fav_movies")
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.movie}"

