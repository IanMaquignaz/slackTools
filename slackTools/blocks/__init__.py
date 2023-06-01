from .views import *
from .elements import *
from .composition import *


def add_action(elements, blocks:list=[], block_id=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#actions'''
    block = (
        {
            "type": "actions",
            "elements": elements
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    blocks.append(block)
    return blocks


def add_context(blocks:list=[], block_id=None, elements=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#context '''
    block = (
        {
            "type": "context",
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    # An array of image elements and text objects. Maximum number of items is 10.
    if elements:
        block.update(
            {
                "elements": elements
            }
        )
    blocks.append(block)
    return blocks


def add_divider(blocks:list=[], block_id=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#divider '''
    block = (
        {
            "type": "divider"
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    blocks.append(block)
    return blocks


def add_header(message, blocks:list=[], block_id=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#header '''
    block = (
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": message,
                "emoji": True
            }
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    blocks.append(block)
    return blocks


def add_input(element, label=" ", blocks:list=[], block_id=None, isDispatch=False, isOptional=False, hint=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#input '''
    block = (
        {
            "type": "input",
            "optional": True if isOptional else False,
                    "dispatch_action": True if isDispatch else False,
                    "element": element,
                    "label": {
                        "type": "plain_text",
                        "text": label,
                        "emoji": True
                    }
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    if hint:
        block.update(
            {
                "hint": {
                    "type": "plain_text",
                    "text": hint
                }
            }
        )
    blocks.append(block)
    return blocks


def add_section(text, blocks:list=[], block_id=None, fields=None, accessory=None):
    ''' See https://api.slack.com/reference/block-kit/blocks#section'''
    block = (
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
    )
    if block_id:
        block.update(
            {
                "block_id": block_id
            }
        )
    # Some king of weird columns
    # List of text objects
    # https://api.slack.com/reference/block-kit/blocks#section_fields
    if fields:
        block.update(
            {
                "fields": fields
            }
        )
    if accessory:
        block.update(
            {
                "accessory": accessory
            }
        )
    blocks.append(block)
    return blocks
