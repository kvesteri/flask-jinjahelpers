from flask import request, url_for
from jinja2 import ChoiceLoader, PackageLoader
from werkzeug.datastructures import MultiDict


def init_jinja_env(env):
    """
    Adds flask_jinjahelpers templates and some utility function to given jinja
    enviroment

    :param env: jinja environment
    """
    env.loader = ChoiceLoader([
        env.loader,
        PackageLoader(
            'flask_jinjahelpers',
            'templates'
        )
    ])
    env.globals.update(
        visible_page_numbers=visible_page_numbers,
        qp_url_for=qp_url_for
    )
    return env


def qp_url_for(endpoint, **kwargs):
    """
    Returns the url for an endpoint but preserves all request query parameters

    kwargs can be used for overriding specific query parameters

    :param endpoint: endpoint to return the url for, eg. user.index
    :param kwargs: dict containing query parameter names as keys
    """
    data = dict(MultiDict(request.args).lists())

    for key, value in kwargs.items():
        data[key] = value
    return url_for(endpoint, **data)


def visible_page_numbers(page, pages, inner_window=3, outer_window=0):
    """
    Takes the current page number and total number of pages, and computes
    an array containing the visible page numbers.  At least three pages on
    either side of the current page as well as the first and last pages
    will be included. For example::

        [1] 2 3 4 5 6 7 ... 42
        1 2 3 4 5 [6] 7 ... 42
        1 ... 4 5 6 [7] 8 9 ... 42
        1 ... 36 37 38 39 [40] 41 42

    :param page: current page number
    :param pages: total number of pages
    """
    window_from = page - inner_window
    window_to = page + inner_window

    if window_to > pages:
        window_from -= window_to - pages
        window_to = pages

    if window_from < 1:
        window_to += 1 - window_from
        window_from = 1
        if window_to > pages:
            window_to = pages

    visible = []

    left_gap_start = min(2 + outer_window, window_from)
    left_gap_end = window_from - 1

    for page in xrange(1, left_gap_start):
        visible.append(page)

    if left_gap_end - left_gap_start > 0:
        visible.append('...')
    elif left_gap_start == left_gap_end:
        visible.append(left_gap_start)

    right_gap_start = min(window_to + 1, pages - outer_window)
    right_gap_end = pages - outer_window - 1

    for page in xrange(left_gap_end + 1, right_gap_start):
        visible.append(page)

    if right_gap_end - right_gap_start > 0:
        visible.append('...')
    elif right_gap_start == right_gap_end:
        visible.append(right_gap_start)

    for page in xrange(right_gap_end + 1, pages + 1):
        visible.append(page)

    return visible
