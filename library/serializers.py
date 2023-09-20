from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BookSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = "__all__"
    def get_average_rating(self, obj):
        return (obj.average_rating())
     
# class StudentSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ('name', 'roll_no', 'email')

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
# class BookRequestSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = BookRequest
#         fields = "__all__"

class BookIssuedSerializers(serializers.ModelSerializer):
    book_name = serializers.ReadOnlyField(source='book_id.book_name')
    class Meta:
        model = BookIssued
        exclude = ("book_id", "username", "issued_date", "Issued", "Submitted")

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('id','username', 'email','password','is_active')
        extra_kwargs={'email':{'required':True,'write_only':True},'password':{'write_only':True}}

    def create(self,validate_data):
        user=User(
            email=validate_data['email'],
            username=validate_data['username']
        )

        user.set_password(validate_data['password'])
        user.save()
        return user 


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    book_issued = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_book_issued(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user == obj.owner:
            book_issued_data = BookIssuedSerializers(
                BookIssued.objects.filter(username=user, Issued="Yes"),
                many=True,
                read_only=True
            ).data
            return book_issued_data
        return []

