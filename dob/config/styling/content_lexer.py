# -*- coding: utf-8 -*-

# This file is part of 'dob'.
#
# 'dob' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'dob' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'dob'.  If not, see <http://www.gnu.org/licenses/>.

"""Manages loading custom Lexer specified by user's config."""

from __future__ import absolute_import, unicode_literals

from gettext import gettext as _

import inspect

import pygments.lexers
from prompt_toolkit.lexers import Lexer, PygmentsLexer

from ...helpers import dob_in_user_warning
from ...traverser import various_lexers
from . import load_obj_from_internal

__all__ = (
    'load_content_lexer',
)


# If you want to test the lexers, set your config, e.g.,
#   `dob config set editor.lexer rainbow`
# or uncomment one of these:
#  default_name = 'rainbow'
#  default_name = 'truncater'
#  default_name = 'wordwrapper'

def load_content_lexer(controller):
    config = controller.config

    def _load_content_lexer():
        named_lexer = resolve_named_lexer()
        lexer_class = load_obj_from_internal(
            controller,
            obj_name=named_lexer,
            internal=various_lexers,
            default_name=None,
            warn_tell_not_found=False,
        )
        return instantiate_or_try_pygments_lexer(named_lexer, lexer_class)

    def resolve_named_lexer():
        cfg_key_lexer = 'editor.lexer'
        return config[cfg_key_lexer]

    def instantiate_or_try_pygments_lexer(named_lexer, lexer_class):
        if lexer_class is not None:
            controller.affirm(inspect.isclass(lexer_class))
            content_lexer = lexer_class()
            controller.affirm(isinstance(content_lexer, Lexer))
            return content_lexer
        return load_pygments_lexer(named_lexer)

    def load_pygments_lexer(named_lexer):
        # (lb): I'm a reSTie, personally, so we default to that.
        # (Though really the default is set in config/__init__.py.)
        lexer_name = named_lexer or 'RstLexer'
        try:
            return PygmentsLexer(getattr(pygments.lexers, lexer_name))
        except AttributeError:
            msg = _('Not a recognized Pygments lexer: “{0}”').format(lexer_name)
            controller.client_logger.warning(msg)
            dob_in_user_warning(msg)
            return None

    return _load_content_lexer()

