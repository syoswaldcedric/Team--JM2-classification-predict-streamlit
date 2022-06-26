import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth

names = ["Syeni Oswald", "Arome Emmanuel", "Murtala Umar", "explore"]
usernames = ["soswald", "emmanuel", "Umar", "explore"]
passwords = ["oswald123", "emmanuel123", "Umar123", "explore123"]

# change plain text password to hash password
hashed_password = stauth.Hasher(passwords).generate()
file_path = Path(__file__).parent / "hased_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_password, file)
