import streamlit as st
import pandas as pd

st.title("Kassel Illumineers - Swiss Rounds")
st.image("logo.jpg", width=250)

number = st.number_input("Wie viele Spieler*innen treten an?", format="%0.0f")

st.write("Bitte trage die Namen aller Spieler*innen in folgende Tabelle ein:")

empty_name_list=[]
for n in range(int(number)):
    empty_name_list.append({"Vorname": "", "Nachname": ""})

df = pd.DataFrame(empty_name_list)
edited_df = st.data_editor(df)


#st.rerun()