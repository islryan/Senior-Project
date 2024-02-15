import streamlit as st

# This allows for the background to be gradient
custom_css = """
<style>
[data-testid="stDecoration"] {

    background-color: rgba(0, 0, 0, 0);

}

[data-testid="stAppViewContainer"] {

    background: linear-gradient(to bottom, #787878, #000000); /* Modify gradient colors as needed */

}

[data-testid="stHeader"] {

    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stFileUploadDropzone"] {

    border-style: dashed;
    border-color: grey;
    background-color: rgba(0, 0, 0, 0);

}

[data-testid="baseButton-secondary"] {

    border-style: solid;
    border-color: grey;
    background-color: rgba(0, 0, 0, 0);

</style>
"""

def dashboard():
    # Sets configuration for the Dashboard page
    st.set_page_config(page_title="Dashboard", page_icon=None, layout="centered")
    #Sets gradient background
    st.markdown(custom_css, unsafe_allow_html=True)
    # Custom function to allow a centered title
    st.markdown("<h1 style='text-align: center; color: white;'>NSFW Content Detector</h1>", unsafe_allow_html=True)
    # Collects picture uploaded to the app
    # Can we upload more than 1 picture to streamlit?
    data = st.file_uploader(label = "Upload image here:")

def results():
    None

def main():
    dashboard()

if __name__ == "__main__":
    main()

