from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from ..models import Conta
from .serializers import ContaSerializer


class ContaViewset(ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Conta.objects.all()
        _id = request.query_params.get("id", None)

        try:
            int(_id)                
        except ValueError:
            return Response(
                {"message": "O parametro 'id' deve ser um inteiro"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        conta = get_object_or_404(queryset, conta_id=_id)
        serializer = ContaSerializer(conta)
        return Response(serializer.data)


class TransacaoViewset(ModelViewSet):
    serializer_class = ContaSerializer
    queryset = Conta.objects.all()

    def processar_transacao(self, conta, valor_decrementar):
        if conta.saldo >= valor_decrementar and conta.saldo > 0:
            conta.saldo -= valor_decrementar
            self.queryset.filter(conta_id=conta.conta_id).update(saldo=conta.saldo)
            return Response({"Saldo": conta.saldo}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        data = request.data

        # validação do campo forma_pagamento e valor
        try:
            if not data["forma_pagamento"]:
                raise KeyError
            if data['valor'] <= 0:
                raise ValueError
        except KeyError:
            return Response(
                {"message": "O paramêtro 'forma_pagamento' não está no payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {"message": "O valor da transação não pode ser igual ou inferior a 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data_to_serialize = {"conta_id": data["conta_id"], "saldo": data["valor"]}

        # se não tiver conta cadastrada criar uma
        if (
            not self.queryset.exists() 
            or not self.queryset.filter(conta_id=data["conta_id"]).exists()
        ):
            serializer = ContaSerializer(data=data_to_serialize)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # efetuar as transaçoes

        # recuperar o valor atual do saldo
        conta = self.queryset.filter(conta_id=data["conta_id"]).get()

        match data["forma_pagamento"]:
            case "P":
                return self.processar_transacao(
                    conta=conta, valor_decrementar=data["valor"]
                )

            case "C":
                porcentagem_cobrado = (
                    lambda porcentagem, valor: valor / 100 * porcentagem
                )
                valor_decrementar = data["valor"] + porcentagem_cobrado(
                    5, data["valor"]
                )

                return self.processar_transacao(
                    conta=conta, valor_decrementar=valor_decrementar
                )

            case "D":
                porcentagem_cobrado = (
                    lambda porcentagem, valor: valor / 100 * porcentagem
                )
                valor_decrementar = data["valor"] + porcentagem_cobrado(
                    3, data["valor"]
                )

                return self.processar_transacao(
                    conta=conta, valor_decrementar=valor_decrementar
                )

            case _:
                return Response(
                    {
                        "message": "O paramêtro 'forma_pagamento' tem que ser do tipo string com valores entre 'P', 'C' e 'D'"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
