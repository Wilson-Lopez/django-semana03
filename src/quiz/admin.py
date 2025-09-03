from django.contrib import admin
from .models import Exam, Question, Choice

class ChoiceInline(admin.TabularInline):
    """Inline admin for choices"""
    model = Choice
    extra = 4

class QuestionInline(admin.StackedInline):
    """Inline admin for questions"""
    model = Question
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """Admin configuration for exams"""
    list_display = ('title', 'created_date')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for questions"""
    list_display = ('text', 'exam')
    inlines = [ChoiceInline]
