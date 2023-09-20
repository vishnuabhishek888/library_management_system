from django.contrib import admin
from .models import *

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'book_name', 'quantity', 'available']
    search_fields = ['book_name', 'book_id']

# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'roll_no', 'email']
#     search_fields = ['name', 'roll_no', 'email']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'username', 'review', 'review_date','rating']
    list_filter = ['review_date']
    search_fields = ['book_id__book_name', 'username__name']

class BookIssuedAdmin(admin.ModelAdmin):
    list_display = ['book_id', 'username']
    search_fields = ['book_id__book_name', 'username__name']

# class BookRequestAdmin(admin.ModelAdmin):
#     list_display = ['book_id', 'username', 'request_date']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'gender', 'dob', 'phone', 'profile_image']
    # search_fields = ['owner', 'phone']

admin.site.register(Book, BookAdmin)
# admin.site.register(Student, StudentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BookIssued, BookIssuedAdmin)
# admin.site.register(BookRequest, BookRequestAdmin)
admin.site.register(Profile, ProfileAdmin)
