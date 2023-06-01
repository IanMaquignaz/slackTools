# Standard
import re
import socket
from random_word import RandomWords

# Custom
from . import keys

class SlackTools:
    ''' Slack Class Encompasses config for interacting with slack and
    encapsulates basic routines
    '''
    notify_init_del = True

    def __init__(
            self,
            filepath_slack_keys:str=None,
            slack_token:str=None,
            slack_default_channel_id:str=None,
            slack_default_channel_name:str=None,
            hostname:str=None,
            notify_init_del:bool=True,
            verbose:bool=False
        ):
        ''' Initializes SlackTools
        var slack_token:str = slack API token,
        var slack_default_channel_id:str = ID of the slack channel to use as the default channel,
        var slack_default_channel_name:str = name of the the default channel,

        var hostname:str = optional identifier for the SlackTools instance, 
            if 'rnd' then it will be randomly generated,
            if '' then it will be taken from the system's hostname
            if None then it will be kept blank

        notify_init_del:bool = whether to notify on initialization and destruction,
        verbose:bool = be verbose
        '''
        self.verbose = verbose

        # Load keys
        self.filepath_slack_keys = filepath_slack_keys
        self.config = keys.load(filepath_slack_keys, verbose=verbose)

        # Set hostname for instance
        if hostname and hostname != 'rnd':
            self.hostname = hostname
        elif hostname == '':
            self.hostname=socket.gethostname()
        elif hostname == 'rnd':
            self.hostname = RandomWords().get_random_word()
        else:
            self.hostname = None

        # Initialize slack config
        self.init_slack(
            slack_token,
            slack_default_channel_id,
            slack_default_channel_name
        )

        # Default notification string
        self.notify = ''
        for user in self.config['SLACK_NOTIFICATION']['NOTIFY_ON_EVENT']:
            self.notify += f" {user}"
        self.notify = self.notify.strip()

        # Notify of initialization
        self.notify_init_del = verbose or notify_init_del
        if self.notify_init_del:
            message = f"{self.__class__.__name__} was initialized" \
                    f"{'as '+self.hostname if self.hostname else ''} {self.notify}"
            if self.__class__.__name__ != SlackTools.__name__:
                self.send_markdown(message)
            print(message)


    def init_slack(self, *args):
        ''' Initializes SlackTools config for interacting with slack'''
        if not isinstance(self, SlackTools):
            raise NotImplementedError(
                "Base class SlackTools cannot be used directly. " \
                + "Please use SlackTools_bot or SlackTools_webhook.")


    def __del__(self):
        ''' Notify of destruction '''

        if self.notify_init_del:
            message = f"{self.__class__.__name__} instance" \
                f"{self.hostname+' ' if self.hostname else ''} was terminated {self.notify}"
            if self.__class__.__name__ != SlackTools.__name__:
                self.send_markdown(str(message))
            print(message)


    def parse_tags(self, blocks):
        ''' Parses @name tags and replaces them with the corresponding slack ID'''
        # Regular expression for @name
        expr = r' @([^ ]*)'

        def lookup(name):
            ''' Returns the corresponding slack ID'''
            if name in self.config['SLACK_USERS']:
                return self.config['SLACK_USERS'][name]

            if self.verbose:
                return f"{name} ({self.__class__.__name__}: " \
                    + f"This person is not in the config file ({self.filepath_slack_keys}... )"

            # Return unmodified.
            # Fallback for when the user is not in the config file.
            return f" @{name}"

        # Recursive through blocks
        if isinstance(blocks, list):
            for b in blocks:
                self.parse_tags(b)

        elif isinstance(blocks, dict):
            if "text" in blocks.keys() and isinstance(blocks["text"], str):
                blocks["text"] = re.sub(
                    expr,
                    lambda m: lookup(m.group(1)),
                    blocks["text"]
                )
                if self.hostname:
                    blocks["text"] = f"{self.hostname} :: {blocks['text']}"
                if self.verbose and "type" in blocks.keys() and blocks['type'] != "mrkdwn":
                    print("<?> Warning, Slack @name references only work when text type is mrkdwn")
                    # Danger! Do not send as a message, as this will cause an infinite loop
            for k in blocks.keys():
                if isinstance(blocks[k], list) or isinstance(blocks[k], dict):
                    self.parse_tags(blocks[k])

        elif isinstance(blocks, str):
            return re.sub(
                    expr,
                    lambda m: lookup(m.group(1)),
                    blocks
                )

    def msg(self, text:str):
        ''' Convenience overload for send_message(...) '''
        self.send_message(message=text)

    def write(self, markdown:str):
        '''Convenience overload for send_markdown(...) '''
        self.send_markdown(message=markdown)

    def upload(self, file:str):
        '''Convenience overload for send_file(...) '''
        self.send_file(filepath=file)


    def send_message(self, message:str):
        ''' Echos a (text only) message '''
        print(f"{self.hostname} (Base) :: {message}")


    def send_markdown(self, message, *args):
        ''' Placeholder '''
        raise NotImplementedError(
                "Base class SlackTools.send_markdown(...) cannot be used directly." \
                + "Please use SlackTools_bot or SlackTools_webhook.")


    def send_block(self, *args):
        ''' Placeholder '''
        raise NotImplementedError(
                "Base class SlackTools.send_block(...) cannot be used directly." \
                + "Please use SlackTools_bot or SlackTools_webhook.")


    def send_file(self, filepath, *args):
        ''' Placeholder '''
        raise NotImplementedError(
                "Base class SlackTools.send_file(...) cannot be used directly." \
                + "Please use SlackTools_bot or SlackTools_webhook.")


    def check_channel(self, channel_id:str=None, channel_name:str=None)->str:
        ''' Converts a the slack channel name to a slack channel ID using keys config '''

        if channel_name:
            if channel_name in self.config['SLACK_CHANNEL']:
                return self.config['SLACK_CHANNEL'][channel_name]
            else:
                raise f"<!> Slack channel name {channel_name} is unrecognized and " \
                    + "cannot be converted to a channel ID. Please add it to the " \
                    + "config file ({filepath_slack_keys}) or use the channel_id instead."
        elif channel_id: # Not None
            return channel_id # No conversion necessary
        else:
            # Return default
            return self.config['SLACK_CHANNEL']['SLACK_DEFAULT_CHANNEL_ID']


    def check_WAN(self, host="8.8.8.8", port=53, timeout=3):
        """
        Checks for an internet connection
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(f"<?> SlackTools has no WAN connection! \n<?> Error: {ex}")
            return False


# TESTING
if __name__ == "__main__":
    test = SlackTools("slack.key.toml")
