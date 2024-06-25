from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from rest_framework import viewsets
from .models import Category, Course, Lesson, Order, User
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, OrderSerializer, TutorSerializer


# New =====================>>>>

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .generate_tokens_util import create_access_token_admin
from .attach_token_to_cookie_util import attach_token_to_cookie
import os
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

# The `UserProfileSerializer` is a serializer class in Django that is used to serialize and
# deserialize user profile data. It is specifically designed to work with the `User` model and
# includes fields such as 'id', 'email', and 'name'. This serializer is used to represent user
# profile information in a structured format for API requests and responses.
UserProfileSerializer
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success', 'user': {
                'name': user.name,
                'userId':user.id,
                'email': user.email,
                'user_type': user.user_type,  
                'isAdmin': user.is_admin,
                }}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        print('===========================request.user=====>>>', request.user)
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='student')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def put(self, request, format=None):
        user_id = request.data.get('userId')
        is_blocked = request.data.get('is_blocked')
        if user_id is None or is_blocked is None:
            return Response({'error': 'user_id and is_blocked are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = is_blocked
        user.save()

        return Response({'status': 'User block status updated'}, status=status.HTTP_200_OK)


class AdminAllCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def enrolled_courses(self, request):
        user = request.user
        enrolled_courses = user.enrolled_courses.all()
        serializer = self.get_serializer(enrolled_courses, many=True)
        return Response(serializer.data)


class TutorCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_queryset(self):
        # Get the authenticated user from the request
        user = self.request.user

        # Filter courses where the tutor is the authenticated user
        return Course.objects.filter(tutor=user)

    def create(self, request, *args, **kwargs):
        # Set the tutor to the authenticated user
        data = request.data.copy()
        data['tutor'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get_queryset(self):
    #     # Get the authenticated user
    #     user = self.request.user
    #     # Get all courses created by this user
    #     user_courses = Course.objects.filter(tutor=user)
    #     # Get lessons that belong to these courses
    #     return Lesson.objects.filter(course__in=user_courses)

    def create(self, request, *args, **kwargs):
        # Get the authenticated user
        user = self.request.user
        
        # Ensure 'course' is included in the request data
        course_id = request.data.get('course')
        if not course_id:
            return Response({"course": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the course exists and belongs to the user
            course = Course.objects.get(id=course_id, tutor=user)
        except Course.DoesNotExist:
            return Response({"course": ["Invalid course ID."]}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the course to the mutable request data
        mutable_data['course'] = course_id

        # Serialize and validate the mutable request data
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        # Save the lesson with the correct course
        self.perform_create(serializer)

        # Link the lesson with the course
        lesson = serializer.instance
        course.lessons.add(lesson)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def sum_prices(self, request):
        total_price = Order.objects.aggregate(total_price=Sum('price'))['total_price']
        if total_price is None:
            total_price = 0
        return Response({'total_price': total_price}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def course_prices(self, request):
        # Get the filter type from request query params
        filter_type = request.query_params.get('filter', 'all')
        now = timezone.now()

        # Apply date filtering based on the filter type
        if filter_type == 'day':
            start_date = now - timezone.timedelta(days=1)
        elif filter_type == 'week':
            start_date = now - timezone.timedelta(weeks=1)
        elif filter_type == 'month':
            start_date = now - timezone.timedelta(days=30)
        else:
            start_date = None

        # Fetch orders based on the filter
        if start_date:
            orders = Order.objects.filter(created_at__gte=start_date)
        else:
            orders = Order.objects.all()
        
        # Dictionary to hold course data
        course_data = {}

        # Organize order prices by course
        for order in orders:
            course_title = order.course.title
            if course_title not in course_data:
                course_data[course_title] = []
            course_data[course_title].append(order.price)

        # Format the response
        course_list = []
        for course_title, prices in course_data.items():
            course_list.append({
                'name': course_title,
                'data': prices
            })

        response_data = {
            'courseList': course_list
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        courseId = request.data.get('courseId')  # Assuming courseId is passed in request data
        try:
            course = Course.objects.get(id=courseId)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Associate the authenticated user with the order
        request.data['user'] = request.user.id
        
        # Adding course instance to the request data before passing it to serializer
        request.data['course'] = course.id
        request.data['status'] = 'pending'
        request.data['price'] = course.price
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Add the course to the enrolled courses of the user
        request.user.enrolled_courses.add(course)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class TutorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='teacher')
    serializer_class = TutorSerializer

# New =====================================>>>

@csrf_exempt
def admin_signin(request):
    if request.method == 'POST':
        email = os.environ.get('ADMIN_MAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if request.POST.get('email') != email or request.POST.get('password') != password:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

        admin_access_token = create_access_token_admin()
        response = JsonResponse({'message': 'Admin login successful', 'isAuth': True})
        attach_token_to_cookie('adminToken', admin_access_token, response)
        return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def admin_logout(request):
    if request.method == 'POST':
        admin_access_token = request.COOKIES.get('adminToken')
        if not admin_access_token:
            print('Admin access token not found')
        response = JsonResponse({'message': 'Admin logout successful'})
        response.delete_cookie('adminToken')
        return response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@require_http_methods(["GET"])
def check_enrollment(request, course_id):
    user = request.user

    if user.is_authenticated:
        try:
            course = Course.objects.get(id=course_id)
            if course in user.enrolled_courses.all():
                return JsonResponse({'enrolled': True})
            else:
                return JsonResponse({'enrolled': False})
        except Course.DoesNotExist:
            return JsonResponse({'enrolled': False})
    else:
        return JsonResponse({'enrolled': False})