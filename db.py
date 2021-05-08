from tinydb import TinyDB, where
from config import CODE_DB_FILE, GS_DB_FILE
import uuid


class GS_Config:

    def __init__(self):
        db = TinyDB(GS_DB_FILE)
        self.gs_config = db.table('GS_Config')

    def add_gs(self, gs_config: dict):
        if self.gs_config.get(where('email') == gs_config['email']):
            raise Exception('Account Exists')
        else:
            self.gs_config.insert(gs_config)

    def get_all(self):
        return self.gs_config.all()

    def remove_gs(self, gs_id: str):
        self.gs_config.remove(where('id') == gs_id)

    def get_gs_config(self):
        gs_config = []
        for config in self.gs_config.all():
            gs = {
                'name': config['name'],
                'id': config['id'],
                'domains': []
            }

            for domain in config['domains']:
                gs['domains'].append(domain['domain_display'])

            gs_config.append(gs)

        return gs_config

    def get_gs(self, gs_id: str):
        return self.gs_config.get(where('id') == gs_id)


class Code:

    def __init__(self):
        db = TinyDB(CODE_DB_FILE)
        self.code = db.table('Code')

    def add(self, amount: int = 50):
        codes = []
        for i in range(amount):
            code = str(uuid.uuid4())
            self.code.insert({
                'code': code
            })
            codes.append(code)
        return codes

    def get_all(self):
        return [code['code'] for code in self.code.all()]

    def delete(self, code: str):
        self.code.remove(where('code') == code)

    def check(self, code: str):
        if self.code.get(where('code') == code):
            return True
        return False


# if __name__ == '__main__':
#
#     c = Code()
#     # c.add(2)
#     c.delete('50a2fc2c-68f0-4cad-a3da-c6d6dd0c67ca')
#     print(
#         c.check('50a2fc2c-68f0-4cad-a3da-c6d6dd0c67ca')
#     )

#     gc = GS_Config()
#     print(
#         gc.get_site_config()
#     )
    # gc.add_gs({
    #     'email': 'email',  #
    #     'client_id': 'wefwef',  #
    #     'client_secret': 'clientwwefweet',  #
    #     'pickled': 'pickled bytes',
    #     'domains': [
    #         {
    #             'domain': 'a.com',
    #             'domain_display': '*.com',
    #         },
    #         {
    #             'domain': 'b.com',
    #             'domain_display': 'b.*',
    #         }
    #     ],
    #     'name': '母鸡大学',
    #     'org_unit_path': '/',
    #     'id': str(uuid.uuid4()),
    # })
