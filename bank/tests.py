from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Create your tests here.
from .models import Conta


class ContaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Conta.objects.create(conta_id=1234, saldo=500)

    def test_model_content(self):
        conta = Conta.objects.get(conta_id=1234)
        self.assertEqual(conta.saldo, 500)
        self.assertEqual(conta.conta_id, 1234)


class ContaViewSetTest(TestCase):
    def setUp(self):
        Conta.objects.create(conta_id=1235, saldo=500)

    def test_conta_viewset(self):
        url = reverse("conta")
        response = self.client.get(url + "?id=1235")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("conta_id"), 1235)
        self.assertEqual(response.data.get("saldo"), 500)

        # casos de falha com conta inexistente
        response = self.client.get(url + "?id=12")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(url + "?id=iii")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transacao_viewset(self):
        url = reverse("transacao")
        data = {"forma_pagamento": "P", "conta_id": 1236, "valor": 500}
        response = self.client.post(url, data, format="json")

        # caso a conta não exista
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("conta_id"), 1236)
        self.assertEqual(response.data.get("saldo"), 500)

        # as transações
        # fazendo compra de 50 no débito
        data = {"forma_pagamento": "D", "conta_id": 1235, "valor": 50}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Saldo"), 448.5)

        # fazendo uma compra de 100 no crédito
        data = {"forma_pagamento": "C", "conta_id": 1235, "valor": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Saldo"), 343.5)

        # fazendo a compra por pix de 75
        data = {"forma_pagamento": "P", "conta_id": 1235, "valor": 75}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Saldo"), 268.5)

        # forma de pagamento inexistente
        data = {"forma_pagamento": "F", "conta_id": 1235, "valor": 75}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # payload faltando parametro
        data = {"conta_id": 1235, "valor": 75}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
