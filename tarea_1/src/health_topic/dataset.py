from __future__ import annotations

from io import BytesIO
from typing import Dict
from pandas import DataFrame

from .parsing import XmlParser
from .conversion import DictToDataFrameConverter
from .util import replace_in_keys

HEALTH_TOPIC_PK = 'id'

ATTR_PKS = {'site': 'url', 'primary_institute': 'url', 'group': 'id', 'related_topic': 'id', 'information_category': 0}

ATTRS_TO_PRUNE = ['also_called', 'see_reference', 'full_summary',
                  'mesh_heading', 'language_mapped_topic', 'other_language']

RENAMINGS = {
    'meta_desc': 'description',
    'standard_description': 'description',
    'text': 'name',
    0: 'name'
}

CONVERTER = DictToDataFrameConverter


class HealthTopicDataset:

    @classmethod
    def from_dict(cls, health_topic_dict: dict) -> HealthTopicDataset:
        health_topics = health_topic_dict['health_topics']

        # Prunes unwanted attributes
        health_topics = [{k: v for k, v in ht.items() if k not in ATTRS_TO_PRUNE} for ht in health_topics]

        # Because 'site' is nested, it is extracted on its own
        for ht in health_topics:
            if not isinstance(ht['site'], list):
                ht['site'] = [ht['site']]

        sites = [site for ht in health_topics if 'site' in ht for site in ht['site']]
        site_attr = {'information_category': ATTR_PKS['information_category']}

        ht_attrs = ATTR_PKS.copy()
        ht_attrs.pop('information_category', None)

        dfs = {
            **CONVERTER.convert(sites, 'site', site_attr, ATTR_PKS['site']),
            **CONVERTER.convert(health_topics, 'health_topic', ht_attrs, HEALTH_TOPIC_PK)
        }

        normalized_dfs = cls._normalize_dfs(dfs)

        timestamp = health_topic_dict['date_generated']

        return HealthTopicDataset(normalized_dfs, timestamp)

    @classmethod
    def from_xml_file(cls, file: BytesIO) -> HealthTopicDataset:
        health_topic_dict = XmlParser.parse_file(file)
        health_topic_dict = replace_in_keys(health_topic_dict, '-', '_')
        health_topic_dict['health_topics'] = health_topic_dict.pop('health_topic')
        return cls.from_dict(health_topic_dict)

    @staticmethod
    def _normalize_dfs(dfs: Dict[str, DataFrame]) -> Dict[str, DataFrame]:
        dfs['info_cat_site'] = dfs['information_category']
        dfs['site_health_topic'] = dfs['site']
        dfs['prim_inst_health_topic'] = dfs['primary_institute']
        dfs['group_health_topic'] = dfs['group']

        dfs['information_category'] = (dfs['info_cat_site'].drop(columns=['site_url'])
                       .drop_duplicates([0])
                       .reset_index(drop=True))

        dfs['site'] = (dfs['site_health_topic'].drop(columns=['health_topic_id', 'information_category'])
                   .drop_duplicates(['url'])
                   .reset_index(drop=True))

        dfs['primary_institute'] = (dfs['prim_inst_health_topic'].drop(columns=['health_topic_id'])
                        .drop_duplicates(['url'])
                        .reset_index(drop=True))

        dfs['group'] = (dfs['group_health_topic'].drop(columns=['health_topic_id'])
                    .drop_duplicates(['id'])
                    .reset_index(drop=True))

        dfs['health_topic'] = dfs['health_topic'].drop_duplicates(['id']).reset_index(drop=True)

        dfs['site_health_topic'] = (dfs['site_health_topic']
                                    .drop(columns=['information_category', 'language_mapped_url',
                                                   'organization', 'standard_description', 'title']))

        dfs['prim_inst_health_topic'] = dfs['prim_inst_health_topic'].drop(columns=['text'])

        dfs['group_health_topic'] = dfs['group_health_topic'].drop(columns=['url', 'text'])

        dfs['related_topic'] = dfs['related_topic'].drop(columns=['url', 'text'])

        for df in dfs.values():
            renamings = {k: v for k, v in RENAMINGS.items() if k in df.columns.to_list()}
            df.rename(columns=renamings, inplace=True)

        return dfs

    def __init__(self, dfs: Dict[str, DataFrame], timestamp: str):
        """Expects normalized set of DataFrames"""
        self.dfs = dfs
        self.size = dfs['health_topic'].count()
        self.timestamp = timestamp
