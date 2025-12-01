from django.db import models
# Create your models here.

class Author(models.Model):
    """
    Represents a writer/author.
    - name: human-readable name of the author.
    One Author can be linked to many Books via the Book.author FK.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ["name"]
        

class Book(models.Model):
    """
    Represents a book entity.
    - title: book title.
    - publication_year: year the book was published (validated in serializer).
    - author: FK to Author (one-to-many relationship).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"


    class Meta:
        ordering = ["title"]
