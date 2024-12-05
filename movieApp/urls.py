from django.contrib import admin
from django.urls import path, include
from .views import UserRegisterationAPIView, ReleaseYearMovieAPIView,CommentAPIView, FavoritesAPIView, UserLoginAPIView, CategoryMovieAPIView, MoviesCreateListAPIView, MovieDetailAPIView, AddFavoriteAPIView

urlpatterns = [
    path("", MoviesCreateListAPIView.as_view(), name = "movie_list"),
    path("<int:pk>/", MovieDetailAPIView.as_view(), name = "movie_detail"),
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("<int:pk>/favorite", AddFavoriteAPIView.as_view(), name="add_favorite"),
    path("favorites/", FavoritesAPIView.as_view(), name = "list_favorites"),
    path("category/<int:category_id>/", CategoryMovieAPIView.as_view(), name="category_list"),
    path('<int:movie_id>/comments/', CommentAPIView.as_view(), name='comment-list'),
    path('year/<int:release_year>', ReleaseYearMovieAPIView.as_view(), name = 'year_list')
]