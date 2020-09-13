from .models import Note


class NoteMixin(object):
    
    def get_context_data(self, **kwargs):
        print('\n\n\n Its me ― NoteMixin ― who is crashing, isnt it?')
        context = super(NoteMixin, self).get_context_data(**kwargs)
        context.update({
            'notes': Note.objects.filter(owner=self.request.user).order_by('-pub_date'),
        })

        return context
