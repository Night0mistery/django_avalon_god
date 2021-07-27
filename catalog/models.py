from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

# Create your models here.
class Player(models.Model):
    """
    Model representing players
    """
    MERLIN = 'Merlin'
    PERCIVAL = 'Percival'
    SERVANT = 'Servant'
    MORGANA = 'Morgana'
    ASSASSIN = 'Assassin'
    MINIONS = 'Minion'
    OBERON = 'Oberon'
    MORDRED = 'Mordred'
    # Choices
    ROLE_CHOICES = [
        # good team
        (MERLIN, 'Merlin'),
        (PERCIVAL, 'Percival'),
        (SERVANT, 'Loyal Servant of Author'),
        # evil team
        (MORGANA, 'Morgana'),
        (ASSASSIN, 'Assassin'),
        (MINIONS, 'Minion of Mordred'),
        (OBERON, 'Oberon'),
        (MORDRED, 'Mordred'),
    ]

    # Fields
    player_name = models.CharField(max_length=20, help_text="Player nick name", primary_key=True)
    id = models.PositiveIntegerField(help_text='seat id')
    role = models.CharField(max_length=20, help_text="Role of each player", choices=ROLE_CHOICES, default=SERVANT)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # all_players = Player.objects.all()
    # Morgana_players = Player.objects.filter(role__iexact='MG')
    # number_Morgana_player = Morgana_players.count()
    ...

    # Metadata
    class Meta:
        ordering = ["id"]
        permissions = (("room_holder", " set a player as a Room holder"),)

    # Methods
    def get_absolute_url(self):
        """
         Returns the url to access a particular instance of Player.
         """
        return reverse('player-detail', args=[str(self.player_name)])

   #@permission_required('catalog.room_holder')
    def is_Merlin(self):
        if self.role == 'Merlin':
            return True
        return False


    def __str__(self):
        return f'{self.id} -- {self.player_name}'


class Room(models.Model):
    """Model representing rooms to play"""
    WAIT = 'WAIT'
    PLAY = 'PLAY'
    READY = 'READY'
    STATUS_CHOICES = [
        (WAIT, 'Waiting...'),
        (PLAY, 'Playing...'),
        (READY, 'Ready!')
    ]
    room_id = models.PositiveIntegerField(primary_key=True, help_text='Room id(e.g. 1234)')
    player_num = models.PositiveIntegerField(help_text='Players in the room', default=0)
    Lady_in_the_lake = models.BooleanField(help_text='Whether a lady in the lake is included in the game')
    max_num = models.ForeignKey('Rule', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, default=WAIT, help_text="Room status(waiting/playing/ready)", choices=STATUS_CHOICES)

    class Meta:
        ordering = ['room_id']

    def get_absolute_url(self):
        #Returns the url to access a particular instance of Room.
        return reverse('room-detail', args=[self.room_id])

    def __str__(self):
        return f'{self.room_id} : {self.player_num}/{self.max_num}'

    """
    def display_genre(self):
        #Create a string for the Genre. This is required to display genre in Admin.
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    """

class Rule(models.Model):
    """Rules for different number of players"""
    RULE_CHOICES = [
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ]
    rule_num = models.PositiveIntegerField(primary_key=True, help_text='Number of players', choices=RULE_CHOICES)
    tasks = models.CharField(max_length=20, help_text='Task Rule')

    class Meta:
        ordering = ['rule_num']

    def __str__(self):
        return f'{self.rule_num}'


# run these commands each time the model changed:
# python manage.py makemigrations
# python manage.py migrate
