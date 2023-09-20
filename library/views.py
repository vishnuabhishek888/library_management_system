from .models import *
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from django.shortcuts import get_object_or_404 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django.db.models import Avg

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    def get_permissions(self):
        if self.action == 'list':  
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]  
        return [permission() for permission in permission_classes]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        user = request.user
        rating = request.data.get("rating")

        if Review.objects.filter(username=user, book_id=book_id).exists():
            return Response(
                {"error": "You have already reviewed this book."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if BookIssued.objects.filter(username=user, book_id=book_id, Issued="Yes").exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(username=user, rating=rating)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(
                {"error": "You can only create a review for a book you have issued."},
                status=status.HTTP_400_BAD_REQUEST
            )
class ReviewRatingViewSet(viewsets.ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializers
    permission_classes=[permissions.IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def reviews_ratings(self, request):
        book_id = request.data.get('book_id')
        
        if book_id is None:
            return Response(
                {"error": "Please provide the 'book_id' "},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reviews_ratings = Review.objects.filter(book_id=book_id)
        if not reviews_ratings.exists():
            return Response(
            {"message": "There are no reviews available for this book."},
            status=status.HTTP_404_NOT_FOUND
            )
        grouped_reviews = {}
        for review in reviews_ratings:
            grouped_reviews.setdefault(review.rating, []).append(review)
        average_rating = reviews_ratings.aggregate(Avg('rating'))['rating__avg']
        serialized_grouped_reviews = {
            str(rating): self.get_serializer(reviews, many=True).data
            for rating, reviews in grouped_reviews.items()
            }
        response_data = {
        "average_rating": round(average_rating, 2),
        "reviews_ratings": serialized_grouped_reviews
            }
        return Response(response_data)


class BookIssuedViewSet(viewsets.ModelViewSet):
    serializer_class = BookIssuedSerializers
    permission_classes = [permissions.IsAuthenticated]  
    queryset = BookIssued.objects.filter(Issued="No")
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return BookIssued.objects.all()
        return BookIssued.objects.filter(username=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get("book_id")

        if BookIssued.objects.filter(username=user, Issued="Yes").count() >= 5:
            return Response(
                {"error": "You have already got 5 books."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if BookIssued.objects.filter(username=user, book_id=book_id, Issued="Yes").exists():
            return Response(
                {"error": "You have already got this book."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book = get_object_or_404(Book, pk=book_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=user, book_id=book)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # @action(detail=True, methods=['post'])
    # def issue_book(self, request, pk=None):
    #     book_request = get_object_or_404(BookIssued, pk=pk)
    #     book = book_request.book_id
    #     user = request.user
        
    #     if self.request.user.is_superuser:
    #         if book.available > 0:
    #             if book_request.Issued == "Yes":
    #                 return Response({'error': 'This book has already been issued to this user.'}, status=status.HTTP_400_BAD_REQUEST)
    #             user_books_count = BookIssued.objects.filter(username=book_request.username, Issued="Yes").count()
    #             if user_books_count >= 5:
    #                 return Response({'error': 'This user has already 5 books.'}, status=status.HTTP_400_BAD_REQUEST)
                
    #             book.available -= 1
    #             book_request.Issued = "Yes"
    #             book_request.Submitted="No"
    #             book_request.save()
    #             book.save()
    #             return Response({'message': 'Book issued successfully.'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'message': 'Book quantity is zero. Cannot issue.'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'message': 'You have only permission to request for book.Only admin can issue books.'}, status=status.HTTP_403_FORBIDDEN)

    # @action(detail=True, methods=['post'])
    # def return_book(self, request, pk=None):
    #     book_request = get_object_or_404(BookIssued, pk=pk)
    #     user = request.user
        
    #     if user == book_request.username:
    #         if book_request.Issued == "Yes" and book_request.Submitted == "No":
    #             book = book_request.book_id
    #             book.available += 1
    #             book_request.Submitted = "Yes"
    #             book_request.Issued = "No"
    #             book_request.save()
    #             book.save()
    #             return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'This book is not currently issued to you.'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'error': 'You are not authorized to return this book.'}, status=status.HTTP_403_FORBIDDEN)
    

    @action(detail=False, methods=['post'])
    def issue_book(self, request):
        book_request_id = request.data.get("book_request_id")
        
        # Check if the admin user is authenticated
        if not self.request.user.is_superuser:
            return Response({'message': 'Only admin can issue books.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the book ID is provided in the request body
        if not book_request_id:
            return Response({'error': 'Please provide a book ID in the request body.'}, status=status.HTTP_400_BAD_REQUEST)
        
        book_request = get_object_or_404(BookIssued, pk=book_request_id)
        book = book_request.book_id

        if book.available <= 0:
            return Response({'message': 'Book quantity is zero. Cannot issue.'}, status=status.HTTP_400_BAD_REQUEST)

        if BookIssued.objects.filter(username=book_request.username, book_id=book_request.book_id, Issued = "Yes").exists():
            return Response({'error': 'This book has already been issued to this user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_books_count = BookIssued.objects.filter(username=book_request.username, Issued="Yes").count()
        if user_books_count >= 5:
            return Response({'error': 'This user has already 5 books.'}, status=status.HTTP_400_BAD_REQUEST)

        book.available -= 1
        book_request.Issued = "Yes"
        book_request.Submitted = "No"
        book_request.save()
        book.save()
        return Response({'message': 'Book issued successfully.'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def return_book(self, request):
        book_request_id = request.data.get("book_request_id")
        user = request.user

        if not book_request_id:
            return Response({'error': 'Please provide a book request ID in the request body.'}, status=status.HTTP_400_BAD_REQUEST)

        book_request = get_object_or_404(BookIssued, pk=book_request_id)

        if user != book_request.username:
            return Response({'error': 'You are not authorized to return this book.'}, status=status.HTTP_403_FORBIDDEN)

        if book_request.Issued == "Yes" and book_request.Submitted == "No":
            book = book_request.book_id
            book.available += 1
            book_request.Submitted="Yes"
            book_request.Issued="No"
            book_request.save()
            book.save()
            return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This book is not currently issued to you or has already been submitted.'}, status=status.HTTP_400_BAD_REQUEST)

    


from django.contrib.auth.models import User

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    
    def list(self, request):
        if request.user.is_superuser: 
            users = User.objects.all()
            serializer = UserSerializers(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "You do not have permission to view this list."}, status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(owner=user)
        return Profile.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

