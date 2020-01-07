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
"""Facts Carousel Status line (footer)"""

from __future__ import absolute_import, unicode_literals

import time

from gettext import gettext as _

from prompt_toolkit.layout.containers import to_container
from prompt_toolkit.widgets import Label

__all__ = (
    'ZoneLowdown',
)


class ZoneLowdown(object):
    """"""
    def __init__(self, carousel):
        self.carousel = carousel
        self.hot_notif = ''
        self.notif_expiry = None

    def standup(self):
        pass

    def update_status(self, hot_notif, clear_after_secs=None):
        self.hot_notif = hot_notif
        self.status_label.text = hot_notif
        self.reset_notif_expiry(clear_after_secs)

    LOWDOWN_NOTIFY_MESSAGE_LIFETIME_SECS = 2.71828

    def reset_notif_expiry(self, clear_after_secs=None):
        if clear_after_secs is None:
            clear_after_secs = ZoneLowdown.LOWDOWN_NOTIFY_MESSAGE_LIFETIME_SECS
        if not clear_after_secs:
            self.notif_expiry = None
        else:
            self.notif_expiry = time.time() + clear_after_secs

    # ***

    def selectively_refresh(self):
        # Clear status messages after timeout.
        if self.notif_expiry and time.time() >= self.notif_expiry:
            self.hot_notif = ''  # So format_lowdown_text prints PK.
            formatted_text = self.format_lowdown_text()
            self.update_status(hot_notif=formatted_text, clear_after_secs=0)

    # ***

    def rebuild_viewable(self):
        """"""
        formatted_text = self.format_lowdown_text()
        lowdown_container = to_container(self.assemble_lowdown(formatted_text))
        return lowdown_container

    def assemble_lowdown(self, footer_text=''):
        self.status_label = Label(
            text=footer_text,
            style='class:footer',
        )
        return self.status_label

    def format_lowdown_text(self):
        """"""
        def _format_lowdown_text():
            # If message notif, show that, until next reset_showing_help,
            # else show current Fact ID and binding hints.
            return show_fact_id_and_binding_hints()

        def show_fact_id_and_binding_hints():
            showing_text = self.hot_notif or showing_fact()
            helpful_text = "[?]: Help / [C-S]: Save / [C-Q]: Quit"

            pad_len = (
                self.carousel.avail_width
                - len(showing_text)
                - len(helpful_text)
            )
            padding = ' ' * pad_len

            hot_notif_or_fact_id_style = self.carousel.add_stylable_classes(
                ppt_widget=None, friendly_name='footer-fact-id',
            )
            # MEH/2019-12-02: (lb): I don't feel like styling the whole bottom line...

            formatted = [
                (hot_notif_or_fact_id_style, showing_text),
                ('', padding),
                ('', helpful_text),
            ]

            return formatted

        def showing_fact():
            curr_edit = self.carousel.edits_manager.curr_edit
            if 'interval-gap' in curr_edit.dirty_reasons:
                context = _('Gap')
                location = _("of {0}").format(curr_edit.format_delta(style=''))
                deleted = _(' [edit to add]')
            else:
                if curr_edit.pk > 0:
                    # 2019-01-26: (lb): For parallelism, I had a similar prefix,
                    #   context = _('Old')
                    # here, but I think it looks funny to call a Fact "Old".
                    context = ''
                    location = _("ID #{0}").format(curr_edit.pk)
                else:
                    num_unstored = self.carousel.edits_manager.edit_fact_count
                    context = _('New')
                    location = _("{0:>{1}} of {2}").format(
                        self.carousel.edits_manager.edit_fact_index + 1,
                        len(str(num_unstored)),
                        num_unstored,
                    )
                deleted = _(' [del]') if curr_edit.deleted else ""
            text = _("{0}{1}Fact {2}{3}").format(
                context, ' ' if context else '', location, deleted,
            )
            return text

        return _format_lowdown_text()
