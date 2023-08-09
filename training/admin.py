from django.contrib import admin

from training.models import Course, Lesson, Payments

# admin.site.register(Course)
# admin.site.register(Lesson)
# admin.site.register(Payments)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)\

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('course',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course', 'lesson', 'payment_amount', 'payment_way')
    search_fields = ('user', 'date', 'payment_amount', 'payment_way')
    list_filter = ('user', 'date', 'payment_amount', 'payment_way')