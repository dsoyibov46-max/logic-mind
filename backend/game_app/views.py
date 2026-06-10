from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Game
from results.models import GameResult


def game_router(request, slug):

    if slug == 'labirint':
        return redirect('game_app:electro_labirint')

    elif slug == 'memory':
        return redirect('game_app:memory_game')

    elif slug == 'math':
        return redirect('game_app:math_game')

    return redirect('game_app:games_list')


def games_list(request):
    games = Game.objects.filter(is_active=True)

    return render(request, 'game_app/games_list.html', {
        'games': games
    })


@login_required
def electro_labirint_view(request):

    game = get_object_or_404(
        Game,
        url_name='labirint'
    )

    if request.method == 'POST':

        score = int(request.POST.get('score', 0))

        GameResult.objects.create(
            user=request.user,
            game=game,
            score=score
        )

        return redirect('student_dashboard')

    return render(request, 'game_app/electro_labirint.html', {
        'game': game
    })


# MEMORY GAME
@login_required
def memory_game_view(request):
    game = get_object_or_404(Game, url_name='memory')

    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        time_taken = int(request.POST.get('time', 0))

        # MODELGA MOSLASH:
        GameResult.objects.create(
            user=request.user,
            game=game,
            score=score,
            time_spent=time_taken, # Bu yerda 'time_spent' bo'lishi shart
            level_reached=1 # Modelingizda bu maydon ham bor ekan
        )
        return redirect('student_dashboard')

    return render(request, 'game_app/memory.html', {'game': game})
# games/views.py — math_game_view ni shu bilan almashtiring

@login_required
def math_game_view(request):
    game = get_object_or_404(Game, url_name='math')
    return render(request, 'game_app/math.html', {'game': game})