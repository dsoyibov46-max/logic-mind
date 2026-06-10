from django.db import models
from django.conf import settings
from game_app.models import Game


class GameResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_results'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField(default=0)
    time_spent = models.PositiveIntegerField(default=0, help_text="Sekundlarda")
    level_reached = models.PositiveIntegerField(default=1)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} - {self.score}"