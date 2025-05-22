
class ESTRError(BaseException):
    pass


class ESTRHourlyLimitReachedError(ESTRError):
    pass


class ESTRForbiddenError(ESTRError):
    pass


class ESTRBadRequestError(ESTRError):
    pass


class ESTRMailValidationError(ESTRError):
    pass


class ESTRDomainError(ESTRError):
    pass


class ESTRAccountError(ESTRError):
    pass


class ESTRJsonInvalidError(ESTRBadRequestError):
    pass


class ESTRFromError(ESTRMailValidationError):
    pass


class ESTRToError(ESTRMailValidationError):
    pass


class ESTRDomainInvalidError(ESTRDomainError):
    pass


class ESTRDomainNotAllowedError(ESTRDomainError):
    pass


class ESTRDomainBlockedError(ESTRDomainError):
    pass


class ESTRDomainSendDisabledError(ESTRDomainError):
    pass


class ESTRAccountInsufficientCreditsError(ESTRAccountError):
    pass


class ESTRAccountSuspendedError(ESTRAccountError):
    pass
