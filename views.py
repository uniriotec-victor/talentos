from talentos.models import Area, FormularioConhecimento
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.conf import settings

class no_arvore:
    nome = 'nomeArea'
    agrupador = False
    filhos = []
    def __unicode__(self):
        return self.nome

def gerar_formulario_conhecimento(noPai = None):
    if noPai:
        areas = Area.objects.filter(pai = Area.objects.get(nome=noPai)).order_by('agrupador')
    else:
        areas = Area.objects.filter(pai = None).order_by('agrupador')

    lista = []
    for area in areas:
        # import logging
        # logging.debug(noPai)
        if area.agrupador:
        #    logging.debug('agrupador')
        #    logging.debug(area.nome)
            if Area.objects.filter(pai = Area.objects.get(nome=area.nome)):
                no = no_arvore()
                no.nome = area.nome
                no.agrupador = True
                no.filhos = gerar_formulario_conhecimento(area.nome)
                lista.append(no)
        else:
            no = no_arvore()
            no.nome = area.nome
            no.agrupador = False
            no.filhos = []
            lista.append(no)
    return lista

def renderizar_formulario_conhecimento(lista, request):
    texto = ''

    if lista != []:
        for item in lista:
            if item.agrupador:
                texto += '\n<tr><td colspan=\"7\">'
                texto += '\n<fieldset><legend>' + item.nome + '</legend>'
                texto += '\n<table><tr><td></td><td>Nao conheco</td>'
                texto += '\n<td>Ouvi falar</td><td>Nocoes minimas</td>'
                texto += '\n<td>Conhecimento Basico</td><td>Conhecimento intermediario</td>'
                texto += '\n<td>Conhecimento avancado</td></tr>'
                texto += renderizar_formulario_conhecimento(item.filhos, request)
                texto += '\n</table>'
                texto += '\n</fieldset>'
                texto += '\n</td></tr>'
            else:
                texto += '\n<tr><th>' + item.nome +'</th>'
                for i in range(0,6):
                    existe = ''
                    testearea = Area.objects.get(nome=item.nome)
                    verificador = FormularioConhecimento()
                    try:
                        verificador = FormularioConhecimento.objects.get(area = testearea, usuario = request.user, nivel = i)
                    except:
                        pass
                    if (verificador.nivel != None):
                        existe = 'checked'

                    import logging
                    logging.debug(verificador.nivel)
                    logging.debug(i)
                    logging.debug(testearea)
                    logging.debug(request.user)
                    logging.debug(existe)
                    logging.debug('######################')
                    texto += '<td><input type=\"radio\" name=\"'+item.nome+'\" value=\"'+i.__str__()+'\" '+ existe +' /></td>'
                texto += '</tr>'
    return texto

@login_required    
def exibir_formulario_conhecimento(request):

    MEDIA_URL = settings.MEDIA_URL

    formulario = gerar_formulario_conhecimento()
    renderizado = renderizar_formulario_conhecimento(formulario, request)

    #import logging
    #logging.debug('###########################################')
    #logging.debug(formulario)
    #logging.debug('-------------------------------------------')
    #logging.debug(renderizado)
    
    return render_to_response("informacoes/base.html", {'form': renderizado, 'MEDIA_URL': MEDIA_URL})



def executar_formulario_conhecimento(request):
    ''' no model:
        verficiar loop infinito
        verificar se ja existe entrada do mesmo usuario
    '''
    
    MEDIA_URL = settings.MEDIA_URL

    if (request.user.is_authenticated() == False):
        return render_to_response("informacoes/base.html",  {'erro':'Falha ao verificar usuario.',  'MEDIA_URL':MEDIA_URL})

    formulario = request.POST

    for conhecimento in formulario:
        if conhecimento == u'csrfmiddlewaretoken':
            continue
        nConhecimento = formulario[conhecimento]
        nivel = 0
        if nConhecimento == u'1':
            nivel = 1
        if nConhecimento == u'2':
            nivel = 2
        if nConhecimento == u'3':
            nivel = 3
        if nConhecimento == u'4':
            nivel = 4
        if nConhecimento == u'5':
            nivel = 5
        resposta = FormularioConhecimento(
            area = Area.objects.get(nome=conhecimento),
            usuario = request.user,
            nivel = nivel
        )

        #import logging
        #logging.debug("##################")
        #logging.debug(resposta.pk)
        #logging.debug(resposta.area)
        #logging.debug(resposta.usuario)
        #logging.debug(resposta.nivel)
        
        entrada_banco = None

        try:
            entrada_banco = FormularioConhecimento.objects.get(area = Area.objects.get(nome=conhecimento), usuario = request.user)
        except:
            pass
        
        if ( entrada_banco != None):
            entrada_banco.nivel = resposta.nivel
            entrada_banco.save()
        else:
            resposta.save()
        message = 'Formulario enviado com sucesso'
    return render_to_response("informacoes/resultado.html", locals())
