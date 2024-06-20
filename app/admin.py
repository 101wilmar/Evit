from django.contrib import admin

from app.models import UserQuiz, Quiz, Question, Answer, Location, Referral, UserAnswer
from app.models.proflie import Profile

admin.site.register(Referral)
# admin.site.register(Profile)

# admin.site.register(Location)

admin.site.register(UserQuiz)
# admin.site.register(Quiz)
# admin.site.register(Question)
admin.site.register(Answer)


class QuestionTabularInline(admin.TabularInline):
    model = Question
    extra = 2


class AnswerTabularInline(admin.TabularInline):
    model = Answer
    extra = 3


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [QuestionTabularInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_required', 'is_multiple', 'display_type', 'created_at')
    list_editable = ['is_required', 'is_multiple', 'display_type']
    inlines = [AnswerTabularInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'created_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_quiz', 'question']
