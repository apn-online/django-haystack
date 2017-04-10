# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from django.core.management import call_command
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    help = "Completely rebuilds the search index by removing the old data and then updating."

    base_options = (
        make_option(
            '--noinput', action='store_false', dest='interactive', default=True,
            help='If provided, no prompts will be issued to the user and the data will be wiped out.'
        ),
        make_option(
            '-u', '--using', action='append', default=[],
            help='Update only the named backend (can be used multiple times). '
                 'By default all backends will be updated.'
        ),
        make_option(
            '-k', '--workers', default=0, type=int,
            help='Allows for the use multiple workers to parallelize indexing. Requires multiprocessing.'
        ),
        make_option(
            '--nocommit', action='store_false', dest='commit',
            default=True, help='Will pass commit=False to the backend.'
        ),
        make_option(
            '-b', '--batch-size', dest='batchsize', type=int,
            help='Number of items to index at once.'
        ),
    )

    option_list = BaseCommand.option_list + base_options

    def handle(self, **options):
        call_command('clear_index', **options)
        call_command('update_index', **options)
