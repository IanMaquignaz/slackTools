def add_home(title, blocks=[], callback_id=None, private_metadata=None):
    ''' See https://api.slack.com/reference/surfaces/views '''
    view = {
        "type": "home",
        "title": {
                "type": "plain_text",
            "text": title,
            "emoji": True
        },
        "blocks": blocks
    }
    if callback_id:
        view.update(
            {
                "callback_id": callback_id
            }
        )
    if private_metadata:
        view.update(
            {
                "private_metadata": private_metadata
            }
        )
    return view


def add_modal(title, blocks=[], submit=False, callback_id=None, private_metadata=None):
    ''' See https://api.slack.com/reference/surfaces/views '''
    view = {
        "type": "modal",
        "title": {
                "type": "plain_text",
            "text": title,
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Close",
            "emoji": True
        },
        "blocks": blocks
    }
    if callback_id:
        view.update(
            {
                "callback_id": callback_id
            }
        )
    if private_metadata:
        view.update(
            {
                "private_metadata": private_metadata
            }
        )
    if submit:
        view.update(
            {"submit":
             {
                 "type": "plain_text",
                 "text": "Submit",
                 "emoji": True
             }
             }
        )
    return view
