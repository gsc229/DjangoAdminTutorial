from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

"""
The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
"""
"""  
helpful refresher on *args *kwargs:
https://realpython.com/python-kwargs-and-args/
"""

class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  

