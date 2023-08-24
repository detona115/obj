from django.urls import path

from .viewsets import ContaViewset


conta = ContaViewset.as_view(
    {
        "get": "list",
    }
)

transacao = ContaViewset.as_view(
    {
        "post": "create",
    }
)


urlpatterns = [
    path("conta", conta, name="conta"),
    path("transacao", transacao, name="transacao"),
]
