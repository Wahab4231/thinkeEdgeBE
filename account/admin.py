from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Course, Lesson, Comment, Report, Order


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'user_type', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'name',
            'last_name',
            'user_type',
            'phone',
            'age',
            'address',
            'website',
            'about',
            'is_active',
            'is_blocked'
        )}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'last_name',
                'user_type',
                'password1',
                'password2',
                'is_active',
                'is_blocked',
                'phone',
                'age',
                'address',
                'enrolled_courses',
                'website',
                'token',
                'about',
            ),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tutor', 'about', 'tagline', 'category',
                    'difficulty', 'thumbnail', 'price', 'is_visible', 'created_at', 'updated_at')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'description',
                    'videoURL', 'duration', 'order', 'created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'content', 'createdAt')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'user', 'reason', 'createdAt')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'status',
                    'price', 'created_at', 'updated_at')


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
