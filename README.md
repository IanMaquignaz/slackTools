
# Getting Started with SlackTools!
This document should get you started with SlackTools in three easy steps

<br>

# Step 1: Installing slackTools
There are a couple ways to install slackTools using pip <br><br>
>pip install via HTTPS:
>```Bash
>python -m pip install --upgrade git+https://github.com/THIS_GIT_REPO.git@OPTIONAL_BRANCH_NAME
>```
>_**If not specifying a branch, omit `@OPTIONAL_BRANCH_NAME`**_

<br>

>pip install via SSH:
>```Bash
>python -m pip install --upgrade git+ssh://git@github.com/THIS_GIT_REPO.git@OPTIONAL_BRANCH_NAME
>```
>_**If not specifying a branch, omit `@OPTIONAL_BRANCH_NAME`**_

**OR** (if you want/already have a local clone)
> pip install via local clone:
>```Bash
>git clone https://github.com/THIS_GIT_REPO.git
>python -m pip install --upgrade -e slackTools
>```
> <br>
<br>

# STEP 2: Configure your **SLACK KEY** 

* This is done by creating the file __`slack.key.toml`__. For a template of this file, please see `template.slack.key.toml` <br>
* When search for slack keys, SlackTools searches the following locations:
    * 1st: The filepath provided at initialization
    * 2nd: Default storage locations:
        * Locally, under the filename `slack.key.toml` or hidden filename `.slack.key.toml`
        * Globally, in home directory under `~/.slack/slack.key.toml`

If you are going to use SlackTools a lot, across several projects, and/or don't want to pollute your git repo, make the key global and place the file in __`~/.slack/slack.key.toml`__.

## What keys do I need?
You need a webhook key (__easy__) or a bot Token (__*slightly*__ harder, but can post <u>*messages* **and** *files</u>* to pretty much anywhere). <br>

Token  | text | mrkdwn | files/images | blocks | to any user | to any channel 
------------- | -------------  | -------------  | -------------  | -------------  | -------------  | -------------
Webhook  | ✅ | ✅ | ❌ | ✅ | ❌ | ❌
Bot  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅

For __webhook tokens__, see: https://api.slack.com/messaging/webhooks <br>
For __bot tokens__, see: https://api.slack.com/authentication/basics <br>

## Notifications and Channels
The limit the scope of permissions available to SlackTools, automatic searching and conversion of usernames and channels to slack IDs is not supported. That being said, your __`slack.key.toml`__ works as a lookup table and slack IDs are easy to find in the `profile` info of a user and the `about` of a channel. <br>
* For notifying users, SlacksTools converts any reference like `@yourName` to the corresponding ID (ex:  `<@UNGCTYRUHJ>`) of each user.
    * Note! Only works with __mrkdwn__ enabled fields (e.g. send_markdown()).
* For channels, SlacksTools converts destination channel_name `yourChannel` to the corresponding ID (ex: `CNGCTYRJ8G`) when you perform an action (e.g. send_message()).
    * Note, with webhooks, this is done through the `webhook_token` parameter. With bot tokens, this is done through the `channel_id` parameter. 

<br>

# Step 3: Start using SlackTools!
Here are some examples:
> *Using a webhook*:
> ```python
> import slackTools as sT
> slack = sT.SlackTools_webhook()
> slack = SlackTools_webhook(filepath_slack_keys="slack.key.toml")
>
> # Text examples:
> slack.msg("I am a cat")
> slack.send_message("Hello world message!!")
>
> # mrkdwn examples:
> slack.write("I am a __whale__")
> slack.send_markdown("@you your **experiment** is done", channel_id="RESEARCH")
> ``` 
> <br>
> 
<br>

> *Using a bot token*
> ```python
> import slackTools as sT
> slack = sT.SlackTools_bot()
> slack = SlackTools_bot(filepath_slack_keys="slack.key.toml")
>
> # Text examples:
> slack.msg("I am a cat")
> slack.send_message("Hello world message!!")
>
> # mrkdwn examples:
> slack.write("I am a __whale__")
> slack.send_markdown("@you your **experiment** is done", channel_id="RESEARCH")
> 
> # File upload example:
> slack.write("I am a __whale__")
> slack.send_markdown("@you your **experiment** is done", channel_id="RESEARCH")
> ``` 
> <br>
> 
<br>

# Notes 1: How do I learn __mrkdwn__ and Slack's Block Kit?
See https://api.slack.com/reference/block-kit/blocks#image <br>
See https://api.slack.com/messaging/composing/layouts#when-to-use-attachments <br>

# Notes 2: Required Authentication Scopes
With webhooks, the permission scope `incoming-webhook` is added automatically and therefore no permission scopes need to be set. 
With bot tokens, the following scopes may be required:

Required Scope | activity 
------------- | ------------- 
_chat:write_ | Send messages
_im:write_ | Start direct messages with people
_mpim:write_ | Start group direct messages with people
_files:write_ | Upload, edit, and delete files

<br>

# Notes 3: Uninstalling SlackTools
```Bash
python -m pip uninstall slackTools
```

