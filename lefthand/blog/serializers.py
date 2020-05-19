from rest_framework import serializers

from .models import Post, Category,Tag


# 文章列表接口需要的 Serializer
class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'name'
    )
    tag = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'name'
    )
    owner = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'username'
    )
    created_time = serializers.DateTimeField(
        format = "%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'created_time']
        extra_kwargs = {
            'url': {'view_name': 'api-post-detail'}
        }


# 文章详情接口需要的 Serializer
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'tag',
            'owner', 'content', 'created_time'
        ]


# 分类接口需要的 Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'created_time',
        ]


class CategoryDetailSerialzer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, many=True, context=['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'created_time', 'posts'
        ]


# 标签接口需要的 Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id', 'name', 'created_time',
        ]


class TagDetailSerialzer(TagSerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, many=True, context=['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = [
            'id', 'name', 'created_time', 'posts'
        ]
