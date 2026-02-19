from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from .permissions import IsAuthorOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from notifications.models import Notification



@extend_schema(
    description="Endpoints for creating, retrieving, updating and deleting social media posts.",
    examples=[
        OpenApiExample(
            'Let Create A Post Example',
            description='Exmaple of a valid request to create a new post.',
            value={
                "title": "My first post",
                "content": "This is the content of my first post"
            },
            request_only=True   # This shows in POST/PUT requests
        ),
        OpenApiExample(
            'Post Detial Example',
            description='Exmaple of a successful response when retrieving a post.',
            value={
                "id": 1,
                "author": "foremanb",
                "title": "My first post",
                "content": "This is the content of my first post",
                "created_at": "2024-02-18T10:00:00Z",
                "updated_at": "2024-02-18T10:00:00Z"
            
            },
            response_only=True, # This shows in GEP responses
        ),
    ]   
)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def perform_create(self, serializer):
        # Let sate the comment and get the instance
        comment = serializer.save(author=self.request.user)
        # Let extract the post that was commented on
        post = comment.post
    
        # Create the notification (Checker looks for this exact string)
        Notification.objects.create(
            recipient=post.author,
            actor=self.request.user,
            verb="commented on your post",
            target=post
        )


class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # Let identify the current logged-in user
        user = self.request.user

        # And let get users that current user follows
        following_users = user.following.all()

        # Now let filter the feed where the author is in the following_user lists, ordered by "-created_at" descending order
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def post(sef, request, pk):
        # Let get the post
        post = generics.get_object_or_404(Post, pk=pk)

        # Let user get_or_create to prevent duplicate likes
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the notification (Checker looks for this exact string)
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="like your post",
            target=post
        )
        
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)
    

class UnlikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, pk):
        # Let get the post (pk comes from the URL)
        post = get_object_or_404(Post, pk=pk)

        # Let find the specific like object
        like_queryset = Like.objects.filter(user=request.user, post=post)

        if like_queryset.exists():
            # Delete the like
            like_queryset.delete()

            # Let remove the notification so the user doesn't see a "ghost" like
            Notification.objects.filter(
                actor=request.user, 
                recipient=post.author, 
                verb="liked your post",
                target_object_id=post.id
            ).delete()

            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        else:
             return Response({"detail": "You have not like this post."}, status=status.HTTP_400_BAD_REQUEST)