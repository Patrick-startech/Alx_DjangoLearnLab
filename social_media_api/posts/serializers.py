# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments_count']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        comment = super().create(validated_data)
        post = comment.post
        if post.author != comment.author:
            create_notification(recipient=post.author, actor=comment.author, verb='commented', target=post)
        return comment
    
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate(self, attrs):
        # Optional: protect against empty content or overly long content
        content = attrs.get('content', '').strip()
        if not content:
            raise serializers.ValidationError({'content': 'Content cannot be empty.'})
        return attrs

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
