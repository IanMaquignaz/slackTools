# Slack
from slack_sdk.web import WebClient
from slack_sdk.http_retry.jitter import RandomJitter
from slack_sdk.http_retry.builtin_interval_calculators import BackoffRetryIntervalCalculator

# Custom
try:
    from .slackTools import SlackTools
    from .retryHandler import MyRetryHandler
except:
    from slackTools import SlackTools
    from retryHandler import MyRetryHandler


## BOT_TOKEN ##

class SlackTools_bot(SlackTools):
    '''Uses SLACK_BOT_TOKEN 
    Offers more universal access (can post to different channels)'''
    
    _instance_SlackTools_bot = None
    def __new__(cls, *args, **kwargs):
        ''' Initializes SlackTools_webhook
        var slack_token:str = slack API token,
        var slack_default_channel_id:str = ID of the slack channel to use as the default channel,
        var slack_default_channel_name:str = name of the default slack channel,

        var hostname:str = optional identifier for the SlackTools instance, 
            if 'rnd' then it will be randomly generated,
            if '' then it will be kept blank

        notify_init_del:bool = whether to notify on initialization and destruction,
        verbose:bool = be verbose
        '''
        if cls._instance_SlackTools_bot is None:
            cls._instance_SlackTools_bot = super(SlackTools_bot, cls).__new__(cls,*args, **kwargs)
        return cls._instance_SlackTools_bot


    def init_slack(
            self,
            slack_token:str=str(),
            slack_default_channel_id:str=str(),
            slack_default_channel_name:str=str()
        ):
        ''' Initializes SlackTools config for interacting with slack'''

        # Set Slack token
        if slack_token:
            self.slack_token = slack_token
        else:
            self.slack_token = self.config['SLACK_BOT']['TOKEN']

        # Set default Slack channel
        self.slack_default_channel_id = self.check_channel(
            slack_default_channel_id, slack_default_channel_name)

        # Initialize the client
        self.client = WebClient(
            self.slack_token,
            retry_handlers=[
                MyRetryHandler(
                    max_retry_count=3,
                    interval_calculator=BackoffRetryIntervalCalculator(
                        backoff_factor=2,
                        jitter=RandomJitter(),
                    ),
                )
            ]
        )
        if self.verbose:
            result = self.client.auth_test()
            print(
                f"{self.__class__.__name__} authentication test:\n" \
                + f"{result}"
            )


    # Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for chat:write
    def send_message(
            self,
            message:str="Hello World Message!!",
            channel_name:str=str(),
            channel_id:str=str(),
            clickbait:str=str(),
            ):
        '''Sends a (text only) message
        message:str = message to send,
        webhook_token:str = webhook token to use 
            OR string identifier of a webhook token in the config file
        clickbait:str = message to display in slack notification
        '''

        blocks = []
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": message,
                    "emoji": True
                }
            }
        )

        # Send the message
        if not clickbait:
            clickbait = message
        return self.send_block(
            channel_name=channel_name,
            channel_id=channel_id,
            blocks=blocks,
            text=clickbait
        )


    def send_markdown(
        self,
        message="~Hello~ \n> *Markdown* _world_`!!`",
        header=str(),
        channel_name=str(),
        channel_id=str(),
        clickbait=str(),
    ):
        '''Sends a message with markdown formatting
        header:str = message title,
        message:str = message to send,
        webhook_token:str = webhook token to use 
            OR string identifier of a webhook token in the config file
        '''
        blocks = []

        # Copy header (No Markdown)
        if header:
            blocks.append(
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": header
                    }
                }
            )

        # Copy Message
        if message:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            )

        # Send the message
        if not clickbait:
            if header:
                clickbait = header
            else:
                clickbait = message
        return self.send_block(
            channel_name=channel_name,
            channel_id=channel_id,
            blocks=blocks,
            text=clickbait
        )


    def send_block(
            self,
            blocks:list=[],
            attachments:list=[],
            text:str='',
            channel_name:str=str(),
            channel_id:str=str()
        ):
        ''' Send Block Kit primitives to Slack via a webhook 
        See https://api.slack.com/reference/block-kit/blocks#image
        See https://api.slack.com/messaging/composing/layouts#when-to-use-attachments
        '''

        # Convert @name to Slack user ID <@####>
        self.parse_tags(text)
        self.parse_tags(blocks)
        self.parse_tags(attachments)
        try:
            # Convert channel name to channel ID
            channel_id = self.check_channel(
                channel_name=channel_name,
                channel_id=channel_id
            )
            if len(blocks) >= 1 or len(attachments) >= 1 or len(text) >=1:
                # Send the message
                response = self.client.chat_postMessage(
                    channel=channel_id,
                    text=text,
                    blocks=blocks,
                    attachments=attachments,
                )
        except Exception as error:
            print(f"<?> Error sending message to slack: {error}")
            return -1


    # Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for files:write
    def send_file(
            self,
            filepath:str="avatar.png",
            title:str=str(),
            message:str=str(),
            channel_name:str=str(),
            channel_id:str=str()
        ):
        '''
        Uploads a file to Slack.
        Note, requires the `files:write` scope enabled for the token
        '''
        try:
            # Convert channel name to channel ID
            channel_id = self.check_channel(
                channel_name=channel_name,
                channel_id=channel_id
                )

            # Tweak
            if not title:
                title = filepath.split('/')[-1]

            # Upload the file
            response = self.client.files_upload_v2(
                channel=channel_id,
                file=filepath,
                title=title,
                initial_comment=message
            )
            assert response.status_code == 200
        except AssertionError as error:
            print(f"<?> Error uploading file to slack: {error}")
            return -1


# TESTING
if __name__ == "__main__":
    test = SlackTools_bot("slack.key.toml", notify_init_del=False)
    test.send_message()
    test.msg("~Test msg~ \n> *Markdown* _world_`!!` @ian @steve")

    test.send_markdown(message="Nothing to see here")
    test.write("Hello World")

    test.send_file(message="Don't worry about it", filepath="./avatar.png")
