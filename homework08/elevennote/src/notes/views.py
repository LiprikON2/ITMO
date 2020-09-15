from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from taggit.models import Tag
from .models import Note
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
        
        # return reverse('notes:update', kwargs={
        #     'pk': self.object.pk
        # })
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
    

def NoteTagList(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tagged_notes = Note.objects.filter(owner=request.user, tags=tag)
    context = {
        'notes': tagged_notes,
    }
    return render(request, 'notes/form.html', context)
    
    
def NoteTagDelete(request, slug, note_pk):
    note = Note.objects.get(pk=note_pk)
    tag = get_object_or_404(Tag, slug=slug)
    note.tags.remove(tag)
    
    success_url = reverse_lazy('notes:update', kwargs={
        'pk': note_pk,
    })
    return HttpResponseRedirect(success_url)
