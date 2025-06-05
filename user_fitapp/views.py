from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from datetime import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class BookSlotView(APIView):
    def post(self, request):
        try:
            fitness_class_id = request.data.get('class_id')
            client_name = request.data.get('client_name')
            client_email = request.data.get('client_email')
            client_phone = request.data.get('client_phone')
            
            if not re.match(EMAIL_REGEX, client_email):
                    return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(client_phone)<10:
                    return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

            if not all([fitness_class_id, client_name, client_email, client_phone]):
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            fitness_class = FitnessClass.objects.get(id=fitness_class_id)

            if fitness_class.available_slots <= 0:
                return Response({'error': 'No available slots'}, status=status.HTTP_400_BAD_REQUEST)

            slot_number = fitness_class.book_slot()

            Booking.objects.create(
                fitness_class=fitness_class,
                client_name=client_name,
                client_email=client_email,
                client_phone=client_phone,
                slot=slot_number
            )

            return Response({'message': 'Slot booked successfully'}, status=status.HTTP_201_CREATED)

        except FitnessClass.DoesNotExist:
            return Response({'error': 'Fitness class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AvailableClasses(APIView):
    def get(self, request):
        try:
            available_classes = FitnessClass.objects.filter(available_slots__gt=0)
            serializer = FitnessClassSerializer(available_classes, many=True)
            data = serializer.data

            for item in data:
                try:
                    item['date_time'] = datetime.strptime(item['date_time'], '%Y-%m-%dT%H:%M:%S%z').date().isoformat()
                except ValueError:
                    try:
                        item['date_time'] = datetime.strptime(item['date_time'], '%Y-%m-%dT%H:%M:%S.%f%z').date().isoformat()
                    except Exception:
                        pass  

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSpecificBooking(APIView):
    def get(self, request, user_email):
        try:
            bookings = Booking.objects.filter(client_email=user_email)
            if not bookings.exists():
                return Response({'message': 'No bookings found for this email'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Modules
class RegisterUserView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']

                if not re.match(EMAIL_REGEX, email):
                    return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(email=email).exists():
                    return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(phone=serializer.validated_data['phone']).exists():
                    return Response({'error': 'Phone number is already registered'}, status=status.HTTP_400_BAD_REQUEST)

                if len(serializer.validated_data['password']) < 6:
                    return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)

                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()

                return Response(
                    {"message": "User registered successfully", "user": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({'error': 'Database integrity error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUserView(APIView):
    def post(self, request):
        try:
            phone = request.data.get('phone')
            password = request.data.get('password')

            if not phone or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(phone=phone)

            if not check_password(password, user.password):
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['phone'] = user.phone

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'name': user.username,
                    'phone': user.phone,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
