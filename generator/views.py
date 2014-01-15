# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView, CreateView

from generator.models import Song, Artist
from generator.forms import SongForm

# Create your views here.

class ListeChantsParAuteur(ListView):
    model = Song
    context_object_name = "liste_chants" 
    template_name = "generator/song_list_by_artist.html"
    paginate_by = 10
    
    def get_queryset(self):
        self.auteur = get_object_or_404(Artist, slug=self.kwargs['artist'])
        return Song.objects.filter(chanteur=self.auteur)
    
    def get_context_data(self, **kwargs):
        context = super(ListeChantsParAuteur,self).get_context_data(**kwargs)
        context['artist'] = Artist.objects.get(slug=self.kwargs['artist']) 
        # FIXME: Si l'objet n'existe pas ? Déjà géré par le get_object_or_404 ?
        return context


class AfficherChant(DetailView):
    context_object_name = "song" 
    model = Song
    template_name = "generator/show_song.html"

    def get_queryset(self):
        return Song.objects.filter(chanteur__slug=self.kwargs['artist'],slug=self.kwargs['slug'])

# 
# class AjoutChant(CreateView): 
#     model = Song
#     template_name = 'generator/add_song.html'
#     form_class = SongForm
#    success_url = reverse_lazy()


class ListeAuteurs(ListView):
    model = Artist
    context_object_name = "liste_auteurs" 
    template_name = "generator/artist_list.html"
    paginate_by = 20
    queryset = Artist.objects.order_by('name')