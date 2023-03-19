# cloudguard/errors.py
# ====================
#
# Copying
# -------
#
# Copyright (c) 2023 cloudguard authors and contributors.
#
# This file is part of the *cloudguard* project.
#
# *cloudguard* is a free software project. You can redistribute it and/or
# modify it following the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY KIND;
# including but not limited to the WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with *cloudguard*.
# If not, see <http://opensource.org/licenses/MIT>.
#
class CloudGuardError(Exception):
    """Base exception class for CloudGuard errors."""

    fmt = "An unspecified error occurred."

    def __init__(self, **kwargs):
        super().__init__(self.fmt.format(**kwargs))


class CloudGuardIOError(CloudGuardError, IOError):
    """Base exception for input/output errors."""

    fmt = "An unspecified I/O error occurred."


class ConfigParseError(CloudGuardIOError):
    """The configuration file could not be parsed."""

    fmt = "Unable to parse configuration file: {path}"
