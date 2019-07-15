from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    content = models.TextField()
    create_time = models.TimeField()

    def __str__(self):
        return f'({self.id}) {self.name}-{self.title}'

