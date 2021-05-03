from django.shortcuts import render

from django.views import generic
from .models import Tournament
from golfer.models import GolferRoundScores


class TournamentListView(generic.ListView):
    model = Tournament
    template_name = 'tournament/tournament_list.html'
    context_object_name = 'tournaments'


class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = "tournament/tournament_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TournamentDetailView, self).get_context_data(**kwargs)
        tournament = self.get_object()
        context['tournament'] = tournament
        context['scores'] = GolferRoundScores.getTournScores(tournament.tourn_id)

        return context
