def addObject_confirmDialogue(title, text, confirm, deny, objs=[], style=None):
    ''' See https://api.slack.com/reference/block-kit/composition-objects#confirm '''
    obj = (
        {
            "title": {
                "type": "plain_text",
                "text": title,
                "emoji": True
            },
            "text": {
                "type": "mrkdwn",
                "text": text
            },
            "confirm": {
                "type": "plain_text",
                "text": confirm,
                "emoji": True
            },
            "deny": {
                "type": "plain_text",
                "text": deny,
                "emoji": True
            }
        }
    )
    if style in ["primary", "danger"]:
        obj.update(
            {
                "style": style
            }
        )
    objs.append(obj)
    return objs


def addObject_text(text, type="mrkdwn", objs=[]):
    ''' See https://api.slack.com/reference/block-kit/composition-objects#text'''
    obj = (
        {
            "type": type,
            "text": text
        }
    )
    if type == "plain_text":
        obj.update(
            {
                "emoji": True
            }
        )
    objs.append(obj)
    return objs
