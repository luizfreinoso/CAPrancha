from django.contrib import admin
from board import models

# Register your models here.
class MediaProjetoInline(admin.TabularInline):
    model = models.MediaProjeto
    insert_after = 'descricao'
    verbose_name = "Imagem"
    verbose_name_plural = "Imagens"
    extra = 1

class BoardAdmin(admin.ModelAdmin):
    inlines = [MediaProjetoInline]
    fields = ('user','nome', 'descricao', 'data_ultima_modificacao','publicado')
    list_display = ('id', 'nome','data_criacao', 'pub_date', 'data_ultima_modificacao','publicado', 'user')
    list_filter = ['data_criacao', 'pub_date', 'data_ultima_modificacao', 'publicado']
    search_fields = ['nome', 'descricao']
    change_form_template = 'admin/custom/change_form.html'
    
    class Media:
        css = {
            'all': (
                'css/admin.css',
            )
        }

admin.site.register(models.Board, BoardAdmin)