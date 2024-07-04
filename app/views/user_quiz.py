import pdfkit
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import get_template

from app.models import UserQuiz, Location, Question
from app.models.quiz import Quiz
from app.service.quiz import save_user_quiz, set_life_expectancy
from app.service.user_quiz import calculate_life_expectancy
from constants import PATH_WKHTMLTOPDF


@login_required
def quiz_list(request):
    user = request.user
    user_quizzes = user.user_quizzes.all().order_by('-created_at')
    return render(request, 'app/user_quiz/list.html', {
        'user_quizzes': user_quizzes
    })


@login_required
def start_quiz(request):
    quiz = Quiz.objects.first()
    questions = quiz.questions.all()
    locations = Location.objects.all().order_by('name')
    return render(request, 'app/quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'locations': locations
    })


@login_required
def save_quiz(request):
    if request.method != 'POST':
        return redirect(reverse('app:quiz_list'))
    user = request.user
    quiz = Quiz.objects.first()
    user_quiz = UserQuiz.objects.create(
        user=user,
        quiz=quiz
    )
    user_quiz.save()
    data = request.POST
    save_user_quiz(user_quiz, data)
    set_life_expectancy(user_quiz)
    # return redirect(reverse('app:quiz_list'))
    return redirect(reverse('app:user_quiz_recommendation', args=[user_quiz.id]))


@login_required
def quiz_detail(request, user_quiz_id):
    user_quiz = get_object_or_404(UserQuiz, pk=user_quiz_id)
    user_questions_and_answers = {}
    user_answers = user_quiz.user_answers.all()
    user_questions = user_answers.values_list('question_id', flat=True)

    for q in user_questions:
        user_questions_and_answers[q] = user_answers.filter(question_id=q).values_list('answers__text', flat=True)

    quiz = user_quiz.quiz
    quiz_questions = quiz.questions.all()

    data = calculate_life_expectancy(user_quiz)
    return render(request, 'app/user_quiz/detail.html', {
        'user_quiz': user_quiz,
        'user_questions_and_answers': user_questions_and_answers,
        'quiz_questions': quiz_questions,
        'data': data
    })


@login_required
def user_quiz_recommendation(request, user_quiz_id: int):
    user_quiz = get_object_or_404(UserQuiz, pk=user_quiz_id)
    recommendation_user_answers = user_quiz.user_answers.annotate(
        duration_sum=Sum('answers__duration')
    ).exclude(
        question__is_recommendation=False
    ).filter(
        duration_sum__lt=0,
    ).order_by('question_id')
    recommendation_user_answers = recommendation_user_answers.select_related('question')
    return render(request, 'app/user_quiz/recommendation/detail.html', {
        'user_quiz': user_quiz,
        'recommendation_user_answers': recommendation_user_answers
    })


@login_required
def user_quiz_recommendation_pdf(request, user_quiz_id: int):
    user_quiz = get_object_or_404(UserQuiz, id=user_quiz_id)
    user = user_quiz.user
    template = get_template('app/user_quiz/recommendation/pdf.html')

    recommendation_user_answers = user_quiz.user_answers.annotate(
        duration_sum=Sum('answers__duration')
    ).exclude(
        question__is_recommendation=False
    ).filter(
        duration_sum__lt=0,
    ).order_by('question_id')
    recommendation_user_answers = recommendation_user_answers.select_related('question')
    html = template.render({
        'user': user,
        'user_quiz': user_quiz,
        'recommendation_user_answers': recommendation_user_answers
    })
    options = {
        'margin-top': '0.3cm',
        'margin-right': '1.0cm',
        'margin-bottom': '0.0cm',
        'margin-left': '2.0cm',
        'page-size': 'A4',
        'copies': 1,
        # 'dpi': 96
    }

    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF) if PATH_WKHTMLTOPDF else None

    pdf = pdfkit.from_string(html, False, options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment;filename = "recommendation-{user_quiz.created_at.strftime("%d.%m.%Y")}.pdf"'
    return response
