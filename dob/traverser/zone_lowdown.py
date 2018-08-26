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

from gettext import gettext as _

from prompt_toolkit.layout.containers import to_container
from prompt_toolkit.widgets import Label

__all__ = [
    'ZoneLowdown',
]


class ZoneLowdown(object):
    """"""
    def __init__(self, carousel):
        self.carousel = carousel
        self.hot_notif = ''

    def standup(self):
        pass

    def update_status(self, hot_notif):
        self.hot_notif = hot_notif
        self.status_label.text = hot_notif

    # ***

    def selectively_refresh(self):
        # FIXME: Implement this.
        pass

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
            padding = " " * pad_len

            formatted = [
                ('', showing_text),
                ('', padding),
                ('', helpful_text),
            ]

            return formatted

        def showing_fact():
            curr_fact = self.carousel.edits_manager.curr_fact
            if 'interval-gap' in curr_fact.dirty_reasons:
                context = _('Gap')
                location = _("of {0}").format(curr_fact.format_delta(style=''))
            elif curr_fact.pk > 0:
                context = _('Old')
                location = _("ID #{0}").format(curr_fact.pk)
            else:
                num_unstored = self.carousel.edits_manager.curr_fact_group_count
                context = _('New')
                location = _("{1:>{0}} of {2}").format(
                    self.carousel.edits_manager.curr_fact_group_index,
                    len(str(num_unstored)),
                    num_unstored,
                )
            curr_edit = self.carousel.edits_manager.curr_edit
            deleted = _(' [del]') if curr_edit.deleted else ""
            text = _("{0} Fact {1}{2}").format(context, location, deleted)
            return text

        return _format_lowdown_text()

