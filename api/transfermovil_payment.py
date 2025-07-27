from django.conf import settings
from datetime import datetime
import hashlib, base64, requests, json


def header():
    date = datetime.now()
    password = '{}{}{}{}{}{}'.format(
        settings.TM_USERNAME,
        date.day, date.month, date.year,
        settings.TM_SEED, settings.TM_SOURCE)

    sha512 = hashlib.sha512()
    sha512.update(password.encode())
    base64_password = base64.b64encode(sha512.digest())

    return {
        "Content-Type": "application/json",
        "username": settings.TM_USERNAME,
        "source": settings.TM_SOURCE,
        "password": base64_password.decode()
    }


def register(amount, phone_number, external_id):
    headers = header()
    if settings.DEBUG:
        amount = min(float(amount), 0.01)

    pay_order = {
        "request": {
            "Amount": float(amount),
            "Phone": "{}".format(short_phone(phone_number)),
            "Currency": "{}".format(settings.TM_CURRENCY),
            "Description": "User {} buy {}".format(phone_number, external_id),
            "ExternalId": "{}".format(external_id),
            "Source": "{}".format(settings.TM_SOURCE),
            "UrlResponse": settings.TM_URL_RESPONSE_TRANSFERMOVIL,
            "ValidTime": 0,
        }
    }

    try:
        response = requests.post(
            settings.TM_CONNECTION,
            data=json.dumps(pay_order),
            headers=headers, verify=False
        )
        print("TM Response time in:", response.elapsed.total_seconds(), "STATUS:", response.status_code)

        if response.status_code == 200 and response.json()['PayOrderResult']['Success']:
            result = response.json()
            qr = dict(
                id_transaccion="{}".format(external_id),
                importe=amount,
                moneda="{}".format(settings.TM_CURRENCY),
                numero_proveedor="{}".format(settings.TM_SOURCE),
                version="1"
            )
            return True, qr, result['PayOrderResult']['OrderId']


        return False, {}, response.json() if response.status_code == 200 else {
            'error': 'payment_failed',
            'status_code': response.status_code,
            'detail': response.text
        }


    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión con TM: {str(e)}")
        return False, {}, {
            'error': 'connection_error',
            'detail': str(e)
        }


def short_phone(phone):
    return phone.replace(" ", "").replace("+", "")