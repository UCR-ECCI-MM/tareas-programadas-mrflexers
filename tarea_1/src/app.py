from io import BytesIO

import streamlit as st
# import gui

from health_topic.dataset import HealthTopicDataset

# Display file select

# Get path, and pass to load
file = BytesIO()
health_topic_dataset = HealthTopicDataset.from_xml_file(file)

for name, df in health_topic_dataset.dfs.items():
    st.write(name)
    st.dataframe(df)

# Display DF and sidebar with different statistical views over data