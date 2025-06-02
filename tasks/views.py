from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Result
from .serializers import TaskSerializer, ResultSerializer
from rest_framework.authtoken.models import Token
from .tasks import process_task


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        process_task.delay(task.id)

    @action(detail=False, methods=['get'])
    def verify_token(self, request):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        try:
            token_obj = Token.objects.get(key=token)
            return Response({'user_id': token_obj.user_id})
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):  
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(task__created_by=self.request.user)
