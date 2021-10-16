from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Local
    path('tasks/', include('tasks.urls')),
]

