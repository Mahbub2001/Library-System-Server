from django.contrib import admin
from . import models

class BookCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

admin.site.register(models.Book)
admin.site.register(models.BookCategory, BookCategoryAdmin)
admin.site.register(models.Borrower)
admin.site.register(models.Wishlist)
admin.site.register(models.Review)
