# Create your views here.
# posts/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.utils import create_notification


class FeedView(generics.ListAPIView):
    """
    Aggregated feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list('id', flat=True)
        return Post.objects.select_related('author').filter(author_id__in=following_ids).order_by('-created_at')


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for posts.
    """
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikePostView(APIView):
    """
    Like a post. Creates a notification for the post author.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            if post.author != request.user:
                create_notification(recipient=post.author, actor=request.user, verb='liked', target=post)
            return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already liked.'}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    """
    Unlike a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for comments.
    """
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
