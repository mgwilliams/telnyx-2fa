[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# Telnyx 2FA

An example heroku app utilizing [Telnyx's](https://telnyx.com) Call Control and Messaging APIs to perform two-factor authentication via voice or sms.

## Prerequisites

- [Telnyx](https://telnyx.com/sign-up) and [Heroku](https://signup.heroku.com/) Accounts.
- A Telnyx [Connection](https://portal.telnyx.com/#/app/connections)
- A Telnyx [Messaging Profile](https://portal.telnyx.com/#/app/messaging)
- A provisioned Telnyx [Phone Number](https://portal.telnyx.com/#/app/numbers/my-numbers), associated with the Connection & Messaging Profile.

## Deployment

This application may be deployed to Heroku by following [this link](https://heroku.com/deploy), or clicking the button above.

Heroku will prompt for an app name (`example-2fa` is used throughout this document) and values for the following environment variables:

- `TELNYX_API_KEY`: Telnyx APIv2 Key
- `TELNYX_API_TOKEN`: Telnyx APIv1 Token
- `TELNYX_CONNECTION_ID`: Telnyx connection ID (from Connection Details)
- `VOICE_ANI`: Number to display for voice calls (in e164 format -- e.g., `+15055551212`). Should be registered with Telnyx.
- `SMS_ANI`: Number to display for SMS messages (in e164 format -- e.g., `+150555512121`). Must be registered & configured with Telnyx.
- `BASE_URL`: Base URL of app, inclluding trailing `/`. E.g., `https://example-2fa.herokuapp.com/`.
- `SMS_TOKEN_DIGITS`: Number of digits for SMS tokens. Default: 6
- `VOICE_TOKEN_DIGITS`: Number of digits for voice tokens. Default: 2
- `VOICE_PROMPT_DE_DE`: Example of a foreign language (German) prompt. Additional environment variables can be added to the app (after initial deployment) to support additional languages.
- `SMS_MESSAGE_DE_DE`: SMS notification message in German.

The Telnyx Connection must be updated with the correct callback URL, e.g.: `https://example-2fa.herokuapp.com/event`.


## Using the API

Once the app is deployed, it will be available at `example-2fa.herokuapp.com` (or a custom domain if configured).

You will need the auto-generated API-Key, which can be obtained by visiting `https://dashboard.heroku.com/apps/example-2fa/settings`
and selecting "Reveal Config Vars".

Note that phone numbers are transmitted in e164 format with a plus (for which the url encoded escape sequence is `%2B`).

To authenticate a number, first obtain the voice & sms links:

```
API_KEY={auto-generated api key}
curl -H "X-API-Key: $API_KEY" "https://example-2fa.herokuapp.com/2fa?to=%2B15055551212"
```

Example Response:
```
{
  "sms": {
    "url": "https://example-2fa.herokuapp.com/2fa/sms?to=%2B15055551212&token=123456&language=en-US",
    "token": "123456"
  },
  "voice": {
    "url": "https://example-2fa.herokuapp.com/2fa/voice?to=%2B15055551212&token=12&language=en-US",
    "token": "12"
  }
}
```

The response will include a url for voice authentication. If the number can receive SMS messages, a url for sms based authentication will be returned as well.

_To authenticate via voice,_ first display the token to the end user with instructions to enter it when prompted by the phone call, then access the voice URL:
```
curl -H "X-API-Key: $API_KEY" "https://example-2fa.herokuapp.com/2fa/voice?to=%2B15055551212&token=12&language=en-US"
```

Example Responses:

Successful Authentication:
```
{"status": "waiting", "uuid": "9959b1d8-ec4a-41e1-a459-0b5fa9892824"}
...
{"status": "success", "uuid": "9959b1d8-ec4a-41e1-a459-0b5fa9892824"}
```

Failed Authentication:
```
{"status": "waiting", "uuid": "e964dbd9-c9ba-42f3-9ee6-0d394501010d"}
...
{"status": "failure", "uuid": "e964dbd9-c9ba-42f3-9ee6-0d394501010d"}
```

Server Failure:
```
{"status": "waiting", "uuid": "e964dbd9-c9ba-42f3-9ee6-0d394501010d"}
...
{"status": "error", "details": [...], "uuid": "e964dbd9-c9ba-42f3-9ee6-0d394501010d"}
```


*Note that multiple "waiting" status lines may be received before receiving "success" or "failure".*

_To authenticate via sms,_ access the SMS URL, and display an input box to the end user:
```
curl -H "X-API-Key: $API_KEY" "https://example-2fa.herokuapp.com/2fa/sms?to=%2B15055551212&token=123456&language=en-US"
```

Example Response:
```
{"status": "ok"}
```

Note that status "ok" only means that the message was sent, it does not indicate succesful authentication of the token. Authentication of the token is performed by comparing the token returned in the initial call to the `/2fa` endpoint to the token entered by the user. 
