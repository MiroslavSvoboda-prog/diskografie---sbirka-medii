from django.views.generic import ListView, DetailView, TemplateView
from .models import Album, Film, Kniha


class HomeView(TemplateView):
    template_name = 'sbirka/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pocet_alb'] = Album.objects.count()
        context['pocet_filmu'] = Film.objects.count()
        context['pocet_knih'] = Kniha.objects.count()
        return context


class AlbumListView(ListView):
    model = Album
    template_name = 'sbirka/album_list.html'
    context_object_name = 'alba'


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'sbirka/album_detail.html'
    context_object_name = 'album'


class FilmListView(ListView):
    model = Film
    template_name = 'sbirka/film_list.html'
    context_object_name = 'filmy'


class FilmDetailView(DetailView):
    model = Film
    template_name = 'sbirka/film_detail.html'
    context_object_name = 'film'


class KnihaListView(ListView):
    model = Kniha
    template_name = 'sbirka/kniha_list.html'
    context_object_name = 'knihy'


class KnihaDetailView(DetailView):
    model = Kniha
    template_name = 'sbirka/kniha_detail.html'
    context_object_name = 'kniha'
