import requests
from django.conf import settings


def verify_turnstile(token, remote_ip=None):
    if not token or not settings.TURNSTILE_SECRET_KEY:
        return False

    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': settings.TURNSTILE_SECRET_KEY,
                'response': token,
                'remoteip': remote_ip,
            },
            timeout=10,
        )

        response.raise_for_status()
        result = response.json()

        return result.get('success', False)

    except requests.RequestException:
        return False
