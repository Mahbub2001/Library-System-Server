from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter() 

router.register('categories', views.BookCategoryViewset)
router.register('books', views.BookViewset)
router.register('wishlist', views.WishlistViewset)
router.register('borrow_list', views.BorrowerViewset)
router.register('reviews', views.ReviewViewSet)  

urlpatterns = [
    path('', include(router.urls)),
]