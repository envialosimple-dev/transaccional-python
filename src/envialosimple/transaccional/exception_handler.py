from .errors import *

ERROR_MAP = {
    'json_invalid': ESTRJsonInvalidError('The JSON sent in the body is invalid.'),
    'from_required': ESTRFromError('It is required to inform the sender of the email (from).'),
    'from_invalid': ESTRFromError('The “from” field has an invalid email value.'),
    'from_email_invalid': ESTRFromError('It is required to inform the sender of the email: (from.email).'),
    'from_email_required': ESTRFromError('The “from.email” field has an invalid email value.'),
    'to_required': ESTRToError('It is required to indicate the recipient of the email (to).'),
    'to_invalid': ESTRToError('The “to” field has an invalid email value.'),
    'to_array_invalid': ESTRToError('The “to” field is an invalid array.'),
    'to_email_required': ESTRToError('It is required to indicate the recipient of the email (to.email).'),
    'to_email_invalid' : ESTRToError('The “to.email” field has an invalid email value.'),
    'domain_invalid': ESTRDomainInvalidError('Incorrect sender. The domain is not the authorized one.'),
    'domain_not_allowed': ESTRDomainNotAllowedError('The domain is not allowed.'),
    'domain_blocked': ESTRDomainBlockedError('The domain is blocked.'),
    'domain_send_disabled': ESTRDomainSendDisabledError('The domain has stopped sending.'),
    'account_hourly_limit_reached': ESTRHourlyLimitReachedError('Hourly limit reached. Please try again later.'),
    'account_insufficient_credits': ESTRAccountInsufficientCreditsError('No more credits available.'),
    'account_suspended': ESTRAccountSuspendedError('The account is suspended.')
}


class ExceptionHandler():
    @staticmethod
    def handle(http_code: int, response: dict) -> None:
        """
        Handles the exceptions based on the HTTP code and response message.
        Raises the corresponding exception if the HTTP code is >= 400.
        """
        response_msg = response.get('msg')

        if http_code == 429:
            raise ESTRHourlyLimitReachedError('Hourly limit reached. Please try again later.')
        if http_code == 403:
            raise ESTRForbiddenError('Make sure API Key is correct and not disabled.')
        if response_msg in ERROR_MAP:
            raise ERROR_MAP[response_msg]

        raise ESTRError(f'The server responded with code {http_code}. Message: {response_msg}')
