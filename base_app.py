# Importing pre-process packages

# Streamlit dependencies
import streamlit as st
# Authentication dependencies
import streamlit_authenticator as stauth
from pathlib import Path
import pickle
from nltk import SnowballStemmer, PorterStemmer, LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, TreebankWordTokenizer
import string
import re
import nltk  # Importing nltk for preprocessing the datasets
from nltk.corpus import stopwords  # importing Stopwords
# sns.set()   # setting plot style

# for image
from PIL import Image

# Data dependencies
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import joblib


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

        selection = st.sidebar.radio("Choose Option", options)

        # Building out the "Information" page
        if selection == "Visualisation":
            st.title("Data Analysis")

            uploaded_file = st.file_uploader(
                label="Upload a csv or excel file for analysis", type=['csv', 'xlsx'])
            # Load the a file to the application
            global df
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                except:
                    df = pd.read_excel(uploaded_file)

            # Display the unprocessed data to user
            if st.checkbox('Show raw data'):  # data is hidden if box is unchecked
                # Display the df or ask the user to load the data frame
                try:
                    st.write(df)
                except:
                    st.write("Upload file")
            if st.checkbox('Show insight'):
                raw = pd.read_csv("resources/train.csv")

                st.write("show the data")
                st.title("Tweet Classifery EDA")

                # You can read a markdown file from supporting resources folder
                st.markdown(
                    "This section contains insights on the loaded data")
                st.subheader("First rows of the clean data")
                st.dataframe(raw.head())

                # taking a look at the labels
                st.subheader("Most used words in the Dataset")
                image = Image.open('resources/imgs/word_cloud.png')
                st.image(image, caption='Word Cloud')

                st.subheader("First 5 rows of the Dataset")
                st.write(raw['sentiment'].value_counts())
                st.subheader("Percentage of each group")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("PRO tweets '1' ", "52.25 %", "Supports")
                col2.metric("Nuetral tweets '0' ", "17.55 %",
                            "Neither supports nor refutes", delta_color="off")
                col3.metric("NPOR  '-1' ", "9.08 %",
                            "Do not believe", delta_color="inverse")
                col4.metric("News '2' ", "21.10 %", "Climate change news")
                st.markdown("A countplot of the labels")

                def countplot():
                    fig = plt.figure(figsize=(10, 4))
                    sns.countplot(x="sentiment", data=raw)
                    st.pyplot(fig)
                countplot()

        # Building out the predication page
        if selection == "Prediction":
            st.title("Prediction")
            st.info("Prediction with ML Models")
            option = st.selectbox(
                'Select the model from the Dropdown',
                ('Logistic Regression', 'Vectoriser', 'SVC'))
            # Creating a text box for user input
            tweet_text = st.text_area("Enter Text", "Type Here")

            # model selection options
            if option == 'Logistic Regression':
                model = "resources/logistic_regression.pkl"
            elif option == 'SVC':
                model = "resources/logistic_regression.pkl"
            elif option == 'Vectoriser':
                model = "resources/logistic_regression.pkl"

            if st.button("Classify"):
                # Transforming user input with vectorizer
                vect_text = tweet_cv.transform([tweet_text]).toarray()
                # Load your .pkl file with the model of your choice + make predictions
                # Try loading in multiple models to give the user a choice
                predictor = joblib.load(open(os.path.join(model), "rb"))
                prediction = predictor.predict(vect_text)

                word = ''
                if prediction == 0:
                    word = '"**Neutral**". It neither supports nor refutes the belief of man-made climate change'
                elif prediction == 1:
                    word = '"**Pro**". The tweet supports the belief of man-made climate change'
                elif prediction == 2:
                    word = '**News**. The tweet links to factual news about climate change'
                else:
                    word = 'The tweet do not belief in man-made climate change'

                # When model has successfully run, will print prediction
                # You can use a dictionary or similar structure to make this output
                # more human interpretable.
                st.success("Text Categorized as: {}".format(word))

        if selection == "Contact us":
            st.title("Contact us")
            st.write("The feedback of your experience with our system matters")

            email = st.text_input("Enter you email")
            message = st.text_area("Enter your message")
            st.button("Send")

        if selection == "Documentation":
            st.title("Documentation")
        # logout
        authenticator.logout("Logout", "sidebar")


# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()
