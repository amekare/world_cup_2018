from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    cups = models.IntegerField(default=0)
    finals = models.IntegerField(default=0)
    semifinals = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Round(models.Model):
    GROUP_CHOICES = (
        ('A', 'Grupo A'),
        ('B', 'Grupo B'),
        ('C', 'Grupo C'),
        ('D', 'Grupo D'),
        ('E', 'Grupo E'),
        ('F', 'Grupo F'),
        ('G', 'Grupo G'),
        ('H', 'Grupo H'),
    )
    ROUND_CHOICES = (
        ('1', 'Primera fase'),
        ('2', 'Octavos'),
        ('3', 'Cuarto'),
        ('4', 'Semifinales'),
        ('5', 'Tercer lugar'),
        ('6', 'Finales'),
    )
    group = models.CharField(choices=GROUP_CHOICES, max_length=1, null=True)
    stage = models.CharField(choices=ROUND_CHOICES, max_length=1, default='1')
    played_matches = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING)

    def get_group(self):
        return self.get_group_display()

    def __str__(self):
        return self.get_group_display() + ' - ' + self.team.name


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=32)
    positions = models.ManyToManyField(Position)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING)
    birth_date = models.DateField(null=True, blank=True)
    jerseyNumber = models.IntegerField(null=True)
    world_cups = models.IntegerField(default=0)
    world_cups_won = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Bet(models.Model):
    source = models.ForeignKey('Gambler', on_delete=models.DO_NOTHING, verbose_name='Fuente')
    match = models.ForeignKey('Match', on_delete=models.DO_NOTHING, verbose_name='Partido de referencia')
    team1 = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='bteam1', default="2",
                              verbose_name='Equipo 1')
    team2 = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='bteam2', default="2",
                              verbose_name='Equipo 2')
    goals_team1 = models.IntegerField(default=0, verbose_name='Goles equipo 1')
    goals_team2 = models.IntegerField(default=0, verbose_name='Goles equipo 2')
    checked = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.team1:
    #         team1 = self.match.team1
    #         team2 = self.match.team2
    #     return super(Bet, self).save(*args, **kwargs)

    def __str__(self):
        return self.team1.name + " - " + self.team2.name


class Match(models.Model):
    team1 = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='team1')
    team2 = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name='team2')

    def __str__(self):
        return self.team1.name + " - " + self.team2.name


class Gambler(models.Model):
    name = models.CharField(max_length=48)
    points_winner = models.IntegerField(default=0)
    points_score = models.IntegerField(default=0)
    points_8vo = models.IntegerField(default=0)
    points_4vo = models.IntegerField(default=0)
    points_semi = models.IntegerField(default=0)
    points_3er = models.IntegerField(default=0)
    points_final = models.IntegerField(default=0)

    def total(self):
        return self.points_3er + self.points_4vo + self.points_8vo + self.points_final + self.points_score
        +self.points_semi + self.points_winner


def __str__(self):
    return self.name
