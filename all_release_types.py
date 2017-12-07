# -*- coding: utf-8 -*-

PLUGIN_NAME = "All Release Types"
PLUGIN_AUTHOR = "divyinfo"
PLUGIN_DESCRIPTION = u'''<p>Prep all release type related tags. Info mainly extracted from <code>title</code> tag.</p>
<p>Put (live), (live版) or (现场版) and similar things into <code>releasetype</code> tag, if <code>releasetype</code> was not previously set.</p>
<p>This plugin will accept Chinese versions of the wordings.</p>
<p>If <code>releasetype</code> was set but not <code>secondaryreleasetype</code>, <code>secondaryreleasetype</code> will be used to set 'live'. <code>releasetype</code> tag then will become a list.</p>
<p>Stuff like (live清晰版), (男声完美版), (电影「魔兽世界」主题曲) will be also considered to be a part of the <code>releasetype</code> and appended.</p>'''
PLUGIN_VERSION = "0.1"
PLUGIN_API_VERSIONS = ["1.0"]


from picard.log import info, warning, error

from picard.metadata import register_track_metadata_processor

from picard.file import File
from picard.cluster import Cluster, ClusterList

from picard.track import Track
from picard.album import Album

from picard.ui.itemviews import BaseAction, register_album_action, register_cluster_action, register_clusterlist_action, register_track_action, register_file_action

import re, os

def prep_file(file):
    if (isinstance(file, File)):

        # -----------------------------------
        # First check parantheses with 'live'
        # -----------------------------------

        p_live = re.compile(ur'\(\s*([^)]*?)\s*([Ll]ive版本|[Ll]ive版|[Ll]ive|现场版本|现场版|现场)\s*([^)]*?)\s*\)', re.UNICODE)
        m_live = p_live.search(file.metadata['title'].strip())

        if m_live:

            # Set tags first

            _set_tag = False

            if file.metadata['releasetype']:
                # If string, check if it gets stripped into an empty one
                if isinstance(file.metadata['releasetype'], basestring):
                    file.metadata['releasetype'] = file.metadata['releasetype'].strip()
                    if file.metadata['releasetype']:
                        # Appened to list end if the first item is not 'live'
                        if 'live' not in file.metadata['releasetype'].lower():
                            file.metadata['releasetype'] = [file.metadata['releasetype'], 'live']
                        else:
                            _set_tag = True
                    else:
                        # Directly set releasetype tag
                        _set_tag = True
                # More complicated checks when it's already maybe a list
                elif isinstance(file.metadata['releasetype'], list):
                    if len(file.metadata['releasetype']) == 1:
                        # Appened to list end if the first item is not 'live'
                        if 'live' not in file.metadata['releasetype'][1].lower():
                            file.metadata['releasetype'].append('live')
                        else:
                            _set_tag = True
                    elif len(file.metadata['releasetype']) == 2:
                        if 'live' not in file.metadata['releasetype'][1].lower():
                            file.metadata['releasetype'] = file.metadata['releasetype'].insert(1, 'live')
            else:
                _set_tag = True

            if _set_tag:
                # Directly set releasetype tag
                file.metadata['releasetype'] = ['other', 'live']

            # Title replacements

            if m_live.group(1).strip() or m_live.group(3).strip():
                file.metadata['title'] = p_live.sub(ur'(\1\3)', file.metadata['title'].strip()).strip()
            else:
                file.metadata['title'] = p_live.sub('', file.metadata['title'].strip()).strip()


            file.set_pending()

class PrepArtistsAction(BaseAction):
    NAME = 'Check "Live" and all releasetype appendix(inside parantheses)'

    def callback(self, objs):
        for obj in objs:
            if (isinstance(obj, File)):
                prep_file(obj)
            elif (isinstance(obj, Cluster) or \
                isinstance(obj, ClusterList) or \
                isinstance(obj, Track) or \
                isinstance(obj, Album)):
                for f in obj.iterfiles():
                    prep_file(f)

register_file_action(PrepArtistsAction())
register_cluster_action(PrepArtistsAction())
register_clusterlist_action(PrepArtistsAction())

register_track_action(PrepArtistsAction())
register_album_action(PrepArtistsAction())