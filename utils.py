import re

def hex_para_rgb(hex):
    """
    Converte uma string hexadecimal (ex: '#FF0000') para uma tupla RGB.
    """
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4))

def permitir_somente_numeros(novo_valor):
    """
    Verifica se o valor digitado contém apenas números.
    Usado para validar entradas como telefone.
    """
    return novo_valor.isdigit() or novo_valor == ""

def formatar_valor_pix(valor_str):
    """
    Formata o valor do PIX como moeda no padrão brasileiro (0,00).
    Caracteres não numéricos são ignorados, exceto a vírgula final.
    """
    numeros = ''.join(filter(str.isdigit, valor_str))

    if not numeros:
        return "0,00"

    if len(numeros) < 3:
        numeros = numeros.zfill(3)

    reais = numeros[:-2]
    centavos = numeros[-2:]
    
    return f"{int(reais)},{centavos}"

def formatar_chave_pix(tipo, valor_str):
    """
    Formata uma chave PIX com base no tipo selecionado.

    Suporta os seguintes tipos de chave:
    - CPF: Formato 000.000.000-00
    - CNPJ: Formato 00.000.000/0000-00
    - Telefone: Formato (00) 00000-0000

    Para os tipos "E-mail" e "Aleatória", o valor original é retornado sem formatação.
    """
    valor = re.sub(r"\D", "", valor_str)

    if tipo == "CPF":
        if len(valor) > 11: valor = valor[:11]
        return f"{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:11]}" if len(valor) >= 11 else valor

    elif tipo == "CNPJ":
        if len(valor) > 14: valor = valor[:14]
        return f"{valor[:2]}.{valor[2:5]}.{valor[5:8]}/{valor[8:12]}-{valor[12:14]}" if len(valor) >= 14 else valor

    elif tipo == "Telefone":
        if len(valor) > 11: valor = valor[:11]
        return f"({valor[:2]}) {valor[2:7]}-{valor[7:11]}" if len(valor) >= 11 else valor

    return valor_str
