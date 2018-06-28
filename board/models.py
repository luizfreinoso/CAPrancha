import datetime
import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from  django.core.files.storage import FileSystemStorage

STATIC_CUR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

upload_storage = FileSystemStorage(location=STATIC_CUR_DIR)

from django.db.models import signals
from django.template.defaultfilters import slugify

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
class Board(models.Model):
    user = models.ForeignKey(User)
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    descricao = models.TextField()
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    pub_date = models.DateTimeField('Publicado', default=timezone.now())
    data_ultima_modificacao = models.DateTimeField('Modificado', default=timezone.now())
    publicado = models.BooleanField('Publicado?', default=True)

class MediaProjeto(models.Model):
    board = models.ForeignKey(Board)
    arquivo =  models.FileField(upload_to='media/upload_user', storage=upload_storage, default="media/none.jpg")
    link_site = models.CharField(max_length=1000, blank=True)
    significado = models.CharField(max_length=255, blank=False)
    data_criacao = models.DateTimeField('Submetido', default=timezone.now())
    ordem = models.IntegerField('Ordem', blank=False, default=-1)

# SIGNALS
def board_pre_save(signal, instance, sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    projeto com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""
    if not instance.slug:
        slug = slugify(instance.nome)
        novo_slug = slug
        contador = 0

        while Board.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
            contador += 1
            novo_slug = '%s-%d'%(slug, contador)

        instance.slug = novo_slug

signals.pre_save.connect(board_pre_save, sender=Board)

@receiver(pre_delete, sender=MediaProjeto)
def mediaProjeto_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.arquivo.delete(False)

@receiver(models.signals.pre_save, sender=MediaProjeto)
def mediaProjeto_auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaProjeto` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = MediaProjeto.objects.get(pk=instance.pk).arquivo
    except MediaProjeto.DoesNotExist:
        return False

    new_file = instance.arquivo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)