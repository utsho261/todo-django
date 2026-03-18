from django.urls import path
from core.views import (
    index,
    create_task,
    delete_task,
    detail_task,
    edit_task,
    complete_task
)

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_task, name='create_task'),
    path('task/<int:id>/', detail_task, name='detail_task'),
    path('task/<int:id>/edit/', edit_task, name='edit_task'),
    path('task/<int:id>/delete/', delete_task, name='delete_task'),
    path('task/<int:id>/complete/', complete_task, name='complete_task'),
]