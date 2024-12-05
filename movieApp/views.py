from django.shortcuts import get_object_or_404, render
from .serializers import UserRegisterationSerializer, UserLoginSeriazlier, MovieSerializer, CommentSerializer, FavoriteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Comment, Favorite, CustomUser, Category

class UserRegisterationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSeriazlier(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user_serializer = CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = user_serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoviesCreateListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_staff or request.user.is_superuser:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({"You have not permission."}, status=status.HTTP_403_FORBIDDEN)

class MovieDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Movie, pk=pk)

    def get(self, request, pk):
        movie = self.get_object(pk)
        movie_serializer = MovieSerializer(movie)
        
        public_comments = movie.comments.filter(is_public=True)
        public_comment_serializer = CommentSerializer(public_comments, many=True)

        user_private_comments = movie.comments.filter(is_public=False, user=request.user)
        private_comment_serializer = CommentSerializer(user_private_comments, many=True)

        return Response(
            {
                "Movie": movie_serializer.data,
                "Public Comments": public_comment_serializer.data,
                "Private Comments": private_comment_serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        movie = self.get_object(pk)
        if request.user.is_staff or request.user.is_superuser:
            serializer = MovieSerializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'You do not have permission.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        if request.user.is_staff or request.user.is_superuser:
            movie.delete()
            return Response({'message': 'Product deleted.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You do not have permission.'}, status=status.HTTP_403_FORBIDDEN)

class AddFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=pk)
        
        favorite_item = Favorite.objects.filter(user=request.user , movie=movie)

        if favorite_item:
            return Response({"message":"You have already added the movie to your favorites"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            favorite_item = Favorite.objects.create(user = request.user, movie=movie)
            return Response({"message":"Movie added to favorite list."}, status=status.HTTP_201_CREATED)
        

class FavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        favorite_items =Favorite.objects.filter(user=request.user)

        if not favorite_items.exists:
            return Response({"message":"Your favorite list is empty."}, status = status.HTTP_200_OK)

        favorite_display = []
        for favorite in favorite_items:
            movie = favorite.movie
            serialized_movie = MovieSerializer(movie).data              
            favorite_display.append(serialized_movie)
        return Response(favorite_display, status=status.HTTP_200_OK)

class CategoryMovieAPIView(APIView):
    def get(self, request, category_id, *args, **kwargs):

        category = Category.objects.filter(id=category_id).first()

        if not category:
            return Response({"error": f"Category with ID {category_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        movies = Movie.objects.filter(categories=category)
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, *args, **kwargs):

        movie = get_object_or_404(Movie, pk=movie_id)
        comments = movie.comments.filter(is_public=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, movie_id, *args, **kwargs):

        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, movie_id, comment_id, *args, **kwargs):
      
        movie = get_object_or_404(Movie, pk=movie_id)
        comment = get_object_or_404(movie.comments, pk=comment_id)

        if comment.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to update this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReleaseYearMovieAPIView(APIView):
    def get(self, request, release_year, *args, **kwargs):
        movies = Movie.objects.filter(release_year=release_year)

        if not movies.exists():
            return Response({"error": f"No movies found for release year {release_year}."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
