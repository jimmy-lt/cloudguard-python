# cloudguard/utils.py
# ===================
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


class Namespace(object):
    """Simple object for storing attributes."""

    def __init__(self, **kwargs):
        """Constructor for :class:`cloudguard.utils.Namespace`."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __contains__(self, key) -> bool:
        """Check if the given key is part of the namespace."""
        return key in self.__dict__

    def __eq__(self, other: "Namespace") -> bool:
        """Check if two namespaces are equal."""
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __repr__(self) -> str:
        """Formal representation of the :class:`cloudguard.utils.Namespace`
        class.

        """
        return "".join(
            (
                self.__class__.__name__,
                "(",
                ", ".join(f"{k}={v}" for k, v in self.__dict__.items()),
                ")",
            )
        )

    def update(self, other: "Namespace") -> None:
        """Update the content of the namespace from another one.


        :param other: The namespace object from which to update the current one.
        :type other: ~cloudguard.utils.Namespace


        :return: ``None``


        :raise TypeError: When the object to update from is not a
                          :class:`cloudguard.utils.Namespace` object.

        """
        if not isinstance(other, Namespace):
            raise TypeError(f"expected `{type(self)!r}` got: {type(other)!r}")
        self.__dict__.update(other.__dict__)
