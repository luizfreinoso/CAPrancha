from django.shortcuts import render
from django.views import generic
from board.models import Board
from django.core.paginator import Paginator

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'boards.html'
    context_object_name = 'board'

    def get_queryset(self):
        pranchas = Board.objects.all().order_by('id').filter(publicado=True)
        p = Paginator(pranchas, 1)
        
        return {
                'prancha' : p.page(1),
                }

def NextView(request, pg):
    
    pranchas = Board.objects.all().order_by('id').filter(publicado=True)
    p = Paginator(pranchas, 1)
    
    ctx = {
        'board' : {
                    'prancha' : p.page(pg)
                  }
          }
    
    return render(request, 'boards.html', ctx)