# tasks/schema.py

import graphene
from graphene_django import DjangoObjectType
from .models import Task, Result

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'

class ResultType(DjangoObjectType):
    class Meta:
        model = Result
        fields = '__all__'

class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)
    task = graphene.Field(TaskType, id=graphene.Int())
    results = graphene.List(ResultType)

    def resolve_tasks(self, info):
        return Task.objects.all()

    def resolve_task(self, info, id):
        return Task.objects.get(pk=id)

    def resolve_results(self, info):
        return Result.objects.all()

schema = graphene.Schema(query=Query)
