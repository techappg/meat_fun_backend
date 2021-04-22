

from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key()


def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        encrypted_text = txt.encode('ascii')
        # encode to urlsafe base64 format
        encrypted_text = base64.b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(txt):
    try:
        # base64 decode
        base64_message = str(txt)
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# def encrypt(txt):
#     try:
#         # convert integer etc to string first
#         txt = str(txt)
#         # get the key from settings
#         cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
#         # #input should be byte, so convert the text to byte
#         encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
#         # encode to urlsafe base64 format
#         encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
#         return encrypted_text
#     except Exception as e:
#         # log the error if any
#         logging.getLogger("error_logger").error(traceback.format_exc())
#         return None
#
#
# def decrypt(txt):
#     try:
#         # base64 decode
#         txt = base64.urlsafe_b64decode(txt)
#         cipher_suite = Fernet(settings.ENCRYPT_KEY)
#         decoded_text = cipher_suite.decrypt(txt).decode("ascii")
#         return decoded_text
#     except Exception as e:
#         # log the error
#         logging.getLogger("error_logger").error(traceback.format_exc())
#         return None

