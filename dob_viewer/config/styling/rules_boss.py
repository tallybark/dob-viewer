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

import editor
import os

from gettext import gettext as _

from config_decorator.config_decorator import ConfigDecorator

from dob_bright.config.fileboss import (
    create_configobj,
    echo_config_obj,
    ensure_file_path_dirred
)
from dob_bright.termio import (
    click_echo,
    dob_in_user_exit,
    dob_in_user_warning,
    highlight_value
)
from dob_bright.termio.config_table import echo_config_decorator_table
from dob_bright.termio.style import attr

from .. import decorate_and_wrap

from .classes_style import (
    load_rules_conf,
    load_style_rules,
    resolve_path_rules
)
from .styling_config import StylingConfig
from .styling_stylit import create_style_rules_object

__all__ = (
    'create_rules_conf',
    'echo_rules_conf',
    'echo_rule_names',
    'echo_rules_table',
    'edit_rules_conf',
)


# *** [CONF] RULES

def echo_rules_conf(controller, rule_name, complete=False):
    config = controller.config

    def _echo_rules_conf():
        config_obj = load_config_obj()
        if config_obj:
            echo_config_obj(config_obj)
        # Else, already printed error message.

    def load_config_obj():
        config_obj, failed = load_rules_conf(config)
        if config_obj:
            return filter_config_obj(config_obj)
        if failed:
            # load_styles_conf prints a ConfigObj error message. Our job is done.
            return None
        return echo_error_no_rules_conf()

    def filter_config_obj(config_obj):
        if not rule_name:
            return config_obj
        new_config = create_configobj(conf_path=None)
        try:
            new_config.merge({rule_name: config_obj[rule_name]})
        except KeyError:
            return echo_error_no_rules_section(rule_name)
        else:
            return new_config

    def echo_error_no_rules_conf():
        msg = _("No rules file at: {0}").format(resolve_path_rules(config))
        dob_in_user_warning(msg)
        return None

    def echo_error_no_rules_section(rule_name):
        msg = _("No matching section “{0}” found in rules file at: {1}").format(
            rule_name, resolve_path_rules(config),
        )
        dob_in_user_warning(msg)
        return None

    # ***

    return _echo_rules_conf()


# *** [CREATE] RULES

def create_rules_conf(controller, force):

    def _create_rules_conf():
        # SIMILAR funcs: See also: ConfigUrable.create_config and
        #   reset_config; and styles_boss.create_styles_conf.
        rules_path = resolve_path_rules(controller.config)
        exit_if_exists_unless_force(rules_path, force)
        ensure_file_path_dirred(rules_path)
        create_rules_file(rules_path)
        echo_path_created(rules_path)

    def exit_if_exists_unless_force(rules_path, force):
        path_exists = os.path.exists(rules_path)
        if path_exists and not force:
            exit_path_exists(rules_path)

    def exit_path_exists(rules_path):
        dob_in_user_exit(_('Rules file already at {}').format(rules_path))

    def create_rules_file(rules_path):
        # Load specified style, or DEFAULT_STYLE if not specified.
        classes_style = create_style_rules_object()
        rule_name = _('Example Style Rule - Showing all built-in options')
        config_obj = decorate_and_wrap(rule_name, classes_style, complete=True)
        config_obj.filename = rules_path
        config_obj.write()

    def echo_path_created(rules_path):
        click_echo(
            _('Initialized basic rules file at {}').format(
                highlight_value(rules_path),
            )
        )

    _create_rules_conf()


# *** [EDIT] RULES

def edit_rules_conf(controller):
    rules_path = resolve_path_rules(controller.config)
    editor.edit(filename=rules_path)
    # If we cared, could call `edited = editor.edit().decode()`, but we're all done!


# *** [LIST] RULES

def echo_rule_names(controller):
    """"""
    def _echo_rule_names():
        rules = load_style_rules(controller)
        print_rules_names(rules, _('User-created rules'))

    def print_rules_names(rules, title):
        click_echo('{}{}{}'.format(attr('underlined'), title, attr('reset')))
        for rule_name in rules.keys():
            click_echo('  ' + highlight_value(rule_name))

    return _echo_rule_names()


# *** [SHOW] RULES

def echo_rules_table(controller, name, table_type):
    def _echo_rules_table():
        if not name:
            rule_name, ruleset = create_example_rule()
        else:
            rule_name, ruleset = fetch_existing_rule()
        print_ruleset_table(rule_name, ruleset)

    def create_example_rule():
        rule_name = _('example')
        ruleset = create_style_rules_object()
        return rule_name, ruleset

    def fetch_existing_rule():
        rules_confobj = load_style_rules(controller)
        styling_rules = StylingConfig(rules_confobj)
        try:
            ruleset = styling_rules.rulesets[name]
        except KeyError:
            exit_rule_unknown(name)
        return name, ruleset

    def exit_rule_unknown(rule_name):
        dob_in_user_exit(_('No rule named “{}”').format(rule_name))

    def print_ruleset_table(rule_name, ruleset):
        condec = ConfigDecorator.create_root_for_section(rule_name, ruleset)
        conf_objs = [condec]
        echo_config_decorator_table(conf_objs, table_type, exclude_section=False)

    _echo_rules_table()

