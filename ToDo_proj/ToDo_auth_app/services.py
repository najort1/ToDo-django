import requests


def testa_cpf(str_cpf):
    """
    Verifica se um CPF é válido.

    Args:
        str_cpf (str): O CPF a ser verificado.

    Returns:
        bool: True se o CPF for válido, False caso contrário.

    Exemplo:
    cpf = "12345678909"
    is_valid = testa_cpf(cpf)
    print(is_valid)  # Exibe True se o CPF for válido, False caso contrário
    """
    if not str_cpf.isdigit():
        return False
    if len(str_cpf) != 11:
        return False
    soma = 0
    resto = 0
    
    if str_cpf == "00000000000":
        return False
    if str_cpf == "11111111111":
        return False
    if str_cpf == "22222222222":
        return False
    if str_cpf == "33333333333":
        return False
    if str_cpf == "44444444444":
        return False
    if str_cpf == "55555555555":
        return False
    if str_cpf == "66666666666":
        return False
    if str_cpf == "77777777777":
        return False
    if str_cpf == "88888888888":
        return False
    if str_cpf == "99999999999":
        return False
    if len(str_cpf) > 11:
        return False
    
    for i in range(1, 10):
        soma += int(str_cpf[i - 1]) * (11 - i)
    resto = (soma * 10) % 11
    
    if (resto == 10) or (resto == 11):
        resto = 0
    if resto != int(str_cpf[9]):
        return False
    
    soma = 0
    for i in range(1, 11):
        soma += int(str_cpf[i - 1]) * (12 - i)
    resto = (soma * 10) % 11
    
    if (resto == 10) or (resto == 11):
        resto = 0
    if resto != int(str_cpf[10]):
        return False
    
    return True


def via_cep(cep):
    pass