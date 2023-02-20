# cloudguard/__init__.py
# ======================
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
import logging


# Ensure that the library does not emit log messages.
# See: https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("cloudguard").addHandler(logging.NullHandler())
