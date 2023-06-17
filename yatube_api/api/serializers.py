from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, User, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True,
                            default=serializers.CurrentUserDefault(),
                            slug_field='username')

    following = SlugRelatedField(queryset=User.objects.all(),
                                 slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=('user', 'following'))]

    def validate(self, validated_data):
        if validated_data['following'] == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться.')
        return validated_data
