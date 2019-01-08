#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

import functools
import json
import os
import textwrap

import requests

# I want to be able to export my pocket stuff (at least my links and tags)

# https://getpocket.com/developer/docs/authentication
# https://getpocket.com/developer/docs/v3/retrieve

# 2019-01-05: Postponing pocket work while I work on WiSRE and machine learning course


format_json = functools.partial(json.dumps, indent=2, sort_keys=True)


def format_prepared_request(req):
    """Pretty-format 'requests.PreparedRequest'

    Example:
        res = requests.post(...)
        print(format_prepared_request(res.request))

        req = requests.Request(...)
        req = req.prepare()
        print(format_prepared_request(res.request))
    """
    headers = '\n'.join(f'{k}: {v}' for k, v in req.headers.items())
    content_type = req.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        body = format_json(json.loads(req.body))
    else:
        body = req.text
    s = textwrap.dedent("""
    REQUEST
    =======
    {method} {url}
    {headers}
    {body}
    """).strip()
    s = s.format(
        method=req.method,
        url=req.url,
        headers=headers,
        body=body,
    )
    return s


def format_response(resp):
    """Pretty-format 'requests.Response'"""
    headers = '\n'.join(f'{k}: {v}' for k, v in resp.headers.items())
    content_type = resp.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        body = format_json(resp.json())
    else:
        body = resp.text
    s = textwrap.dedent("""
    RESPONSE
    ========
    {status_code}
    {headers}
    {body}
    """).strip()

    s = s.format(
        status_code=resp.status_code,
        headers=headers,
        body=body,
    )
    return s


def main():
    consumer_key = os.environ['KEY_pocket_backup_consumer_key']
    redirect_uri = 'pocket_backup:authorizationFinished'
    base_url = 'https://getpocket.com'

    session = requests.Session()
    session.timeout = 30
    session.headers.update({
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Accept': 'application/json',
    })

    with session:
        res = session.post(
            f'{base_url}/v3/oauth/request',
            json={
                'consumer_key': consumer_key,
                'redirect_uri': redirect_uri,
            }
        )

    print(format_prepared_request(res.request))
    print(format_response(res))

    # print(res.json())


if __name__ == "__main__":
    main()

