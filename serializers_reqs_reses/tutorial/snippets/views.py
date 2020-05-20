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

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  """
  List all code snippets, or create a new snippet.
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  
  """
    BEFORE REFACTOR USING MIXINS
    def get(self, request, format=None):
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)
  """
  def get(self, request, *args, **kwargs):    
    return self.list(request, *args, **kwargs)

  """ 
  BEFORE REFACTOR USING MIXINS
  def post(self, request, format=None):
    
    serializer = SnippetSerializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)     
    return Response(serializer.errors)
  """
  def post(self, request, *args, **kwargs):    
    return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):
  """  
  Retrieve, update or delete a code snippet.
  """
  # class function to be called in all the single-instance methods
  """  
    No LONGER NEED THIS BC of querset and serializer_class
    def get_object(self, pk):
      try:    
          return Snippet.objects.get(pk=pk)
      except Snippet.DoesNotExist:
          raise Http404
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer

  """ 
    BEFORE:
    def get(self, request, *args, **kwargs):
      snippet = self.get_object(pk)
      serializer = SnippetSerializer(snippet)  
      return Response(serializer.data) 
  """
  """ AFTER """
  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  """
    BEFORE
    def put(self, request, *args, **kwargs):
      snippet = self.get_object(pk)
      serializer = SnippetSerializer(snippet, data=request.data)

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  """
  """ AFTER """
  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)

  """ 
    BEFORE
    def delete(self, request, *args, **kwargs):
      snippet = self.get_object(pk)
      snippet.delete()
      return HttpResponse(status=status.HTTP_204_NO_CONTENT)
  """ 
  """ AFTER """
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)

  
  """ 
  https://www.django-rest-framework.org/tutorial/3-class-based-views/

  Refactoring to class based 
  """