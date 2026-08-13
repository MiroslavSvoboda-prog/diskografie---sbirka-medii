from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Album, Film, Kniha
from .forms import AlbumForm, FilmForm, KnihaForm


class HomeView(TemplateView):
    template_name = 'sbirka/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pocet_alb'] = Album.objects.count()
        context['pocet_filmu'] = Film.objects.count()
        context['pocet_knih'] = Kniha.objects.count()
        return context


# --- Album ---

class AlbumListView(ListView):
    model = Album
    template_name = 'sbirka/album_list.html'
    context_object_name = 'alba'


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'sbirka/album_detail.html'
    context_object_name = 'album'


class AlbumCreateView(CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'sbirka/album_form.html'
    success_url = reverse_lazy('sbirka:album_list')


class AlbumUpdateView(UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'sbirka/album_form.html'
    success_url = reverse_lazy('sbirka:album_list')


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'sbirka/album_confirm_delete.html'
    success_url = reverse_lazy('sbirka:album_list')


# --- Film ---

class FilmListView(ListView):
    model = Film
    template_name = 'sbirka/film_list.html'
    context_object_name = 'filmy'


class FilmDetailView(DetailView):
    model = Film
    template_name = 'sbirka/film_detail.html'
    context_object_name = 'film'


class FilmCreateView(CreateView):
    model = Film
    form_class = FilmForm
    template_name = 'sbirka/film_form.html'
    success_url = reverse_lazy('sbirka:film_list')


class FilmUpdateView(UpdateView):
    model = Film
    form_class = FilmForm
    template_name = 'sbirka/film_form.html'
    success_url = reverse_lazy('sbirka:film_list')


class FilmDeleteView(DeleteView):
    model = Film
    template_name = 'sbirka/film_confirm_delete.html'
    success_url = reverse_lazy('sbirka:film_list')


# --- Kniha ---

class KnihaListView(ListView):
    model = Kniha
    template_name = 'sbirka/kniha_list.html'
    context_object_name = 'knihy'


class KnihaDetailView(DetailView):
    model = Kniha
    template_name = 'sbirka/kniha_detail.html'
    context_object_name = 'kniha'


class KnihaCreateView(CreateView):
    model = Kniha
    form_class = KnihaForm
    template_name = 'sbirka/kniha_form.html'
    success_url = reverse_lazy('sbirka:kniha_list')


class KnihaUpdateView(UpdateView):
    model = Kniha
    form_class = KnihaForm
    template_name = 'sbirka/kniha_form.html'
    success_url = reverse_lazy('sbirka:kniha_list')


class KnihaDeleteView(DeleteView):
    model = Kniha
    template_name = 'sbirka/kniha_confirm_delete.html'
    success_url = reverse_lazy('sbirka:kniha_list')
