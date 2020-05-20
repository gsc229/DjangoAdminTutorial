from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
"""
The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
"""

""" GET all, POST   (generics.ListCreateAPIView) """
class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
""" GET single, PUT, DELETE    (RetrieveUpdateDestroyAPIView) """
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  
"""  GET the a list of all users (ListAPIView) """
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

"""  GET single user (RetrieveAPIView) """
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer