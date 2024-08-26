from io import BytesIO

import streamlit as st

from health_topic.dataset import HealthTopicDataset

file = BytesIO()
health_topic_dataset = HealthTopicDataset.from_xml_file(file)

site_df = health_topic_dataset._dfs['site']

site_df['description'] = site_df['description'].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)

st.dataframe(site_df)

st.dataframe(health_topic_dataset.get_health_topics(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn()},
                     hide_index=True)

st.dataframe(health_topic_dataset.get_top_info_cat(), hide_index=True)