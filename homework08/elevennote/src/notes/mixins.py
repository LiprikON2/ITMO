from .models import Note


class NoteMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(NoteMixin, self).get_context_data(**kwargs)
        context.update({
            'notes': Note.objects.filter(owner=self.request.user).order_by('-pub_date'),
        })
        
        if 'share_key' in self.request.session:
            context.update({
                'share_key': self.request.session['share_key']
            })
            
        return context
