from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
from django.db.models import Q
from django.db.models.functions import ExtractYear
import plotly.express as px
import plotly.io as pio
from django.utils.safestring import mark_safe
from django.db.models import Count

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
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
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
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
                if form.cleaned_data.get(field):
                    queryset = queryset.filter(**{field: True})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        queryset_year = queryset.exclude(dateOfBirth__isnull=True)
        queryset_year = queryset_year.annotate(birth_year=ExtractYear('dateOfBirth'))
        year_data = queryset_year.values('birth_year').order_by('birth_year')
        year_counts = {record['birth_year']: queryset_year.filter(birth_year=record['birth_year']).count() for record in year_data}
        fig_year = px.bar(x=list(year_counts.keys()), y=list(year_counts.values()), labels={'x': 'Year of Birth', 'y': 'Count'})
        context['year_birth_histogram'] = mark_safe(pio.to_html(fig_year, full_html=False))

        party_counts = queryset.values('partyAffiliation').annotate(count=Count('partyAffiliation'))
        fig_party = px.pie(party_counts, names='partyAffiliation', values='count', title='Voter Distribution by Party Affiliation')
        context['party_affiliation_pie'] = mark_safe(pio.to_html(fig_party, full_html=False))

        election_fields = ['v20State', 'v21Town', 'v21Primary', 'v22General', 'v23Town']
        election_counts = {field: queryset.filter(**{field: True}).count() for field in election_fields}
        fig_election = px.bar(x=list(election_counts.keys()), y=list(election_counts.values()), labels={'x': 'Election', 'y': 'Voter Count'})
        context['election_participation_histogram'] = mark_safe(pio.to_html(fig_election, full_html=False))

        context['form'] = VoterFilterForm(self.request.GET)
        
        return context