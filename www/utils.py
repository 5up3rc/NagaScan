# -*- coding: utf-8 -*-

import bleach
from reform import HtmlEncode

def content_escape(content):
    if isinstance(content, list):
        escaped_content = []
        for item in content:
            escaped_item = {}
            for key, value in item.items():
                escaped_item[key] = bleach.clean(value)
            escaped_content.append(escaped_item)
    elif isinstance(content, str):
        escaped_content = bleach.clean(content)
    else:
        escaped_content = content
    return escaped_content

def html_encode(content):
    if isinstance(content, list):
        encode_content = []
        for item in content:
            encode_item = {}
            for key, value in item.items():
                try:
                    encode_item[key] = HtmlEncode(str(value))
                except Exception, err:
                    encode_item[key] = HtmlEncode(value.encode('utf-8'))
            encode_content.append(encode_item)
    elif isinstance(content, str):
        try:
            encode_content = HtmlEncode(content)
        except Exception, err:
            encode_content = HtmlEncode(content.encode('utf-8'))
    else:
        encode_content = content
    return encode_content
