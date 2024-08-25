import streamlit as st

from .health_topics import HealthTopicDataset

# Display file select

# Get path, and pass to load
path = ''
health_topic_dataset = HealthTopicDataset.from_xml_file(path)

# Display DF and sidebar with different statistical views over data

"Hello World"