from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    book_name = models.CharField(max_length=50)
    book_id = models.IntegerField(unique=True, primary_key=True)
    book_summary = models.TextField()
    quantity = models.IntegerField()
    available = models.IntegerField()
    def average_rating(self):
        reviews = self.review.all()  
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average = total_rating / reviews.count()
            return round(average, 2)
        return 0.0
# class Student(models.Model):
#     name = models.CharField(max_length=50)
#     roll_no = models.IntegerField(unique=True, null=False)
#     email = models.EmailField(unique=True)
#     password=models.CharField(max_length=50, default="Example@123")

class Review(models.Model):
    book_id = models.ForeignKey(Book, related_name='review', on_delete=models.CASCADE)
    username= models.ForeignKey('auth.User', related_name='review', on_delete=models.CASCADE,default=None, blank=True, null=True)
    review = models.CharField(max_length=500)
    review_date = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True)

    class Meta:
        unique_together = ['book_id', 'username']


# class BookRequest(models.Model):
#     book_id = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)  
#     username = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  
#     request_date = models.DateTimeField(auto_now_add=True)
#     # Issued=models.CharField(max_length=10, default="No")

class BookIssued(models.Model):
    book_id = models.ForeignKey(Book, related_name='book_issued', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='book_issued', on_delete=models.CASCADE)
    # requested_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  
    issued_date = models.DateTimeField(auto_now_add=True, null=True)
    Issued=models.CharField(max_length=10, default="No")
    Submitted=models.CharField(max_length=5, default="No")



options = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others')
)

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_data')
    gender = models.CharField(
        max_length=20,
        choices=options,
        default='male',
        null=False,
        blank=False
    )
    dob = models.DateField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_image", null=True, blank=True)