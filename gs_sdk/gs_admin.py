from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from random import randint


class GS_Admin:

    def __init__(self, credentials):
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        self.admin_service = build(
            serviceName='admin',
            version='directory_v1',
            credentials=credentials
        )

    def create_user(self, primary_email: str, given_name: str,
                    family_name: str, org_unit_path: str = '/'):

        user_info = {
            'primaryEmail': primary_email,
            'name': {
                'givenName': given_name,
                'familyName': family_name,
            },
            'password': self.password_gen(),
            'changePasswordAtNextLogin': True,
            'orgUnitPath': org_unit_path
        }

        r = self.admin_service.users().insert(body=user_info).execute()

        if r['kind'] == 'admin#directory#user':
            del user_info['changePasswordAtNextLogin']
            del user_info['orgUnitPath']
            del user_info['name']
            return user_info

        else:
            raise Exception(r)

    @staticmethod
    def password_gen():
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower = 'abcdefghijklmnopqrstuvwxyz'
        num = '0123456789'
        psw = ''
        for i in range(3):
            psw += upper[randint(0, 25)]
            psw += lower[randint(0, 25)]
            psw += num[randint(0, 9)]
        return psw
