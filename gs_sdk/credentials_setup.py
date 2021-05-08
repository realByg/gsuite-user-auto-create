from google_auth_oauthlib.flow import InstalledAppFlow


class Credentials_Setup:

    def __init__(self):
        self.flow = None

    def get_auth_url(self, client_id: str, client_secret: str, scopes: list):
        self.flow = InstalledAppFlow.from_client_config(
            client_config={
                'installed': {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
                    'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob', 'http://localhost']
                }
            },
            scopes=scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )
        auth_url, state = self.flow.authorization_url()
        return auth_url

    def get_credentials(self, auth_code: str):
        self.flow.fetch_token(code=auth_code)
        return self.flow.credentials

