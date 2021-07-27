from .models import Player, Room, Rule
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RoleVisionForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_players = Player.objects.all().count()
    num_rooms = Room.objects.all().count()

    # Available Rooms (status = 'a')
    num_rooms_wait = Room.objects.filter(status__iexact='WT').count()

    # The 'all()' is implied by default.
    num_rules = Rule.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_players': num_players,
        'num_rooms': num_rooms,
        'num_rooms_wait': num_rooms_wait,
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


class RoomListView(generic.ListView):
    model = Room
    paginate_by = 10

    def get_queryset(self):
        return Room.objects.all()

    """
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    """


class PlayerDetailView(generic.DetailView):
    model = Player

class RoomDetailView(generic.DetailView):
    model = Room


from django.contrib.auth.mixins import LoginRequiredMixin

class RoleVisionUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Player
    template_name ='catalog/role_vision_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Player.objects.filter(user=self.request.user)

@login_required
#@permission_required('catalog.room_holder')
def RoleVision(request, pk):
    player = get_object_or_404(Player, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RoleVisionForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            player.role = form.clean_role_vision
            print(player.role)
            player.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RoleVisionForm(initial={'role': 'Servant'})

    context = {
        'form': form,
        'player': player,
    }
    return render(request, 'catalog/role_vision.html', context)

class PlayerCreate(CreateView):
    model = Player
    fields = ['player_name', 'id', 'role', 'room', 'user']
    initial = {'room': '1000'}

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['player_name', 'id', 'role', 'room', 'user']# Not recommended (potential security issue if more fields added)

class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('players')

class RoomCreate(CreateView):
    model = Room
    fields = ['room_id', 'player_num', 'Lady_in_the_lake', 'max_num', 'status']


class RoomUpdate(UpdateView):
    model = Room
    fields = ['room_id', 'player_num', 'Lady_in_the_lake', 'max_num', 'status']


class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('rooms')