# This file is part of Indico.
# Copyright (C) 2002 - 2015 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from indico.core.db import db
from indico.util.console import cformat
from indico_zodbimport import Importer, convert_to_unicode

from indico_search_invenio.plugin import InvenioSearchPlugin


class InvenioSearchImporter(Importer):
    plugins = {'search', 'search_invenio'}

    def migrate(self):
        self.migrate_settings()

    def migrate_settings(self):
        print cformat('%{white!}migrating settings')
        InvenioSearchPlugin.settings.delete_all()
        opts = self.zodb_root['plugins']['search']._PluginType__plugins['invenio']._PluginBase__options
        InvenioSearchPlugin.settings.set('search_url',
                                         convert_to_unicode(opts['serverUrl']._PluginOption__value).strip())
        type_map = {'public': 'api_public',
                    'private': 'api_private',
                    'redirect': 'redirect'}
        display_mode = type_map[opts['type']._PluginOption__value]
        InvenioSearchPlugin.settings.set('display_mode', display_mode)
        db.session.commit()
