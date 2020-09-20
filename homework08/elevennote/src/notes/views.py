from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import (
    get_object_or_404, render, HttpResponseRedirect, redirect, HttpResponse
)
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import JsonResponse

# For search
from django.db.models import Q
import re
# For sharing notes
import hashlib

from taggit.models import Tag
from .models import Note, Permalink
from .forms import NoteForm
from .mixins import NoteMixin


class NoteList(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'notes/index.html'
    context_object_name = 'latest_note_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-pub_date')


class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/detail.html'
    context_object_name = 'note'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteDetail, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteCreate(LoginRequiredMixin, NoteMixin, CreateView):
    form_class = NoteForm
    template_name = 'notes/form.html'
    success_url = reverse_lazy('notes:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.pub_date = timezone.now()
        
        # tags handling
        new_note = form.save(commit=False)
        new_note.save()
        form.save_m2m()
        
        return super(NoteCreate, self).form_valid(form)


class NoteUpdate(LoginRequiredMixin, NoteMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/form.html'
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('notes:update', kwargs={
            'pk': self.object.pk,
        })
        

class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notes:create')

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


@login_required
def SearchView(request):
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'body', 'tags__name'])
        notes = Note.objects.filter(entry_query, owner=request.user).distinct().order_by('-pub_date')
    else:
        success_url = reverse_lazy('notes:update', kwargs={
            'pk': Note.objects.first().pk,
        })
        return HttpResponseRedirect(success_url)
        
    context = {
        'notes': notes,
        'query': query_string,
    }
    return render(request, 'notes/form.html', context)


def normalize_query(
    query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub
):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects. 
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


@login_required
def share_note(request, note_pk):
    note = get_object_or_404(Note, owner=request.user, pk=note_pk)
    share_key = hashlib.md5(note.title.encode('utf-8')).hexdigest()[:8]
    permalink = Permalink(key=share_key, refersTo=note)
    permalink.save()
    response = {
        'share_key': share_key,
    }
    return JsonResponse(response)


class SharedNote(DetailView):
    template_name = 'notes/detail.html'

    def dispatch(self, *args, **kwargs):
        return super(SharedNote, self).dispatch(*args, **kwargs)

    def get_object(self):
        note = get_object_or_404(Permalink, key=self.kwargs['slug']).refersTo
        return note
