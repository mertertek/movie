from django.contrib import admin
from .models import CustomUser, Movie, Comment, Favorite, Category

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Movie, MovieAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    
admin.site.register(CustomUser, CustomUserAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'is_public')

admin.site.register(Comment, CommentAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie')

admin.site.register(Favorite, FavoriteAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)