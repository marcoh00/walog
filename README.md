# Walog: WhatsApp conversation logger

Walog logs your WhatsApp messages to JSON files (one line per message). This can be useful for archiving group conversations, for example.

## How to use

Before you can use walog, you will need obtain credentials to be able to login to the WhatsApp service.

### Obtain credentials

This package depends on yowsup, so you will have yowsup-cli installed. To obtain a new phone number/password pair type:

`yowsup-cli registration --requestcode sms --phone CCXXXXXXXX--cc CC -E android`

`CC` is your local country prefix, the `X`es are supposed to represent the other digits of your phone number. Be sure that WhatsApp is not installed on the device with this phone number, as it is possible that you probably won't be able to see WhatsApp's confirmation SMS then.

When you receive the confirmation code via SMS, type:

`yowsup-cli registration --register ZZZZZZZ --phone CCXXXXXXXX --cc CC -E android`

`ZZZZZZZ` is the confirmation code you just received in this example.

### Use walog

Walog's help message looks like this:

```
% walog --help
usage: walog [-h] --phone PHONE --passkey PASSKEY [--output OUTPUT] [--retry]

WhatsApp conversation logger

optional arguments:
  -h, --help            show this help message and exit
  --phone PHONE         Registered WhatsApp Phone Number
  --passkey PASSKEY     Passkey belonging to given number
  --output OUTPUT, -o OUTPUT
                        Output directory to write messages to
  --retry               Try again on errors
```

You can start walog by typing:

`walog --phone "491639999999" --passkey "JajsJJS+==" --output "/home/user/whatsapp_messages" --retry`

This will try to login to the account with the phone number `491639999999` using passkey `JajsJJS+==`. Received messages will be saved to `/home/user/whatsapp_messages`. Walog will try to reconnect to the WhatsApp service in case the connection gets closed for whatever reason.

## Troubleshooting
From time to time, yowsup's Axolotl/encryption library can get a little bit lost, leading to strange errors. Encryption keys are saved in your home directory: `~/.yowsup`. Deleting this directory will lead to a reinitialization of your keyring. Sometimes it helps.