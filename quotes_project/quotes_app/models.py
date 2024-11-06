from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.fullname
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.quote
