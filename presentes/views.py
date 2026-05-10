from django.shortcuts import render, redirect
from .models import Contribuicao
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal
import mercadopago
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


def get_mercadopago_sdk():
    return mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)


def home(request):
    """
    Gera PIX apenas uma vez por sessão.
    F5 não duplica contribuição nem pagamento.
    """

    contribuicao_id = request.session.get("contribuicao_id")

    if contribuicao_id:
        contribuicao = Contribuicao.objects.filter(
            id=contribuicao_id,
            status='Pendente'
        ).first()

        if contribuicao and contribuicao.pix_code and contribuicao.qr_code:
            return render(request, 'pix.html', {
                'nome': contribuicao.nome,
                'valor': contribuicao.valor,
                'pix_code': contribuicao.pix_code,
                'qr_code': contribuicao.qr_code
            })

    if request.method == "POST":
        try:
            nome = request.POST.get("nome")
            valor = Decimal(request.POST.get("valor"))

            contribuicao = Contribuicao.objects.create(
                nome=nome,
                valor=valor,
                status='Pendente'
            )

            pagamento_data = {
                "transaction_amount": float(valor),
                "description": "Presente Casamento Jefferson e Carla",
                "payment_method_id": "pix",
                "payer": {
                    "first_name": nome,
                    "email": "comprador@email.com"
                }
            }

            pagamento = get_mercadopago_sdk().payment().create(pagamento_data)
            dados = pagamento["response"]

            contribuicao.pagamento_id = dados["id"]
            contribuicao.pix_code = dados["point_of_interaction"]["transaction_data"]["qr_code"]
            contribuicao.qr_code = dados["point_of_interaction"]["transaction_data"]["qr_code_base64"]
            contribuicao.save()

            request.session["contribuicao_id"] = contribuicao.id

            return render(request, 'pix.html', {
                'nome': nome,
                'valor': valor,
                'pix_code': contribuicao.pix_code,
                'qr_code': contribuicao.qr_code
            })

        except Exception:
            return render(request, 'home.html', {
                'erro': 'Erro ao gerar o pagamento Pix. Tente novamente.'
            })

    return render(request, 'home.html')


def lista(request):
    """
    Painel protegido por senha
    """

    if request.method == "POST":
        senha = request.POST.get("senha")

        if senha == settings.SENHA_PAINEL:
            contribuicoes = Contribuicao.objects.all().order_by('-criado_em')

            total = Contribuicao.objects.filter(
                status='Pago'
            ).aggregate(
                Sum('valor')
            )['valor__sum'] or 0

            total_formatado = (
                f"{total:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            return render(request, 'lista.html', {
                'contribuicoes': contribuicoes,
                'total': total_formatado
            })

        return render(request, 'login_lista.html', {'erro': True})

    return render(request, 'login_lista.html')


def resetar_pix(request):
    request.session.pop("contribuicao_id", None)
    return redirect('home')


@csrf_exempt
def webhook_mercadopago(request):
    """
    Recebe notificações do Mercado Pago
    """

    print("WEBHOOK RECEBIDO")

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print(data)

            pagamento_id = data.get("data", {}).get("id")

            print("ID:", pagamento_id)

            if not pagamento_id:
                return HttpResponse(status=400)

            pagamento = get_mercadopago_sdk().payment().get(pagamento_id)

            status_pagamento = pagamento["response"]["status"]

            print("STATUS:", status_pagamento)

            if status_pagamento == "approved":

                contribuicao = Contribuicao.objects.filter(
                    pagamento_id=str(pagamento_id)
                ).first()

                print("CONTRIBUIÇÃO:", contribuicao)

                if contribuicao:
                    contribuicao.status = "Pago"
                    contribuicao.save()

                    print("PAGAMENTO SALVO")

            return HttpResponse(status=200)

        except Exception as e:
            print("ERRO:", e)
            return HttpResponse(status=500)

    return HttpResponse(status=405)