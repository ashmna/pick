from domain import Token
from datetime import datetime


class TokenRepository:
    def __init__(self):
        pass

    def get(self, token):
        return Token.objects.get(token=token)

    def get_by_partner(self, partner_id):
        return Token.objects.get(partner_id=partner_id)

    def generate_new_token(self, partner_id):
        import hashlib
        try:
            token_obj = self.get_by_partner(partner_id)
        except Token.DoesNotExist:
            token_obj = Token()
            token_obj.enabled = True
            token_obj.partner_id = partner_id
            token_obj.settings = {
                'calculation_velocity': 10
            }
        m = hashlib.md5()
        token_obj.token = m.update(str(datetime.now()))
        token_obj.save()
        return token_obj

    def get_all(self):
        return Token.objects(enabled=True)
