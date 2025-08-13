import json
from django.http import JsonResponse

class JsonResponseMixin:
    """Mixin para padronizar respostas JSON"""

    def json_error(self, error_message, status_code=400, extra_data=None):
        response_data = {'success': False, 'error': error_message}
        if extra_data:
            response_data.update(extra_data)
        return JsonResponse(response_data, status=status_code)

    def json_success(self, message, data=None):
        response_data = {'success': True, 'message': message}
        if data:
            response_data.update(data)
        return JsonResponse(response_data)

    def validate_json_request(self, request):
        """Valida se a requisição é JSON e retorna o dict carregado"""
        if request.content_type != 'application/json':
            return self.json_error('Formato inválido', 400)
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return self.json_error('Formato JSON inválido', 400)
    
    



