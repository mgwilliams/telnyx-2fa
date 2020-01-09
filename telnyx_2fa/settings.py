import os


PORT = int(os.environ.get('PORT', 8080))
TELNYX_API_KEY = os.environ['TELNYX_API_KEY']
TELNYX_CONNECTION_ID = os.environ['TELNYX_CONNECTION_ID']

BASE_URL = os.environ['BASE_URL']
VOICE = os.environ.get('VOICE', 'female')
DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'en-US')
DEFAULT_VOICE_PROMPT = os.environ.get('DEFAULT_VOICE_PROMPT',
                                      ('This is the verification call you '
                                       'requested. Please enter the '
                                       'verification code now. If you did '
                                       'not request this call, please '
                                       'hang up.'))
DEFAULT_VOICE_SUCCESS = os.environ.get('DEFAULT_VOICE_SUCCESS', 'Thank you!')
DEFAULT_VOICE_FAILURE = os.environ.get('DEFAULT_VOICE_FAILURE', 'Goodbye!')
DEFAULT_SMS_MESSAGE = os.environ.get('DEFAULT_SMS_MESSAGE',
                                     'Authorization Code:')
VOICE_ANI = os.environ['VOICE_ANI']
VOICE_TIMEOUT = int(os.environ.get('VOICE_TIMEOUT', 10))
VOICE_REPEAT_PROMPT = int(os.environ.get('VOICE_REPEAT_PROMPT', 3))
SMS_ANI = os.environ['SMS_ANI']
VOICE_TOKEN_DIGITS = int(os.environ.get('VOICE_TOKEN_DIGITS', 2))
SMS_TOKEN_DIGITS = int(os.environ.get('SMS_TOKEN_DIGITS', 4))
API_KEY = os.environ['API_KEY']


def get(key, default):
    return os.environ.get(f'{key}', default)
