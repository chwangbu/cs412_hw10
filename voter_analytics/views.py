from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
from django.db.models import Q

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['partyAffiliation']:
                queryset = queryset.filter(partyAffiliation=form.cleaned_data['partyAffiliation'])
            if form.cleaned_data['minDateOfBirth']:
                queryset = queryset.filter(dateOfBirth__gte=form.cleaned_data['minDateOfBirth'])
            if form.cleaned_data['maxDateOfBirth']:
                queryset = queryset.filter(dateOfBirth__lte=form.cleaned_data['maxDateOfBirth'])
            if form.cleaned_data['voterScore']:
                queryset = queryset.filter(voterScore=form.cleaned_data['voterScore'])
            for field in ['v20State', 'v21Town', 'v21Primary', 'v22General', 'v23Town']:
                if form.cleaned_data[field]:
                    queryset = queryset.filter(**{field: True})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context