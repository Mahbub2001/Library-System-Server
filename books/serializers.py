from rest_framework import serializers
from . import models

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookCategory
        fields = '__all__'
        


class BookSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)  
    genre = serializers.CharField(write_only=True) 

    class Meta:
        model = models.Book
        fields = '__all__'
        extra_fields = ['genre_name']

    def create(self, validated_data):
        genre_name = validated_data.pop('genre')  
        genre = models.BookCategory.objects.get(name=genre_name)  
        validated_data['genre'] = genre 
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'genre' in validated_data:
            genre_name = validated_data.pop('genre') 
            genre = models.BookCategory.objects.get(name=genre_name)  
            instance.genre = genre  
        return super().update(instance, validated_data)
       
class BorrowerSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.title', read_only=True)  
    class Meta:
        model = models.Borrower
        fields = '__all__'

        
class WishlistSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = models.Wishlist
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'user', 'book', 'review_text', 'rating', 'created_at']