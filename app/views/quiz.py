from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from app.models import Quiz


@login_required
def management_quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'app/quiz/list.html', {
        'quizzes': quizzes
    })


@login_required
def management_quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all().order_by('created_at')
    return render(request, 'app/quiz/detail.html', {
        'quiz': quiz,
        'questions': questions
    })
