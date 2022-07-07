# navigation dependecy
from streamlit_option_menu import option_menu

# Importing pre-process packages

# Streamlit dependencies
import streamlit as st

import string
import re

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

    with st.sidebar:
        selection = option_menu(
            menu_title="Main Menu",
            options=["Prediction", "Visualisation", "About us",
                     "Contact us", "Documentation"],
            icons=["emoji-expressionless",
                   "robot", "people-fill", "phone", "book"],
            menu_icon="cast",
            default_index=0
        )

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

            st.subheader("Classification Distribution")
            st.write(raw['sentiment'].value_counts())

            st.subheader("Percentage of each group")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("PRO tweets '1' ", "52.25 %", "Supports")
            col2.metric("Nuetral tweets '0' ", "17.55 %",
                        "Neither supports nor refutes", delta_color="off")
            col3.metric("ANTI  '-1' ", "9.08 %",
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
            model = "resources/log_reg_model.pkl"
        elif option == 'SVC':
            model = "resources/svc1_model.pkl"
        elif option == 'Vectoriser':
            model = "resources/Logistic_regression.pkl"

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
        col1, col2 = st.columns(2)
        with col1:

            st.subheader("Contact info")
            st.write("Cola Street, Near ATTC,")
            st.write("Adjacent Sociate Generale, Head Office,")
            st.write("Kokomlemle, P.O. Box AN0000, Kenya")
            st.write("Telephone:+233 00 111 2222")
            st.write("WhatsApp:+234 210 12344 1390")
            st.write("Email: eagleanalytics@gmail.com")
            st.write("Website: eagleanalytics.com")
        with col2:
            st.subheader("Send Us")
            email = st.text_input("Enter your email")
            message = st.text_area("Enter your message")
            st.button("Send")

    if selection == "Documentation":
        st.title("Documentation")
        st.subheader("Table of content")
        st.write("1. Get Started")
        st.write("2. Select Page")
        st.write("3. Predict")
        st.write("4. Visualisation")
        st.write("5.About us")
        st.write("")
        st.subheader("1. Get Started")
        st.write(
            "To have access to the developed solutiion first start by login to the system by puting your username and password")
        st.subheader("2. Select Page")
        st.write("Various pages are available in the application. The various ")
        st.subheader("3. Predict")
        st.write(
            "To predict select your the model you want to use for the prediction")
        st.write("Type your text and click on classify")
        st.subheader("4. Visualisation")
        st.write("To visualize a new datas set load an excel or csv file")
        st.write("Click on Show data to visualize the data")
        st.write("Click on Show Insight to have more information on the data")
        st.subheader("5. About us")
        st.write("Send us an email")
        st.write("")

    if selection == "About us":
        st.title("Eagle Analytics")
        st.subheader("Who are we?")
        st.write(
            "Eagle Analytics is a freelance tech startup specialised in Data Science, Machine Learning, Data Analysis, and Business Intelligence. ")
        st.write("Our team of expert scientists and researchers is dedicated to helping companies derive insightful information from existing data. By doing so Eagle Analytics hardwork is oriented in facilitating decision making as well prediction in business setting.")
        st.write(
            "Our vision is to make the world a better place through hidden insight in data")
        st.subheader("Meet the team")
        # team members
        Arome = Image.open('resources/imgs/Arome.png')
        Umar = Image.open('resources/imgs/Umar.png')
        Soala = Image.open('resources/imgs/Soala.png')
        Johnson = Image.open('resources/imgs/Johnson.png')
        Oswald = Image.open('resources/imgs/Oswald.png')
        Silindile = Image.open('resources/imgs/Silindile.png')
        # Arome
        col1, col2 = st.columns(2)
        with col1:
            st.image(Arome)
        with col2:
            st.subheader("Emmanuel Uloko (CEO)")
            st.write("Emmanuel has his PhD in Business Intellingence and over 15 years of experience running most successful businesses like Google, Microsoft, Oracle and Explore AI")
            st.write(
                "With this blend of skills and experience the CEO and his team has helped over 250 startups improve their service")

        # Oswald
        col1, col2 = st.columns(2)
        with col1:
            st.image(Oswald)
        with col2:
            st.subheader("Oswald Cedric Syeni (CTO)")
            st.write("Being a Master holder in Machine learning from the University of Michigan, Oswald developed the machine learning algorithm for Tesla self driving and was the team lead for its implementation")
            st.write("He has also been CTO of numero organizations like Alibaba, Jumia, and Amazone where he has gained practinal knowledge that he put in use for the succcess of the startup")

        # Umar
        col1, col2 = st.columns(2)
        with col1:
            st.image(Umar)
        with col2:
            st.subheader("Murtala Umar Adamu (MD)")
            st.write(
                "Umar has a master in Project Management from Havard University and has applied his knowlege in numerous fortune Startup")
            st.write("During his 30 years of experience he has managed the development of well known and successfull product like Iphone 6, Iphone X, Iphone 11 Pro, and recently Samsung 22 before he moved to Eagle Analytics ")

        # Silindile
        col1, col2 = st.columns(2)
        with col1:
            st.image(Silindile)
        with col2:
            st.subheader("Kuhle Silindile Mbamali (COO)")
            st.write(
                "She has her PhD in Business Administration from Polytechnique University in Canada and is dedicated in successfuly running Business.")
            st.write("She spent the fifteen years of her successful career at Silicon Valley where she has helped the compamy inscrease its revenue by 80 percent")

        # Johnson
        col1, col2 = st.columns(2)
        with col1:
            st.image(Johnson)
        with col2:
            st.subheader("Johnson Amodu (DS)")
            st.write(
                "He has a master of research in Data Science from Tokio University and a graduate student from Explore Data Science Accademy")
            st.write(
                "Over the past seven years he has been part of team team in charged of the Netflix Recommendation System, which has helped the company increase their customer satisfaction by 50 percent")

        # Soala
        col1, col2 = st.columns(2)
        with col1:
            st.image(Soala)
        with col2:
            st.subheader("Oluasoala")
            st.write(
                "He has two masters one in Machine Learning from Tokio University and the other in Statiscal analysis from Havard University.")
            st.write(
                "Over the past six years he has been part of team team in charged of the Netflix Recommendation System, which has helped the company increase their customer satisfaction by 50 percent")


# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()
