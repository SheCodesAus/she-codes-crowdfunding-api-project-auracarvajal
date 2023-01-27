from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, ProjectDetailsSerializer, PledgeSerializer
from django.http import Http404
from rest_framework import status, generics, permissions
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        projects= Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]


    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailsSerializer(project)
        return Response(serializer.data)

    def put(self,request,pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailsSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class Pledgelist(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    IsOwnerOrReadOnly
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)


    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Project.DoesNotExist:
            raise Http404


    def put(self, request, pk):
        pledge = self.get_object(pk)
        data = request.data
        serializer = PledgeSerializer(
            instance=pledge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
                serializer.save()