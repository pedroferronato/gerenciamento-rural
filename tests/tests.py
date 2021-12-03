from app.models.insumo import Insumo


def test_resposta_200_para_pagina_login(client):
    request = client.get('/login')
    
    assert request.status_code == 200


def test_resposta_302_para_tentativa_nao_autorizada_de_acesso_pagina(client):
    request = client.get('/')
    
    assert request.status_code == 302


def test_texto_redirecionamento_na_resposta_para_tentativa_nao_autorizada_de_acesso_pagina(client):
    request = client.get('/')
    
    assert '<a href="/login">' in request.data.decode()


def test_redirecionado_para_pagina_login_caso_nao_autorizado(client):
    request = client.get('/', follow_redirects=True)
    
    assert '/login' in request.request.url
    assert request.status_code == 200


def test_verificar_metodo_formatacao_quantidade_insumo():
    insumo = Insumo(
        quantidade = 10.0,
        unidade_medida = "sacos"
    )

    texto_retorno_esperado = "10 sacos"

    assert insumo.quantidade_formatada() == texto_retorno_esperado


def test_verificar_metodo_formatacao_quantidade_fracionada_insumo():
    insumo = Insumo(
        quantidade = 11.3,
        unidade_medida = "sacos"
    )

    texto_retorno_esperado = "11.3 sacos"

    assert insumo.quantidade_formatada() == texto_retorno_esperado


def test_verificar_metodo_formatacao_valor_total_insumo():
    insumo = Insumo( valor_total = 10.0 )

    texto_retorno_esperado = "R$ 10.00"

    assert insumo.valor_final_formatado() == texto_retorno_esperado


def test_verificar_metodo_formatacao_valor_total_extenso_insumo():
    # Realiza o teste caso valor flutuate seja extenso 
    # (Valor inválido ou gerado pela linguagem)
    # (1.00000001)

    insumo = Insumo( valor_total = 11.2500001 )

    texto_retorno_esperado = "R$ 11.25"

    assert insumo.valor_final_formatado() == texto_retorno_esperado
