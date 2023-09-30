from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import BookFilter
from .serializers import CustomUserSerializer

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

from django_filters.rest_framework import DjangoFilterBackend


class UserRegistration(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


class ExpressInterest(APIView):
    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        if book.owner == request.user:
            return Response({"message": "You cannot express interest in your own book."},
                            status=status.HTTP_400_BAD_REQUEST)


        book.interested_users.add(request.user)
        return Response({"message": "Interest expressed successfully."}, status=status.HTTP_200_OK)



class OwnershipDecision(APIView):
    def put(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        if book.owner != request.user:
            return Response({"message": "You are not the owner of this book."}, status=status.HTTP_403_FORBIDDEN)

        if book.interested_users.count() == 0:
            return Response({"message": "No users have expressed interest in this book."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the recipient from the request data (e.g., recipient_id)
        recipient_id = request.data.get("recipient_id")
        if recipient_id is None:
            return Response({"message": "Recipient not specified."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            return Response({"message": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the chosen recipient
        book.chosen_recipient = recipient
        book.save()
        return Response({"message": "Recipient selected successfully."}, status=status.HTTP_200_OK)


