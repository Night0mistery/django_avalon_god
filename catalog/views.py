from .models import Player, Room, Rule
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_players = Player.objects.all().count()
    num_rooms = Room.objects.all().count()
    # The 'all()' is implied by default.
    num_rules = Rule.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_players': num_players,
        'num_rooms': num_rooms,
        'num_rules': num_rules,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class PlayerListView(generic.ListView):
    model = Player
    #context_object_name = 'Player'
    #template_name = 'players/player_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Player.objects.all()
        #return Player.objects.filter(role__iexact='ML')[:10]

class MerlinVisionView(generic.ListView):
    model = Player
    paginate_by = 10
    template_name = 'catalog/merlin_list.html'

    def get_queryset(self):
        return Player.objects.filter(role__in=['Morgana', 'Assassin', 'Minion', 'Oberon'])

class PercivalVisionView(generic.ListView):
    model = Player
    paginate_by = 10
    template_name = 'catalog/percival_list.html'

    def get_queryset(self):
        return Player.objects.filter(role__in=['Merlin', 'Morgana'])

class MorganaVisionView(generic.ListView):
    model = Player
    paginate_by = 10
    template_name = 'catalog/morgana_list.html'

    def get_queryset(self):
        return Player.objects.filter(role__in=['Mordred', 'Assassin', 'Minion'])

class BadRoleVisionView(generic.ListView):
    model = Player
    paginate_by = 10
    template_name = 'catalog/badrole_list.html'

    def get_queryset(self):
        return Player.objects.filter(role__in=['Morgana', 'Assassin', 'Minion', 'Mordred'])

class RoomListView(generic.ListView):
    model = Room
    paginate_by = 10

    def get_queryset(self):
        return Room.objects.all()

class PlayerDetailView(generic.DetailView):
    model = Player

class RoomDetailView(generic.DetailView):
    model = Room

class RoleVisionUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Player
    template_name ='catalog/role_vision_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

class PlayerCreate(CreateView):
    model = Player
    fields = ['player_name', 'id', 'role', 'room', 'user']
    initial = {'room': '1000'}

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['player_name', 'id', 'room', 'user']# Not recommended (potential security issue if more fields added)

class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('players')

class RoomCreate(CreateView):
    model = Room
    fields = ['room_id', 'Lady_in_the_lake', 'max_num']
    initial = {'Lady_in_the_lake': False}

class RoomUpdate(UpdateView):
    model = Room
    fields = ['room_id', 'Lady_in_the_lake', 'max_num']

class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('rooms')

class VoteUpdate(UpdateView):
    model = Player
    fields = ['vote']
    success_url = reverse_lazy('my-role')

class ActionUpdate(UpdateView):
    model = Player
    fields = ['action']
    success_url = reverse_lazy('my-role')

@login_required
def mission(request, pk):
    """View function for home page of site."""
    room = get_object_or_404(Room, pk=pk)
    # Generate counts of some of the main objects
    room_id, num_players, num_mission, num_pass, num_fail = room.mission_result()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'room_id': room_id,
        'num_mission': num_mission,
        'num_pass': num_pass,
        'num_fail': num_fail,
        'num_visits': num_visits
    }

    return render(request, 'mission.html', context=context)