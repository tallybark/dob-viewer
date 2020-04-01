# This file exists within 'dob-viewer':
#
#   https://github.com/hotoffthehamster/dob-viewer
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

"""Facts Carousel"""

from gettext import gettext as _

from nark import get_version as get_version_nark

from .. import __resolve_vers__ as resolve_vers_dob

__all__ = (
    'render_carousel_help',
    'NUM_HELP_PAGES',
)


def render_carousel_help():
    carousel_help = _(
        """ ┏━━━━━━━━━ NAVIGATION ━━━━━━━━━┳━━━━ EDITING ━━━━┳━━━━━━━ INTERVAL ━━━━━━━━┓
 ┃ → / ←    Next/Previous Fact  ┃  [e] Edit Fact  ┃   Add/Subtract 1 min.   ┃
 ┃ j / k      Same as → / ←     ┠─────────────────╂─────────────────────────┨
 ┃ ↑ / ↓    Move Cursor Up/Down ┃    Or edit:     ┃  To Start: Shift → / ←  ┃
 ┃ h / l      Same as ↑ / ↓     ┃  [a]  act@gory  ┃  To End:    Ctrl → / ←  ┃
 ┃ PgUp     Move Cursor Up/Down ┃  [t]  tagslist  ┃  To Both:               ┃
 ┃  PgDn      by pageful        ┃  [d]  descript  ┃       Ctrl-Shift → / ←  ┃
 ┣━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━┻━━━━━┳━━━━━━━━━━━┻━━━━━━━━━┳━━━━━━━━━━━━━━━┫
 ┃  [?] Read   ┃   Ctrl-S  ┃  Ctrl-Q  ┃  [c-p] Split Fact ½ ┃   [u]   Undo  ┃
 ┃  More Help  ┃    Save   ┃   Exit   ┃  [c-e] Empty Fact   ┃  [c-r]  Redo  ┃
 ┣━━━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━┳━━━━━┻━━━━━━━━━━━┳━━━━━━━━━┻━━━━━━━━━━━━━━━┫
 ┃ [g-g]    Jump to First Fact  ┃ H A M S T E R   ┃    H A M S T E R        ┃
 ┃  [G]     Jump to Final Fact  ┃  H A M S T E R  ┃     H A M S T E R       ┃
 ┠──────────────────────────────╂─────────────────┸─────────────────────────┨
 ┃ [Home]   First line Descript ┃  dob v.{dob_vers: <34} ┃
 ┃ [End]    Bottom of Descript. ┃ nark v.{nark_vers: <34} ┃
 ┣━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━┻━━━━━┯━━━━━━━━━┯━━━━━━━━━┳━━━━━━━━━━━━━━━━━┫
 ┃  [?] Close  ┃  [q] Easy  ┃  [c-c]  │  [c-x]  │  [c-v]  ┃   [c-z]  Undo   ┃
 ┃  this Help  ┃    Exit    ┃   Copy  │   Cut   │  Paste  ┃   [c-y]  Redo   ┃
 ┗━━━━━━━━━━━━━┻━━━━━━━━━━━━┻━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━┻━━━━━━━━━━━━━━━━━┛

        """.format(
            dob_vers=resolve_vers_dob()[:34],
            nark_vers=get_version_nark()[:34],
        ).rstrip()
    )
    return carousel_help


NUM_HELP_PAGES = 2

