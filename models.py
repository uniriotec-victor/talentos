from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):

    pai = models.ForeignKey('self', null=True, blank=True, limit_choices_to = {'agrupador': True})

    agrupador = models.BooleanField("Agrupador", default='true')

    nome = models.CharField("Nome", max_length = 128)

    def __unicode__(self):
        return self.nome


class FormularioConhecimento(models.Model):
    
    area = models.ForeignKey(Area)

    nivel = models.IntegerField("Nivel")
    
    usuario = models.ForeignKey(User)
    
    '''
    # para fazer unicode do nivel de conhecimento
    def nivel.__unicode__(nivel):
        if nivel == 0:
            return "Nao conheco"
        return "Ouvi falar"
        
    '''
