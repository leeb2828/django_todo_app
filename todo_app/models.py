from django.db import models

# TodoList
class TodoList(models.Model):
    name = models.TextField(max_length=18)

    def __str__(self):
        return self.name 

# Task
class Task(models.Model):
    name = models.CharField(max_length=22)
    todolist_id = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    
    def get_list(self, todolist_id):
        _list_ = TodoList.objects.get(id=todolist_id)
        return _list_ 

    def __str__(self):
        return self.name 