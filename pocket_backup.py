#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

import textwrap
import json
import os
import requests

# I want to be able to export my pocket stuff (at least my links and tags)

# https://getpocket.com/developer/docs/authentication
# https://getpocket.com/developer/docs/v3/retrieve

# 2019-01-05: Postponing pocket work while I work on WiSRE and machine learning course

def format_prepared_request(req):
    """Pretty-format 'requests.models.PreparedRequest'

    Example:
        res = requests.post(...)
        print(format_prepared_request(res.request))

        req = requests.Request(...)
        req = req.prepare()
        print(format_prepared_request(res.request))
    """
    headers = '\n'.join(f'{k}: {v}' for k, v in req.headers.items())
    s = textwrap.dedent("""
    {method} {url}
    {headers}
    {body}
    """).strip()
    s = s.format(
        method=req.method,
        url=req.url,
        headers=headers,
        body=req.body,
    )
    return s


def main():
    consumer_key = os.environ['KEY_pocket_backup_consumer_key']
    redirect_uri = 'pocket_backup:authorizationFinished'
    base_url = 'https://getpocket.com'

    base_headers = {
        'Content-Type' : 'application/json; charset=UTF-8',
        'X-Accept': 'application/json',
    }

    res = requests.post(
        f'{base_url}/v3/oauth/request',
        headers=base_headers,
        data = json.dumps({
            'consumer_key': consumer_key,
            'redirect_uri': redirect_uri,
        })
    )

    print(format_prepared_request(res.request))

    print(res.json())


if __name__ == "__main__":
    main()

