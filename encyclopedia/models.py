from django.db import models

class Article(models.Model):
    id = models.BigAutoField(primary_key=True)  # Use BigAutoField if you want larger ID range
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
