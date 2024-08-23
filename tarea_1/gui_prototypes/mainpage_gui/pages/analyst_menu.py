
import streamlit as st

def display_general_data_mainpage(datafile):
    st.markdown(
        f"""
        ___
        ## General Dataset Information
        __File name__: {datafile.name} \n
        __Register Amount__: 100 \n
        __Date__: 2021-10-01 \n
        __Time__: 12:00:00 \n
        """
    )

# navigation menu
st.markdown("# App menu")

# Uploader
datafile = st.file_uploader(label="Upload XML data file",
                          type=["xml"],
                          key="upload_xml")


# Buttons to functionalities
st.markdown("## Functions")
with st.container():
    if st.button("Show data statistics", key="option1",use_container_width=True):
        # here goes switch page and pass the datafile
        pass

    if st.button("Search specific data", key="option2", use_container_width=True):
        pass

    if st.button("Feature", key="option3",use_container_width=True):
        pass

    MAX_FILE_SIZE = 150 * 1024 * 1024  # 150MB

    if datafile is not None:
        if datafile.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
        else:
            # avail three option buttons when my_upload is not None
            display_general_data_mainpage(datafile)


