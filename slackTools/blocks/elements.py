def addElement_button(text, action_id, elements=[], url=None, value=None, style=None, confirm=None):
    ''' See https://api.slack.com/reference/block-kit/block-elements#button '''
    element = (
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            },
            "action_id": action_id
        }
    )
    if value:
        element.update(
            {
                "value": value
            }
        )
    if url:
        element.update(
            {
                "url": url
            }
        )
    if style in ["primary", "danger"]:
        element.update(
            {
                "style": style
            }
        )
    if confirm:
        element.update(
            {
                "confirm": confirm
            }
        )
    elements.append(element)
    return elements


def addElement_checkboxes(options, action_id, options_initial=None, elements=[], url=None, value=None, style=None, confirm=None, focus_on_load=False):
    ''' See https://api.slack.com/reference/block-kit/block-elements#checkboxes '''
    element = (
        {
            "type": "checkboxes",
            "options": options,
                    "action_id": action_id,
                    "focus_on_load": focus_on_load
        }
    )
    if options_initial:
        element.update(
            {
                "initial_options": options_initial
            }
        )
    if url:
        element.update(
            {
                "url": url
            }
        )
    if style in ["primary", "danger"]:
        element.update(
            {
                "style": style
            }
        )

    if confirm:
        element.update(
            {
                "confirm": confirm
            }
        )
    elements.append(element)
    return elements


def addElement_image(image_url, alt_text, elements=[]):
    ''' See https://api.slack.com/reference/block-kit/block-elements#image '''
    element = (
        {
            "type": "image",
            "image_url": image_url,
            "alt_text": alt_text
        }
    )
    elements.append(element)
    return elements


def addElement_input_plainText(action_id, elements=[], initial_value=None, multiline=False, min_length=None, max_length=None, dispatch_action_config=None, focus_on_load=False, placeholder=None):
    ''' See https://api.slack.com/reference/block-kit/block-elements#input '''
    element = (
        {
            "type": "plain_text_input",
            "action_id": action_id,
            "focus_on_load": focus_on_load,
            "multiline": multiline
        }
    )
    if initial_value:
        element.update(
            {
                "initial_value": initial_value
            }
        )
    if min_length:
        element.update(
            {
                "min_length": min_length
            }
        )
    if max_length:
        element.update(
            {
                "max_length": max_length
            }
        )
    if dispatch_action_config:
        element.update(
            {
                "dispatch_action_config": dispatch_action_config
            }
        )
    if placeholder:
        element.update(
            {
                "placeholder": placeholder
            }
        )
    elements.append(element)
    return elements


def addElement_input_url(action_id, elements=[], initial_value=None, placeholder=None, focus_on_load=False, dispatch_action_config=None):
    ''' See https://api.slack.com/reference/block-kit/block-elements#url '''
    element = (
        {
            "type": "url_text_input",
            "action_id": action_id,
            "focus_on_load": focus_on_load,
        }
    )
    if initial_value:
        element.update(
            {
                "initial_value": initial_value
            }
        )
    if dispatch_action_config:
        element.update(
            {
                "dispatch_action_config": dispatch_action_config
            }
        )
    if placeholder:
        element.update(
            {
                "placeholder": placeholder
            }
        )
    elements.append(element)
    return elements
