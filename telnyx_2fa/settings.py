import os


PORT = int(os.environ.get('PORT', 8080))
API_KEY = os.environ['TELNYX_API_KEY']
API_TOKEN = os.environ['TELNYX_API_TOKEN']
CONNECTION_ID = os.environ['TELNYX_CONNECTION_ID']

BASE_URL = os.environ['TELNYX_2FA_BASE_URL']
VOICE = os.environ.get('TELNYX_2FA_VOICE', 'female')
DEFAULT_LANGUAGE = os.environ.get('TELNYX_2FA_DEFAULT_LANGUAGE', 'en-US')
DEFAULT_VOICE_PROMPT = os.environ.get('TELNYX_2FA_DEFAULT_VOICE_PROMPT',
                                      ('This is the verification call you '
                                       'requested. Please enter the '
                                       'verification code now. If you did '
                                       'not request this call, please '
                                       'hang up.'))
DEFAULT_SMS_MESSAGE = os.environ.get('TELNYX_2FA_DEFAULT_SMS_MESSAGE',
                                     'Authorization Code:')
VOICE_ANI = os.environ['TELNYX_2FA_VOICE_ANI']
VOICE_TIMEOUT = int(os.environ.get('TELNYX_2FA_VOICE_TIMEOUT', 30))
VOICE_REPEAT_PROMPT = int(os.environ.get('TELNYX_2FA_VOICE_REPEAT_PROMPT', 3))
SMS_ANI = os.environ['TELNYX_2FA_SMS_ANI']
VOICE_TOKEN_DIGITS = int(os.environ.get('TELNYX_2FA_VOICE_TOKEN_DIGITS', 2))
SMS_TOKEN_DIGITS = int(os.environ.get('TELNYX_2FA_SMS_TOKEN_DIGITS', 4))


def get(key, default):
    return os.environ.get(f'TELNYX_2FA_{key}', default)
