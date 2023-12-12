import requests
import json
from get_currencie_by import get_currencie

currencie = get_currencie()


class APIException(Exception):
  pass


class CryptoConverter:

  @staticmethod
  def get_price(quote=str, base=str, amount=str):
    try:
      amount = float(amount)
    except ValueError:
      raise APIException(f'Мне кажется "{amount}" - это не цифра, '
                         f'Попробуй ешё раз\n\nПример ввода: 10 USD BYN')

    if quote == base:
      raise APIException(f'Невозможно перевести одинаковае валюты {quote}')

    if quote == 'BYN' or base == 'BYN':
      if quote == 'BYN':
        if base not in currencie.keys():
          raise APIException(f'Я не знаю волюту "{base}", '
                             f'Попробуй ешё раз\n\nПример ввода: 10 USD BYN')
        else:
          total_base = round(
              (currencie[base][0] / currencie[base][2]) * amount, 2)
      else:
        if quote not in currencie.keys():
          raise APIException(f'Я не знаю волюту "{quote}", '
                             f'Попробуй ешё раз\n\nПример ввода: 10 USD BYN')
        else:
          total_base = round(
              (currencie[quote][2] / currencie[quote][0]) * amount, 2)
    else:
      if quote not in currencie.keys():
        raise APIException(f'Я не знаю волюту "{quote}", '
                           f'Попробуй ешё раз\n\nПример ввода: 10 USD BYN')

      if base not in currencie.keys():
        raise APIException(f'Я не знаю волюту "{base}", '
                           f'Попробуй ешё раз\n\nПример ввода: 10 USD BYN')

      total_base = round(
          ((currencie[quote][2] / currencie[quote][0]) * amount) /
          (currencie[base][2] / currencie[base][0]), 2)
    return total_base
