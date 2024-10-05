from __future__ import annotations

from io import BytesIO
from typing import Dict
from pandas import DataFrame

import pandas as pd

from ..analysis.parsing import XmlParser
from .conversion import DictToDataFrameConverter
from .search import SearchEngine
from .util import replace_in_keys, list_elems_to_string

HEALTH_TOPIC_PK = 'id'

ATTR_PKS = {'site': 'url', 'primary_institute': 'url', 'group': 'id', 'related_topic': 'id', 'information_category': 0}

ATTRS_TO_PRUNE = ['also_called', 'see_reference', 'mesh_heading', 'language_mapped_topic', 'other_language']

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
        document_dict = XmlParser.parse_file(file)
        health_topics_dict = document_dict['health-topics']
        health_topics_dict = replace_in_keys(health_topics_dict, '-', '_')
        health_topics_dict['health_topics'] = health_topics_dict.pop('health_topic')
        return cls.from_dict(health_topics_dict)

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
        self._dfs = dfs
        self._filtered_hts = dfs['health_topic'][:]
        self._search_engine = SearchEngine(dfs['health_topic'][['id', 'full_summary']]
                                           .rename(columns={'full_summary': 'text'}))
        self.size = dfs['health_topic'].count()
        self.timestamp = timestamp

    def semantic_filter_health_topics(self, query: str) -> HealthTopicDataset:
        self._filtered_hts = self._dfs['health_topic'][:]

        if query and not query.isspace():
            result_ids = self._search_engine.search(query)
            self._filtered_hts = self._filtered_hts[self._filtered_hts['id'].isin(result_ids)]

        return self

    def get_health_topics(self):
        health_topic_df = self._filtered_hts[:]

        title_col = health_topic_df.pop('title')
        health_topic_df.insert(0, 'title', title_col)

        return (health_topic_df.drop(columns=['id', 'full_summary'])
        .rename(
            columns={
                'title': 'Título', 'description': 'Descripción', 'url': 'URL',
                'language': 'Idioma', 'date_created': 'Fecha de Creación'
            }
        ))

    def get_sites(self):
        sites_df = self._dfs['site']

        title_col = sites_df.pop('title')
        sites_df.insert(0, 'title', title_col)

        sites_df['description'] = list_elems_to_string(sites_df['description'])

        return sites_df.rename(
            columns={
                'title': 'Título', 'url': 'URL', 'organization': 'Organización',
                'description': 'Descripción', 'language_mapped_url': 'URL Otro Idioma'
            }
        )

    def get_top_info_cat(self, top: int = 10):
        # Merge site_health_topic with info_cat_site to associate health topics with information categories
        merged_df = pd.merge(
            self._dfs['site_health_topic'],
            self._dfs['info_cat_site'],
            left_on='url',
            right_on='site_url'
        ).rename(
            columns={'name': 'info_cat_name'}
        )[['info_cat_name', 'health_topic_id']]

        # Group by information_category and count the occurrences of health_topic
        category_counts = merged_df.groupby('info_cat_name').size().reset_index(name='count')

        # Get the top 10 information categories by count
        top_ten_categories = (category_counts.nlargest(top, 'count')
                              .reset_index(drop=True)
                              .set_index('info_cat_name'))

        return top_ten_categories
