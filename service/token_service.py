

class TokenService:
    def __init__(self):
        from repository import token_repository
        self.token_repository = token_repository

    def generate_token(self, token_data):
        token_obj = self.token_repository.generate_new_token(
            partner_id=token_data['partner_id']
        )
        return token_obj

    def get_data(self, token):
        return self.token_repository.get(token)

    def get_partner_id(self, request):
        return 1
        token_obj = self.get_data(request.query['token'])
        return token_obj.partner_id

    def get_all(self):
        return self.token_repository.get_all()