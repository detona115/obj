from django.urls import path

from .viewsets import ContaViewset, TransacaoViewset


conta = ContaViewset.as_view({
    'get': 'list',
})

transacao = TransacaoViewset.as_view({
    'post': 'create',
})


urlpatterns = [
    path('conta', conta, name='conta'),
    path('transacao', transacao, name='transacao'),
]
