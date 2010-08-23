#! /usr/bin/env python

###############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2009 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
Messaging, logging and support.
"""

import sys
import os
import logging
import textwrap

###############################################################################
## LOGGING

_LOGGING_LEVEL_ENVAR="DENDROPY_LOGGING_LEVEL"
_LOGGING_FORMAT_ENVAR="DENDROPY_LOGGING_FORMAT"

def get_logging_level():
    if _LOGGING_LEVEL_ENVAR in os.environ:
        if os.environ[_LOGGING_LEVEL_ENVAR].upper() == "NOTSET":
            level = logging.NOTSET
        elif os.environ[_LOGGING_LEVEL_ENVAR].upper() == "DEBUG":
            level = logging.DEBUG
        elif os.environ[_LOGGING_LEVEL_ENVAR].upper() == "INFO":
            level = logging.INFO
        elif os.environ[_LOGGING_LEVEL_ENVAR].upper() == "WARNING":
            level = logging.WARNING
        elif os.environ[_LOGGING_LEVEL_ENVAR].upper() == "ERROR":
            level = logging.ERROR
        elif os.environ[_LOGGING_LEVEL_ENVAR].upper() == "CRITICAL":
            level = logging.CRITICAL
        else:
            level = logging.NOTSET
    else:
        level = logging.NOTSET
    return level

def get_logger(name="dendropy"):
    """
    Returns a logger with name set as given, and configured
    to the level given by the environment variable _LOGGING_LEVEL_ENVAR.
    """

#     package_dir = os.path.dirname(module_path)
#     config_filepath = os.path.join(package_dir, _LOGGING_CONFIG_FILE)
#     if os.path.exists(config_filepath):
#         try:
#             logging.config.fileConfig(config_filepath)
#             logger_set = True
#         except:
#             logger_set = False
    logger = logging.getLogger(name)
    if not hasattr(logger, 'is_configured'):
        logger.is_configured = False
    if not logger.is_configured:
        level = get_logging_level()
        rich_formatter = logging.Formatter("[%(asctime)s] %(filename)s (%(lineno)d): %(levelname) 8s: %(message)s")
        simple_formatter = logging.Formatter("%(levelname) 8s: %(message)s")
        raw_formatter = logging.Formatter("%(message)s")
        default_formatter = None
        logging_formatter = default_formatter
        if _LOGGING_FORMAT_ENVAR in os.environ:
            if os.environ[_LOGGING_FORMAT_ENVAR].upper() == "RICH":
                logging_formatter = rich_formatter
            elif os.environ[_LOGGING_FORMAT_ENVAR].upper() == "SIMPLE":
                logging_formatter = simple_formatter
            elif os.environ[_LOGGING_FORMAT_ENVAR].upper() == "NONE":
                logging_formatter = None
            else:
                logging_formatter = default_formatter
        else:
            logging_formatter = default_formatter
        if logging_formatter is not None:
            logging_formatter.datefmt='%H:%M:%S'
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(logging_formatter)
        logger.addHandler(ch)
        logger.is_configured = True
    return logger

def deprecation(message, logger_obj=None, stacklevel=3):
    try:
        import warnings
        warnings.warn(message, DeprecationWarning, stacklevel=stacklevel)
    except:
        if logger_obj:
            logger_obj.warning(message)

class ConsoleMessenger(object):

    def __init__(self, name, verbosity):
        self.name = name
        self.verbosity = verbosity
        self.dest1 = sys.stderr
        self.dest2 = None
        if self.name is None:
            initial_indent = ""
        else:
            initial_indent = self.name + ": "
        subsequent_indent = " " * len(initial_indent)
        self.text_wrapper = textwrap.TextWrapper(width=70,
                initial_indent=initial_indent,
                subsequent_indent=subsequent_indent,
                drop_whitespace=True)

    def compose_message(self, msg, wrap=0, newline=True, force=False, prefix=None):
        pass

    def write(self, msg):
        self.send(msg, newline=False)

    def send_multi(self, msg, wrap=0, newline=True, force=False):
        for line in msg:
            self.send(msg=line, wrap=wrap, newline=newline, force=force)

    def send(self, msg, wrap=0, newline=True, force=False, prefix=None):

        if wrap:
            msg = textwrap.fill(msg, width=70)
        if newline:
            suffix = "\n"
        else:
            suffix = ""
        msg = msg + suffix
        if prefix is not None:
            msg = prefix + msg
        if self.dest1:
            self.dest1.write(msg)
        if self.dest2:
            self.dest2.write(msg)

    def send_formatted(self, msg, force=False):
        self.send(msg, wrap=True, force=force)

    def send_error(self, msg, wrap=False):
        self.send(msg, wrap=wrap, force=True)

    def send_warning(self, msg, wrap=False):
        self.send(msg, wrap=wrap, force=True)
