from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100