from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from app.models import UserQuiz
from app.service.quiz import get_difference


@login_required
def statistic(request):
    try:
        user_quizzes = request.user.user_quizzes.all().order_by('created_at')

        last_quiz: UserQuiz = user_quizzes.last()
        worst_performance = last_quiz.user_answers.filter(question__is_editable=True).annotate(
            duration_sum=Sum('answers__duration')).filter(
            duration_sum__lt=0
        ).order_by(
            'duration_sum'
        )[:5]
        worst_performance_text = list(worst_performance.values_list('question__text', flat=True))
        worst_performance_duration = list(worst_performance.values_list('duration_sum', flat=True))
        worst_performance_duration = [abs(float(i)) for i in worst_performance_duration]

        previous_quiz: UserQuiz = user_quizzes.exclude(id=last_quiz.pk).last()
        improved_results, worsening_results = get_difference(last_quiz, previous_quiz)

        dates = list(user_quizzes.values_list('created_at', flat=True))
        dates = [i.strftime('%m-%d-%Y') for i in dates]

        durations = list(user_quizzes.values_list('duration', flat=True))
        durations = [float(i) for i in durations]

        last_duration = durations[-1]
        improved_duration = round(last_duration + sum(worst_performance_duration[:3]), 2)

        avg_duration = round(sum(durations) / len(durations), 2)
        max_duration = round(max(durations), 2)
        min_duration = round(min(durations), 2)

        return render(request, 'app/flat/statistic.html', {
            'user_quizzes': user_quizzes,
            'last_quiz': last_quiz,

            'worst_performance_text': worst_performance_text,
            'worst_performance_duration': worst_performance_duration,

            'improved_results': improved_results,
            'worsening_results': worsening_results,

            'dates': dates,
            'durations': durations,

            'last_duration': last_duration,
            'improved_duration': improved_duration,
            'avg_duration': avg_duration,
            'max_duration': max_duration,
            'min_duration': min_duration,
        })
    except:
        is_error = True
    return render(request, 'app/flat/statistic.html', {
        'is_error': is_error
    })
