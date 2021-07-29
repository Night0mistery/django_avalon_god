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
    VOTE_CHOICES = [
        ('agree', 'agree'),
        ('disagree', 'disagree'),
        ('hesitate...', 'hesitate...')
    ]
    ACTION_CHOICES = [
        ('PASS', 'PASS'),
        ('OUT', 'OUT'),
        ('FAIL', 'FAIL'),
    ]
    # Fields
    player_name = models.CharField(max_length=20, help_text="Player nick name", primary_key=True)
    id = models.PositiveIntegerField(help_text='seat id')
    role = models.CharField(max_length=20, help_text="Role of each player", choices=ROLE_CHOICES, default=SERVANT)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vote = models.CharField(max_length=20, help_text="Choose 'agree' if the chief`s proposal sounds OK for you.", choices=VOTE_CHOICES, default='hesitate...')
    action = models.CharField(max_length=10, help_text='PASS if you decide to complete the mission. FAIL if you decide otherwise. OUT if you are not in the mission!', choices=ACTION_CHOICES, default='OUT')

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

    # check the role of player
    def is_Good(self):
        if self.role in ['Merlin', 'Percival', 'Servant']:
            return True
        return False

    def is_Merlin(self):
        if self.role == 'Merlin':
            return True
        return False

    def is_Percival(self):
        if self.role == 'Percival':
            return True
        return False

    def is_Servant(self):
        if self.role == 'Servant':
            return True
        return False

    def is_Evil(self):
        if self.role in ['Morgana', 'Assassin', 'Minion', 'Oberon', 'Mordred']:
            return True
        return False

    def is_Morgana(self):
        if self.role == 'Morgana':
            return True
        return False

    def is_Assassin(self):
        if self.role == 'Assassin':
            return True
        return False

    def is_Minion(self):
        if self.role == 'Minion':
            return True
        return False

    def is_Oberon(self):
        if self.role == 'Oberon':
            return True
        return False

    def is_Mordred(self):
        if self.role == 'Mordred':
            return True
        return False

    def is_Evil_but_Morgana(self):
        if self.role in ['Assassin', 'Minion', 'Mordred']:
            return True
        return False

    def vote_agree(self):
        if self.vote in ['agree']:
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

    def update_status(self):
        player_num = Player.objects.filter(room=self.room_id).count()
        self.player_num = player_num
        if self.status == 'WAIT':
            if player_num == self.max_num.rule_num:
                self.status = 'READY'
        self.save()
        return True

    def role_distribute(self):
        ROLES = self.max_num.roles.split()
        if self.status == 'READY':
            player_in_room = Player.objects.filter(room=self.room_id)
            for player in player_in_room:
                player.role, ROLES = pop_and_remove(ROLES)
                player.save()
            self.status = 'PLAY'
            self.save()
            return True
        return False

    def mission_result(self):
        if self.status == 'PLAY':
            player_in_room = Player.objects.filter(room=self.room_id)
            num_players = player_in_room.all().count()
            num_out = player_in_room.filter(action__iexact='OUT').count()
            num_mission = num_players - num_out
            num_pass = player_in_room.filter(action__iexact='PASS').count()
            num_fail = player_in_room.filter(action__iexact='FAIL').count()
            return self.room_id, num_players, num_mission, num_pass, num_fail
        else:
            return 0, 0, 0, 0


    def get_absolute_url(self):
        #Returns the url to access a particular instance of Room.
        return reverse('room-detail', args=[self.room_id])

    def __str__(self):
        return f'{self.room_id} : Max player: {self.max_num}'

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
    roles = models.CharField(max_length=150, help_text='Roles for each player', null=True)

    class Meta:
        ordering = ['rule_num']

    def __str__(self):
        return f'{self.rule_num}'

import random
def pop_and_remove(items):
    if items:
        index = random.randrange(len(items))
        item = items.pop(index)
        return item, items
# run these commands each time the model changed:
# python manage.py makemigrations
# python manage.py migrate
