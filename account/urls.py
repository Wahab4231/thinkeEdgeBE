from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    CategoryViewSet,
    CourseViewSet,
    LessonViewSet,
    OrderViewSet,
    TutorViewSet,
    check_enrollment,
    UserOrderViewSet,
    TutorCourseViewSet,
    UserViewSet,
    AdminAllCourseViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'orders', OrderViewSet)

# Admin
router.register(r'admin/category', CategoryViewSet)
router.register(r'admin/users', UserViewSet)
router.register(r'admin/tutors', TutorViewSet)
router.register(r'admin/courses', AdminAllCourseViewSet)
router.register(r'admin/orders', OrderViewSet)


# Teacher
router.register(r'tutors', TutorViewSet)
router.register(r'tutor/details/top', TutorViewSet)
router.register(r'tutor/courses', TutorCourseViewSet)
router.register(r'tutor/lessons', LessonViewSet)

# User Routes
router.register(r'user/courses', CourseViewSet)
router.register(r'user/lessons', LessonViewSet)
router.register(r'user/orders/create', UserOrderViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegistrationView.as_view(),
         name='user-registration'),
    path('auth/signin/', UserLoginView.as_view(), name='user-login'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/change-password/', UserChangePasswordView.as_view(),
         name='user-change-password'),
    path('auth/send-password-reset-email/',
         SendPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('auth/password-reset/<uid>/<token>/',
         UserPasswordResetView.as_view(), name='password-reset'),
    path('user/details/', UserProfileView.as_view(), name='user-profile'),

    path('user/details/enrolled/<int:course_id>/check/', check_enrollment, name='check_enrollment'),
]