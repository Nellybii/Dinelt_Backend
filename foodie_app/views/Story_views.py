from rest_framework import generics, permissions
from foodie_app.models import Story
from foodie_app.serializer import StorySerializer

class StoryListCreate(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            self.permission_denied(self.request)
        return post
