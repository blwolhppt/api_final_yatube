from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, FollowSerializer)
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)

    def get_queryset(self):
        pk_post = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk_post)
        return post.comments

    def perform_create(self, serializer):
        pk_post = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=pk_post)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('user__username', 'following__username',)

    def get_queryset(self):
        return self.request.user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
