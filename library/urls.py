from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'book_request', BookIssuedViewSet)
router.register(r'user',UserViewSet,basename='user')
router.register(r'profiles',ProfileViewSet,basename='profiles')
router.register(r'reviews_ratings',ReviewRatingViewSet, basename='reviews_ratings')


urlpatterns = [
    path('', include(router.urls)),
    path('book_request/issue_book/', BookIssuedViewSet.as_view({'post': 'issue_book'}), name='issue-book'),
    
]
