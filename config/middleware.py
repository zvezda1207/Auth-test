from django.utils.deprecation import MiddlewareMixin
from jwt import InvalidTokenError, ExpiredSignatureError

from accounts.models import User
from .jwt_utils import decode_access_token


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Устанавливает request.user по JWT из заголовка Authorization.
    Выполняется в process_view (после AuthenticationMiddleware), чтобы не быть
    перезаписанным Django session-auth.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        auth_header = (request.META.get('HTTP_AUTHORIZATION') or '').strip()
        if not auth_header:
            return None

        parts = auth_header.split(None, 1)
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        token = parts[1].strip()
        if not token:
            return None

        try:
            payload = decode_access_token(token)
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None

        user_id = payload.get('user_id')
        if user_id is None:
            return None

        try:
            user = User.objects.get(id=user_id, is_active=True)
            request.user = user
        except User.DoesNotExist:
            return None
        return None
