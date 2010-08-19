from talentos.models import Area, FormularioConhecimento
from django.contrib import admin

def make_published(modeladmin, request, queryset):
    queryset.update(nivel=-1)
make_published.short_description = "Mark selected stories as published"

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pai', 'agrupador')
    
class FormularioConhecimentoAdmin(admin.ModelAdmin):
    list_filter = ['usuario', 'area']
    list_display = ('id','usuario','area','nivel')
    actions = [make_published]

admin.site.register(Area, AreaAdmin)
admin.site.register(FormularioConhecimento, FormularioConhecimentoAdmin)