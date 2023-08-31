from django.contrib import admin

from training.models import Course, Lesson, Payments

# admin.site.register(Course)
# admin.site.register(Lesson)
# admin.site.register(Payments)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('course',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'course', 'lesson', 'payment_amount', 'payment_method')
    search_fields = ('owner', 'date', 'payment_amount', 'payment_method')
    list_filter = ('owner', 'date', 'payment_amount', 'payment_method')