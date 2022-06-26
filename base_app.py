# Authentication dependencies
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
# Streamlit dependencies
import streamlit as st
import joblib
import os

# Data dependencies
import pandas as pd

# Vectorizer
news_vectorizer = open("resources/tfidfvect.pkl", "rb")
# loading your vectorizer from the pkl file
tweet_cv = joblib.load(news_vectorizer)

# Load your raw data
raw = pd.read_csv("resources/train.csv")

# The main function where we will build the actual app


def main():
    """Tweet Classifier App with Streamlit """

    # Creates a main title and subheader on your page -
    # these are static across all pages
    st.title("Tweet Classifer")
    names = ["Syeni Oswald", "Arome Emmanuel", "Murtala Umar", "explore"]
    usernames = ["soswald", "emmanuel", "Umar", "explore"]

    # load hashed passwords
    file_path = Path(__file__).parent / "hased_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        "home screen", "abcdef", cookie_expiry_days=10)

    names, authentication_status, username = authenticator.login(
        "Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Enter your username and password")

    if authentication_status:
        # Creating sidebar with selection box -
        # you can create multiple pages this way
        options = ["Prediction", "Visualisation",
                   "Documentation", "Contact us"]
        selection = st.sidebar.selectbox("Choose Option", options)

        # Building out the "Information" page
        if selection == "Visualisation":
            st.info("General Information")

            uploaded_file = st.file_uploader(
                label="Upload a csv or excel file for analysis", type=['csv', 'xlsx'])
            # Load the a file to the application
            global df
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                except:
                    df = pd.read_excel(uploaded_file)

            if st.checkbox('Show raw data'):  # data is hidden if box is unchecked
                # will write the df to the page
                try:
                    st.write(df)
                except:
                    st.write("Upload file")

        # Building out the predication page
        if selection == "Prediction":
            st.info("Prediction with ML Models")
            # Creating a text box for user input
            tweet_text = st.text_area("Enter Text", "Type Here")

            if st.button("Classify"):
                # Transforming user input with vectorizer
                vect_text = tweet_cv.transform([tweet_text]).toarray()
                # Load your .pkl file with the model of your choice + make predictions
                # Try loading in multiple models to give the user a choice
                predictor = joblib.load(
                    open(os.path.join("resources/svc_model.pkl"), "rb"))
                prediction = predictor.predict(vect_text)

                # When model has successfully run, will print prediction
                # You can use a dictionary or similar structure to make this output
                # more human interpretable.
                st.success("Text Categorized as: {}".format(prediction))
        # logout
        authenticator.logout("Logout", "sidebar")


# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()
