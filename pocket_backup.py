#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

import functools
import logging
import json
import os
import textwrap

import requests

logger = logging.getLogger(__name__)

# I want to be able to export my pocket stuff (at least my links and tags)

# https://getpocket.com/developer/docs/authentication
# https://getpocket.com/developer/docs/v3/retrieve

# 2019-01-05: Postponing pocket work while I work on WiSRE and machine learning course


format_json = functools.partial(json.dumps, indent=2, sort_keys=True)
indent = functools.partial(textwrap.indent, prefix='  ')


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
        try:
            body = format_json(json.loads(req.body))
        except json.JSONDecodeError:
            body = req.body
    else:
        body = req.body
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
        try:
            body = format_json(resp.json())
        except json.JSONDecodeError:
            body = resp.text
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


def log_on_error(resp, *args, **kwargs):
    """Log errors for a request

    This is intended to be used as a requests.Session event hook
    """
    # Get the current logger
    logger = logging.getLogger(__name__)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        logger.error(f'failing request: {format_prepared_request(resp.request)}')
        logger.error(f'failing response: {format_response(resp)}')
        raise


def main():
    consumer_key = os.environ['KEY_pocket_backup_consumer_key']
    redirect_uri = 'pocket_backup:authorizationFinished'
    base_url = 'https://getpocket.com'

    session = requests.Session()
    session.timeout = 30
    session.hooks['response'].append(log_on_error)
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
        # https://getpocket.com/developer/docs/authentication
        # https://medium.com/@alexdambra/getting-your-reading-history-out-of-pocket-using-python-b4253dbe865c

    print(res.json())


if __name__ == "__main__":
    main()

