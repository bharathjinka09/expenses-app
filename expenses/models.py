from django.db import models

# Create your models here.
class Book(models.Model):
    article = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    author = models.CharField(max_length=255, default="")
    page_no = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.article},{self.title},{self.author},{self.page_no}"

    class Meta:
        db_table = "Book"
