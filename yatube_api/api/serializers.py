from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('author',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def get_follow_user(self, data):
        return User.objects.get(username=data['following'])

    def validate(self, data):
        current_user = self.context['request'].user

        if data['following'] == current_user:
            raise serializers.ValidationError(
                'Невозможно оформить подписку на самого себя!'
            )

        try:
            follow = self.get_follow_user(data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Not valid follower')
        if Follow.objects.filter(user=current_user, following=follow).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )

        return data

    def create(self, validated_data):
        follow = self.get_follow_user(validated_data)
        validated_data['following'] = follow
        return Follow.objects.create(**validated_data)
