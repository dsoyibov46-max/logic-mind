import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from game_app.models import Game
from .models import GameResult
from django.db.models import Sum, Max


@csrf_exempt
@login_required
def save_game_result(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)

        game_id = data.get('game_id')
        score = data.get('score', 0)
        time_spent = data.get('time_spent', 0)
        level_reached = data.get('level_reached', 1)

        game = Game.objects.get(id=game_id)

        result = GameResult.objects.create(
            user=request.user,
            game=game,
            score=score,
            time_spent=time_spent,
            level_reached=level_reached
        )

        return JsonResponse({
            'status': 'success',
            'result_id': result.id
        })

    except Game.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Game topilmadi'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


# results/views.py

from django.db.models import Sum, Max  # ← shu qatorni fayl boshiga qo'shing

# ...existing imports...


def leaderboard(request):
    results = (
        GameResult.objects
        .select_related('user')
        .values(
            'user__id',
            'user__username',
            'user__avatar',
        )
        .annotate(
            score=Sum('score'),
            time_spent=Sum('time_spent'),
            level_reached=Max('level_reached'),
        )
        .order_by('-score')[:10]
    )
    return render(request, 'results/leaderboard.html', {'results': results})