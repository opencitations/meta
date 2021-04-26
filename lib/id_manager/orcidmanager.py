#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2019, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.


from meta.lib.id_manager.identifiermanager import IdentifierManager
from re import sub, match


class ORCIDManager(IdentifierManager):
    def __init__(self):
        self.p = "orcid:"
        super(ORCIDManager, self).__init__()

    def is_valid(self, id_string):
        orcid = self.normalise(id_string)
        return orcid is not None and \
               match("^([0-9]{4}-){3}[0-9]{3}[0-9X]$", orcid) and \
               ORCIDManager.__check_digit(orcid)

    def normalise(self, id_string, include_prefix=False):
        try:
            orcid_string = sub("[^X0-9]", "", id_string.upper())
            return "%s%s-%s-%s-%s" % (self.p if include_prefix else "",
                                      orcid_string[:4], orcid_string[4:8], orcid_string[8:12], orcid_string[12:16])
        except:  # Any error in processing the ISSN will return None
            return None

    @staticmethod
    def __check_digit(orcid):
        total = 0
        for d in sub("[^X0-9]", "", orcid.upper())[:-1]:
            i = 10 if d == "X" else int(d)
            total = (total + i) * 2
        reminder = total % 11
        result = (12 - reminder) % 11
        return (str(result) == orcid[-1]) or (result == 10 and orcid[-1] == "X")
