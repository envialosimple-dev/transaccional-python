from .http import HttpClient
from .mail import MailParams
from .exception_handler import ExceptionHandler

API_URL = 'https://api.envialosimple.email/api/v1'


class Mail():

    ENDPOINT = '/mail/send'

    def __init__(self, httpClient: HttpClient) -> None:
        self._http = httpClient

    def send(self, mail_params: MailParams) -> dict:
        http_code, response = self._http.post(
            API_URL + self.ENDPOINT, mail_params.to_dict())

        if http_code >= 400:
            ExceptionHandler.handle(http_code, response)

        return response
