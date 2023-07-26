# Slack
from slack_sdk.webhook import WebhookClient


# Custom
try:
    from .slackTools import SlackTools
    from .retryHandler import MyRetryHandler
except:
    from slackTools import SlackTools
    from retryHandler import MyRetryHandler


## WEBHOOK  ##
class SlackTools_webhook(SlackTools):
    '''Uses generic SLACK_WEBHOOK_TOKEN
    Can post messages (text and markdown ONLY, through blocks and attachments)
    Each slack token can only post to one channel, but SlackTools_webhook can 
    post to multiple channels by using multiple tokens. Add the more tokens to 
    the config file under [SLACK_WEBHOOK] and use their dict key as webhook_token
    when sending messages.  
    '''

    _instance_SlackTools_webhook = None
    def __new__(cls, *args, **kwargs):
        ''' Initializes SlackTools_webhook
        var slack_token:str = slack API token,
        var hostname:str = optional identifier for the SlackTools instance, 
            if 'rnd' then it will be randomly generated,
            if '' then it will be kept blank

        notify_init_del:bool = whether to notify on initialization and destruction,
        verbose:bool = be verbose
        '''
        if cls._instance_SlackTools_webhook is None:
            cls._instance_SlackTools_webhook = super(SlackTools_webhook, cls).__new__(cls)
        return cls._instance_SlackTools

    def init_slack(
            self,
            slack_token:str=str(),
            *args
        ):
        ''' Initializes SlackTools config for interacting with slack'''

        # Set Slack token
        if slack_token:
            self.slack_token = slack_token
        else:
            self.slack_token = self.config['SLACK_WEBHOOK']['TOKEN']


    def check_webhook_token(self, token:str=str()):
        '''Checks webhook token'''
        if token and token in self.config['SLACK_WEBHOOK'].keys():
            return self.config['SLACK_WEBHOOK'][token]
        else:
            # Assume it is correct
            return self.slack_token


    def send_message(
            self,
            message:str="Hello World Message!!",
            webhook_token:str=str(),
            clickbait:str=str(),
            ):
        '''Sends a (text only) message
        message:str = message to send,
        webhook_token:str = webhook token to use 
            OR string identifier of a webhook token in the config file,
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
            webhook_token=webhook_token,
            blocks=blocks,
            text=clickbait
        )


    def send_markdown(
        self,
        message:str="~Hello~ \n> *Markdown* _world_`!!`",
        header:str=str(),
        clickbait:str=str(),
        webhook_token:str=str()
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
            webhook_token=webhook_token,
            blocks=blocks,
            text=clickbait
        )


    def send_block(
            self,
            blocks:list=[],
            attachments:list=[],
            text:str='',
            webhook_token:str=str()
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
            webhook_token = self.check_webhook_token(webhook_token)
            webhook = WebhookClient(webhook_token, timeout=3, retry_handlers=[MyRetryHandler()])
            if len(blocks) >= 1 or len(attachments) >= 1 or len(text) >=1:
                # Send the message
                response = webhook.send(
                    text=text,
                    blocks=blocks,
                    attachments=attachments
                )
                assert response.status_code == 200
                assert response.body == "ok"
        except Exception as error:
            print(f"<?> Error sending message to slack: {error}")
            return -1


# TESTING
if __name__ == "__main__":
    test = SlackTools_webhook("slack.key.toml")
    # test.send_message()
    # test.send_markdown()
    test.write("~Test write~ \n> *Markdown* _world_`!!` @ian")
    test.msg("~Test msg~ \n> *Markdown* _world_`!!` @ian @steve")
