from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class BookCategory(models.Model):
    name = models.CharField(max_length = 30)
    slug = models.SlugField(max_length = 40)
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title= models.CharField(max_length=200)
    description= models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    availability_status = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Borrower(models.Model):
    name= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
    book= models.ForeignKey(Book,on_delete= models.CASCADE)
    book_name = models.CharField(max_length=200, blank=True, null=True) 
    borrowDate = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.book_name = self.book.title  
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}:{self.book}'
    
    
class Wishlist(models.Model):
    name= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE)
    book= models.ForeignKey(Book,on_delete= models.CASCADE)
    book_name = models.CharField(max_length=200, blank=True, null=True) 
    wishlistDate = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.book_name = self.book.title  
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}:{self.book}'
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.book}'