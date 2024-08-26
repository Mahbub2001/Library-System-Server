from rest_framework import filters, viewsets
from . import models, serializers
from rest_framework.decorators import permission_classes
from .models import Borrower, Book,Wishlist
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    # authentication_classes=[TokenAuthentication]
    queryset = None
    serializer_class = None


class BookCategoryViewset(BaseModelViewSet):
    permission_classes=[AllowAny]
    # authentication_classes=[TokenAuthentication]
    queryset = models.BookCategory.objects.all()
    serializer_class = serializers.BookCategorySerializer

  
class BookViewset(BaseModelViewSet):
    permission_classes = [AllowAny]
    # authentication_classes=[TokenAuthentication]
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['genre__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(genre_id=category_id)
        title_letters = self.request.query_params.get('title')
        if title_letters:
            queryset = queryset.filter(title__icontains=title_letters)

        return queryset

    
# class BorrowerViewset(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#     queryset = Borrower.objects.all()
#     serializer_class = serializers.BorrowerSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         book_id = serializer.validated_data['book'].id
        
#         book = Book.objects.get(id=book_id)
#         if book.quantity > 0:
#             book.quantity -= 1
#             if book.quantity == 0:
#                 book.availability = False
#             book.save()
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"detail": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         book = instance.book

#         book.quantity += 1
#         if book.quantity > 0:
#             book.availability_status = True 
#         book.save()

#         return super().destroy(request, *args, **kwargs)

class BorrowerViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Borrower.objects.all()  
    serializer_class = serializers.BorrowerSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrower.objects.filter(name=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book'].id
        book = Book.objects.get(id=book_id)
        
        if book.quantity > 0:
            book.quantity -= 1
            if book.quantity == 0:
                book.availability_status = False
            book.save()
            serializer.save(name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Book is not available."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name != request.user:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        book = instance.book
        book.quantity += 1
        if book.quantity > 0:
            book.availability_status = True
        book.save()

        return super().destroy(request, *args, **kwargs)

# class WishlistViewset(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#     queryset = Wishlist.objects.all()
#     serializer_class = serializers.WishlistSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         book = instance.book
        
#         return super().destroy(request, *args, **kwargs)

class WishlistViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Wishlist.objects.all() 
    serializer_class = serializers.WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(name=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(name=request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name != request.user:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)