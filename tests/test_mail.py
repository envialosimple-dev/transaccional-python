import os
import pytest
from envialosimple.transaccional import Transaccional
from envialosimple.transaccional.mail import MailParams, Attachment

api_key = os.environ.get('TEST_API_KEY')
from_email = os.environ.get('TEST_FROM_EMAIL')
from_name = os.environ.get('TEST_FROM_NAME')
to_email = os.environ.get('TEST_TO_EMAIL')
to_name = os.environ.get('TEST_TO_NAME')
subject = os.environ.get('TEST_SUBJECT')
template_id = os.environ.get('TEST_TEMPLATE_ID')
reply_to = os.environ.get('TEST_REPLY_TO')
preview_text = os.environ.get('TEST_PREVIEW_TEXT')

estr = Transaccional(api_key)


def test_integrity_nofrom():
    params = MailParams()

    # Omit FROM
    params.to_email = to_email
    params.to_name = to_name
    params.subject = subject
    params.html = "<body>PyTest Integrity</body>"

    with pytest.raises(ValueError):
        estr.mail.send(params)


def test_integrity_noto():
    params = MailParams()

    # Omit TO
    params.from_email = from_email
    params.from_name = from_name
    params.subject = subject
    params.html = "<body>PyTest Integrity</body>"

    with pytest.raises(ValueError):
        estr.mail.send(params)


def test_integrity_nosubject():
    params = MailParams()

    # Omit Subject
    params.to_email = to_email
    params.to_name = to_name
    params.from_email = from_email
    params.from_name = from_name
    params.html = "<body>PyTest Integrity</body>"

    with pytest.raises(ValueError):
        estr.mail.send(params)


def test_integrity_nocontent():
    params = MailParams()

    # Omit Text, HTML and TemplateID
    params.to_email = to_email
    params.to_name = to_name
    params.from_email = from_email
    params.from_name = from_name
    params.subject = subject

    with pytest.raises(ValueError):
        estr.mail.send(params)


def test_integrity_contentconflict():
    params = MailParams()

    # Pass template_id with text and/or html
    params.from_email = from_email
    params.from_name = from_name
    params.to_email = to_email
    params.to_name = to_name
    params.subject = subject
    params.template_id = template_id
    params.html = "<body>PyTest Basic {{sub}}</body>"
    params.text = "PyTest Basic {{sub}}"
    params.context = {'sub': 'substitution'}

    with pytest.raises(ValueError):
        estr.mail.send(params)


def test_basic_send():
    """
    Send an E-Mail
    """
    params = MailParams()
    params.from_email = from_email
    params.from_name = from_name
    params.to_email = to_email
    params.to_name = to_name
    params.subject = subject
    params.reply_to = reply_to
    params.preview_text = preview_text
    params.html = "<body>PyTest Basic {{sub}}</body>"
    params.text = "PyTest Basic {{sub}}"
    params.context = {'sub': 'substitution'}

    outcome = estr.mail.send(params)

    assert (type(outcome) is dict)
    assert ('id' in outcome)
    assert ('queued' in outcome)
    assert (outcome['queued'] is True)


def test_attachment_send():
    """
    Send E-Mail with attachment
    """
    html = '<body><img src="cid:logo"/>PyTest Attachment {{sub}}</body>'
    text = "PyTest Attachment {{sub}}"

    # Use alternative construction
    params = MailParams(
        from_email=from_email, from_name=from_name,
        to_email=to_email, to_name=to_name,
        subject=subject, html=html, text=text,
        context={'sub': 'substitution'})

    filename = os.path.join(os.getcwd(), 'tests/logo.png')

    with open(filename, 'rb') as image_file:
        attachment_a = Attachment(
            content=image_file.read(),
            disposition=Attachment.ATTACHMENT,
            filename='pic.png')

    with open(filename, 'rb') as image_file:
        attachment_b = Attachment(
            content=image_file.read(),
            disposition=Attachment.INLINE,
            filename='pic.png',
            id='logo')

    params.addAttachment(attachment_a).addAttachment(attachment_b)

    outcome = estr.mail.send(params)

    assert (type(outcome) is dict)
    assert ('id' in outcome)
    assert ('queued' in outcome)
    assert (outcome['queued'] is True)
