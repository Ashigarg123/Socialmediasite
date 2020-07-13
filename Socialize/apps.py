# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class SocializeConfig(AppConfig):
    name = 'Socialize'

    def ready(self):
        import Socialize.mysignal
