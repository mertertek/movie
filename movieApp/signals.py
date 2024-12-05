from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from .models import Comment


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Comment)
def update_rating(sender, instance, **kwargs):
    movie = instance.movie 
    comments = movie.comments.filter(is_public=True) 

    total_rating = 0
    for comment in comments:
        total_rating += comment.rating  

    if comments.count() > 0:  
        movie.avarage_rating = total_rating / comments.count()
    else:
        movie.avarage_rating = 0

    movie.save()  


