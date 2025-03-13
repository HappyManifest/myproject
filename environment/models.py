from django.db import models
class News(models.Model) :
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.title
class Article(models.Model) :
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.title
