from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    company = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.company

class Book(models.Model):
    isbn = models.CharField(unique=True, primary_key=True, null=False, max_length=13)
    title = models.CharField(max_length=200)
    auth = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    image = models.CharField(max_length=400)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Url(models.Model):
    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    kb = models.URLField(unique=True)
    yp = models.URLField(unique=True)
    bd = models.URLField(unique=True)
    
    def __str__(self):
        return self.book.title