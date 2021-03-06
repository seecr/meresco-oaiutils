## begin license ##
#
# "Meresco Oai Common" are utils to support "Meresco Oai".
#
# Copyright (C) 2007-2008 SURF Foundation. http://www.surf.nl
# Copyright (C) 2007-2010 Seek You Too (CQ2) http://www.cq2.nl
# Copyright (C) 2007-2009 Stichting Kennisnet Ict op school. http://www.kennisnetictopschool.nl
# Copyright (C) 2009 Delft University of Technology http://www.tudelft.nl
# Copyright (C) 2009 Tilburg University http://www.uvt.nl
# Copyright (C) 2012, 2015, 2018 Seecr (Seek You Too B.V.) http://seecr.nl
# Copyright (C) 2012 Stichting Bibliotheek.nl (BNL) http://www.bibliotheek.nl
# Copyright (C) 2015 Koninklijke Bibliotheek (KB) http://www.kb.nl
#
# This file is part of "Meresco Oai Common"
#
# "Meresco Oai Common" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# "Meresco Oai Common" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with "Meresco Oai Common"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
## end license ##

from ._partition import Partition

def resumptionTokenFromString(s):
    try:
        return ResumptionToken.fromString(s)
    except ResumptionTokenException:
        return None

class ResumptionTokenException(Exception):
    pass

class ResumptionToken(object):
    SHORT = {
        'm': 'metadataPrefix',
        'c': 'continueAfter',
        'f': 'from_',
        'u': 'until',
        's': 'set_',
    }
    ALL_SHORT = dict(p='partition', **SHORT)

    def __init__(self, metadataPrefix='', continueAfter='0', from_='', until='', set_='', partition=None):
        self.metadataPrefix = metadataPrefix
        self.continueAfter = continueAfter
        self.from_ = from_ or '' #blank out "None"
        self.until = until or ''
        self.set_ = set_ or ''
        self.partition = Partition.create(partition)

    def __str__(self):
        return '|'.join("%s%s" % (key, value) for key, value in
                    ((key, getattr(self, attr)) for key, attr in
                        self.ALL_SHORT.items())
                if value is not None)

    def __repr__(self):
        return repr(str(self))

    def __eq__(self, other):
        return \
            ResumptionToken == other.__class__ and \
            self.metadataPrefix == other.metadataPrefix and \
            self.continueAfter == other.continueAfter and \
            self.from_ == other.from_ and \
            self.until == other.until and \
            self.set_ == other.set_ and \
            self.partition == other.partition

    @classmethod
    def fromString(cls, s):
        resumptDict = dict(((part[0], part[1:]) for part in s.split('|') if part))
        if not set(cls.SHORT.keys()).issubset(set(resumptDict.keys())):
            raise ResumptionTokenException()
        return cls(**dict((cls.ALL_SHORT[k],v) for k,v in resumptDict.items()))

__all__ = ['ResumptionToken', 'ResumptionTokenException', 'resumptionTokenFromString']
