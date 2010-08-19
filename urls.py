from django.conf.urls.defaults import *

from talentos.views import exibir_formulario_conhecimento, executar_formulario_conhecimento

urlpatterns = patterns('',

					(r'^$', exibir_formulario_conhecimento),
					(r'^executar/$', executar_formulario_conhecimento),
					                    
					)

