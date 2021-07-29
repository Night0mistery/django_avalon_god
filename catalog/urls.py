from django.urls import path
from . import views

# add the names in base_generic.html sidebar block
urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('vision/merlin/', views.MerlinVisionView.as_view(), name='merlin-vision'),
    path('vision/percival/', views.PercivalVisionView.as_view(), name='percival-vision'),
    path('vision/morgana/', views.MorganaVisionView.as_view(), name='morgana-vision'),
    path('vision/badrole/', views.BadRoleVisionView.as_view(), name='badrole-vision'),
    path('player/<str:pk>', views.PlayerDetailView.as_view(), name='player-detail'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('room/<str:pk>', views.RoomDetailView.as_view(), name='room-detail'),
]
urlpatterns += [
    path('myrole/', views.RoleVisionUserListView.as_view(), name='my-role'),
]
urlpatterns += [
    path('player/create/', views.PlayerCreate.as_view(), name='player-create'),
    path('player/<str:pk>/update/', views.PlayerUpdate.as_view(), name='player-update'),
    path('player/<str:pk>/delete/', views.PlayerDelete.as_view(), name='player-delete'),
    path('player/<str:pk>/vote/', views.VoteUpdate.as_view(), name='player-vote'),
    path('player/<str:pk>/action/', views.ActionUpdate.as_view(), name='player-action'),
]

urlpatterns += [
    path('room/create/', views.RoomCreate.as_view(), name='room-create'),
    path('room/<int:pk>/update/', views.RoomUpdate.as_view(), name='room-update'),
    path('room/<int:pk>/delete/', views.RoomDelete.as_view(), name='room-delete'),
]

urlpatterns += [
    path('mission/<int:pk>', views.mission, name='mission'),
]