# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from haystack.utils import importlib
from django.db.models.loading import get_app, get_model, get_models

__all__ = ['haystack_get_models', 'haystack_load_apps']

APP = 'app'
MODEL = 'model'


def is_app_or_model(label):
    label_bits = label.split('.')

    if len(label_bits) == 1:
        return APP
    elif len(label_bits) == 2:
        try:
            if not get_model(*label_bits):
                return APP
        except LookupError:
            return APP
        return MODEL
    else:
        raise ImproperlyConfigured(
            "'%s' isn't recognized as an app (<app_label>) or model (<app_label>.<model_name>)." % label)


def haystack_get_app_modules():
    """Return the Python module for each installed app"""
    return [importlib.import_module(i) for i in settings.INSTALLED_APPS]


def haystack_load_apps():
    # Do all, in an INSTALLED_APPS sorted order.
    items = []

    for app in settings.INSTALLED_APPS:
        app_label = app.split('.')[-1]

        try:
            get_app(app_label)
        except ImproperlyConfigured:
            continue  # Intentionally allow e.g. apps without models.py

        items.append(app_label)

    return items


def haystack_get_models(label):
    app_or_model = is_app_or_model(label)

    if app_or_model == APP:
        app_mod = get_app(label)
        return get_models(app_mod)
    else:
        app_label, model_name = label.rsplit('.', 1)
        return [get_model(app_label, model_name)]


def haystack_get_model(app_label, model_name):
    return get_model(app_label, model_name)