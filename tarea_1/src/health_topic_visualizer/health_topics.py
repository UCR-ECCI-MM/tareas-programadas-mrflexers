from __future__ import annotations

from .parsing import XmlParser
from .conversion import DictToDataFrameConverter
from .util import replace_in_keys


class HealthTopicDataset:

    @staticmethod
    def from_xml_file(path: str) -> HealthTopicDataset:
        health_topic_dict = XmlParser.parse_file(path)
        health_topic_dict = replace_in_keys(health_topic_dict, '-', '_')
        health_topic_dict['health_topics'] = health_topic_dict.pop('health_topic')
        return HealthTopicDataset(health_topic_dict)

    # @staticmethod
    # def from_dicts?

    def __init__(self, health_topic_dict):
        self.health_topics = health_topic_dict['health_topics']
        self.timestamp = health_topic_dict['date_generated']
        self.size = len(self.health_topics)  # More reliable than 'total'

        # declare dfs