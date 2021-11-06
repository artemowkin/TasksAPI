from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TaskSerializer
from . import services


class AllCreateTasksView(APIView):
    serializer_class = TaskSerializer

    def get(self, request):
        all_tasks = services.get_all_tasks(request.user)
        serialized_tasks = self.serializer_class(all_tasks, many=True).data
        return Response(serialized_tasks)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_task = services.create_task(request.user, serializer.data)
            serialized_task = self.serializer_class(new_task).data
            return Response(serialized_task, status=201)

        return Response(serializer.errors, status=400)


class ConcreteTaskView(APIView):
    serializer_class = TaskSerializer

    def get(self, request, pk):
        task = services.get_concrete_task(request.user, pk)
        serialized_task = self.serializer_class(task).data
        return Response(serialized_task)

    def delete(self, request, pk):
        services.delete_task(request.user, pk)
        return Response(status=204)

