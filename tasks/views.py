from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TaskSerializer
from . import services


class AllCreateTasksView(APIView):
    serializer_class = TaskSerializer

    def get(self, request):
        all_tasks = services.get_all_tasks()
        serialized_tasks = self.serializer_class(all_tasks, many=True).data
        return Response(serialized_tasks)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_task = services.create_task(serializer.data)
            serialized_task = self.serializer_class(new_task).data
            return Response(serialized_task)

        return Response(serializer.errors, status=400)


class DeleteTaskView(APIView):

    def delete(self, request, pk):
        services.delete_task(pk)
        return Response(status=204)

