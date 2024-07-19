from django.utils import timezone
from django.http import HttpRequest, HttpResponse

from datetime import timedelta, datetime


def cookie_date(expire_date: datetime) -> str:
    """
    Форматирует дату истечения срока действия cookie в строку, соответствующую формату GMT.

    Args:
        - expire_date (datetime): Дата истечения срока действия.

    Returns:
        - str: Строка даты в формате '%a, %d-%b-%Y %H:%M:%S GMT'.
    """

    return expire_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')


def get_last_city_ids_from_cookie(request: HttpRequest) -> list[int]:
    """
    Извлекает идентификаторы последних городов из cookie.

    Args:
        - request (HttpRequest): Запрос, содержащий cookie.

    Returns:
        - list[int]: Список идентификаторов городов.
    """

    last_city_ids = request.COOKIES.get('last_city_ids', '')
    return [int(city_id) for city_id in last_city_ids.split(',') if city_id.isdigit()]


def set_last_city_cookie(request: HttpRequest, response: HttpResponse, city_id: int) -> None:
    """
    Устанавливает cookie с идентификаторами последних городов.

    Args:
        - request (HttpRequest): Запрос, содержащий существующую cookie.
        - response (HttpResponse): Ответ, в который будет добавлено новое значение cookie.
        - city_id (int): Идентификатор города для добавления в cookie.

    Returns:
        - None
    """

    expire_date = timezone.now() + timedelta(days=7)

    last_city_ids = request.COOKIES.get('last_city_ids', '').split(',')
    last_city_ids = [city_id for city_id in last_city_ids if city_id.isdigit()]

    if str(city_id) in last_city_ids:
        last_city_ids.remove(str(city_id))
    
    last_city_ids.insert(0, str(city_id))
    last_city_ids = last_city_ids[:7]

    response.set_cookie('last_city_ids', ','.join(last_city_ids), expires=cookie_date(expire_date))
