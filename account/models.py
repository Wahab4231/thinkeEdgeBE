from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#  Custom User Manager


USER_TYPE_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
)

DIFFICULTY = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('expert', 'Expert'),
    
)

class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            name,
            password=None,
            user_type=None,
            enrolled_courses=None,
            **extra_fields
    ):
        """
        Creates and saves a User with the given email, name, user_type, and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not user_type:
            raise ValueError('user_type is required')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        if enrolled_courses:
            user.enrolled_courses.set(enrolled_courses)  # Set enrolled courses

        return user

    def create_superuser(
            self,
            email,
            name,
            password=None,
            phone=None,
    ):
        """
        Creates and saves a superuser with the given email, name, user_type and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
            user_type='admin',
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Additional fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    enrolled_courses = models.ManyToManyField('Course', blank=True)
    is_blocked = models.BooleanField(default=False)
    token = models.JSONField(default=list,  blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'teacher'}
    )
    about = models.TextField()
    tagline = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY,
        blank=True,
        null=True
    )
    thumbnail = models.CharField(max_length=15000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_visible = models.BooleanField(default=True)
    lessons = models.ManyToManyField(
        'Lesson', related_name='courses', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE)
    description = models.TextField()
    videoURL = models.CharField(max_length=255)
    duration = models.IntegerField()
    order = models.IntegerField(null=True)
    likes = models.ManyToManyField(User, related_name='liked_lessons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s comment on {self.lesson.title}"


class Report(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='reports', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s report on {self.lesson.title}"


class Order(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.name} - {self.course.title}"


# class Tutor(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     phone = models.CharField(max_length=20)
#     age = models.IntegerField(null=True, blank=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     is_blocked = models.BooleanField(default=False)
#     token = models.JSONField(default=list, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.email
