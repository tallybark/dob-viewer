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
"""Fact Editing State Machine"""

from __future__ import absolute_import, unicode_literals

from collections import namedtuple

from nark.items import Fact

__all__ = [
    'PlaceableFact',
]


FactoidSource = namedtuple(
    'FactoidSource', ('line_num', 'line_raw'),
)


class PlaceableFact(Fact):
    """"""

    def __init__(
        self,
        *args,
        dirty_reasons=None,
        line_num=None,
        line_raw=None,
        **kwargs
    ):
        super(PlaceableFact, self).__init__(*args, **kwargs)
        # For tracking edits between store saves.
        self.dirty_reasons = dirty_reasons or set()
        # For identifying errors in the input.
        self.parsed_source = FactoidSource(line_num, line_raw)
        self.orig_fact = None
        self.next_fact = None
        self.prev_fact = None

    def copy(self, *args, **kwargs):
        """
        """
        new_fact = super(PlaceableFact, self).copy(*args, **kwargs)
        new_fact.dirty_reasons = set(list(self.dirty_reasons))
        new_fact.parsed_source = self.parsed_source
        new_fact.orig_fact = self.orig_fact
        # SKIP: next_fact, prev_fact.
        return new_fact

    def restore_edited(self, restore_fact):
        self.start = restore_fact.start
        self.end = restore_fact.end
        self.activity = restore_fact.activity
        self.tags = list(restore_fact.tags)
        self.description = restore_fact.description
        self.deleted = bool(restore_fact.deleted)
        self.dirty_reasons = set(list(restore_fact.dirty_reasons))
        assert self.orig_fact is restore_fact.orig_fact
        # SKIP: next_fact, prev_fact.

    def squash(self, other, squash_sep=''):
        # (lb): The squash is a useful end user application feature for existing
        # facts, and I'm not sure what else it might be used for, so I'm putting
        # a bunch of asserts here to force you to re-read this comment when next
        # this code blows up because new usage and you realize you can assuredly
        # delete this comment and one or all of these assert and you will likely
        # be just fine.
        assert other.pk is None or other.pk < 0
        assert not self.deleted
        assert not other.deleted
        assert not other.split_from
        # When squashing, the first fact should have a start, but not an end.
        # And we do not care about other; it could have a start, or an end, or
        # neither.
        assert self.start
        assert not self.end

        self.end = other.start or other.end

        if other.activity_name or other.category_name:
            # (lb): MAYBE: Do we care that this is destructive?
            self.activity = other.activity

        self.tags_replace(self.tags + other.tags)

        self.description_squash(other, squash_sep)

        self.dirty_reasons.add('squash')
        if self.end:
            self.dirty_reasons.add('stopped')
            self.dirty_reasons.add('end')

        other.deleted = True
        # For completeness, and to make verification easier.
        other.start = self.start
        other.end = self.end

        other.dirty_reasons.add('deleted-squashed')

    def description_squash(self, other, squash_sep=''):
        if not other.description:
            return
        # (lb): Build local desc. copy, because setter stores None, never ''.
        new_description = self.description or ''
        new_description += squash_sep if new_description else ''
        new_description += other.description
        self.description = new_description
        other.description = None

    @classmethod
    def create_from_factoid(cls, factoid, *args, **kwargs):
        """
        """
        new_fact, err = super(PlaceableFact, cls).create_from_factoid(
            factoid, *args, **kwargs
        )
        if new_fact is not None:
            line_num = 1
            line_raw = factoid
            new_fact.parsed_source = FactoidSource(line_num, line_raw)
        return new_fact, err

    @property
    def dirty(self):
        return self.unstored or len(self.dirty_reasons) > 0

    @property
    def unstored(self):
        return (not self.pk) or (self.pk < 0)

