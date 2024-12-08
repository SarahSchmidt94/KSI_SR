import streamlit as st
import pandas as pd
import numpy as np

# Title and Image
st.set_page_config(layout="wide")
st.title("Kassel Illumineers - Swiss Rounds")
st.image("logo.jpg", width=250)


# Session State for Results
if "pairs_round1_df" not in st.session_state:
    st.session_state["pairs_round1_df"] = None
if "pairs_round1_df_edited" not in st.session_state:
    st.session_state["pairs_round1_df_edited"] = None
if "round1" not in st.session_state:
    st.session_state["round1"] = None
if "spiele" not in st.session_state:
    st.session_state["spiele"] = None
if "topcut" not in st.session_state:
    st.session_state["topcut"] = None
if "topcut_start" not in st.session_state:
    st.session_state["topcut_start"] = None
if "number" not in st.session_state:
    st.session_state["number"] = None
if "round1_scores" not in st.session_state:
    st.session_state["round1_scores"] = None
for runde in range(100):
    if "round"+str(runde)+"_scores" not in st.session_state:
        runden_title="Runde "+str(runde)
        st.session_state["pairs"+runden_title]=None
        st.session_state["pairs_round"+str(runde)+"_df"]=None
        st.session_state["round"+str(runde)+"_scores"] = None

with st.form("spieleranzahl"):
    number = st.number_input("Wie viele Spieler:innen treten an?", value="min", min_value=0,
                            help="Bitte trage eine Zahl ein und bestätige mit Enter.")
    part_rounds={0:0,8:3,16:4,32:5,64:6,128:7,226:8,1e6:9}
    part_topcut={0:0,8:0,16:4,32:8,64:8,128:8,226:8,1e6:8}
    part_limits=[0,8,16,32,64,128,226,1e6]
    r=0

    while number > part_limits[r]:
        r=r+1
        rec_rounds=part_rounds[part_limits[r]]
        rec_topcut=part_topcut[part_limits[r]]
        
    letsgo = st.form_submit_button("Let's go!")
    if letsgo:
        st.session_state["number"]=number
    

# Form for Tournament Setup
if st.session_state["number"] is not None:
    with st.form("turnier"):
        st.header("Turnierformat")

        st.write(f"Empfohlene Rundenanzahl bei {number} Spieler:innen: {rec_rounds}")

        runden=rec_rounds
        runden = st.number_input("Wie viele Runden sollen gespielt werden?",
                                min_value=0, value=rec_rounds, help="Bitte trage eine Zahl ein und bestätige mit Enter.")
        
        st.write(f"Empfohlenes Topcut-Format bei {number} Spieler:innen: Top {rec_topcut}")
        topcut = st.number_input("Wie viele Spieler:innen sollen den Topcut spielen?",
                                min_value=0, value=rec_topcut, help="Bitte trage eine gerade Zahl ein und bestätige mit Enter.")
        
        if topcut%2!=0:
            st.warning("Bitte korrigiere das Topcut-Format. Zulässige Werte: 0 oder gerade Zahlen.")


        spiele_def=2
        spiele=spiele_def
        spiele = st.number_input("Wie viele Spiele sollen pro Runde gespielt werden?", value=spiele_def, 
                                help="Bitte trage eine Zahl ein und bestätige mit Enter.")

        if spiele not in [2, 3]:
            st.warning("Bitte korrigiere die Spielanzahl. Zulässige Werte: 2 oder 3.")

        st.header("Teilnehmer:innenliste")
        st.write("Bitte trage die Namen aller Spieler:innen in folgende Liste ein.")

        empty_name_list = [{"Vorname": "", "Nachname": ""} for _ in range(int(number))]
        df = pd.DataFrame(empty_name_list)
        participants_df = st.data_editor(df)

#         submitted = st.form_submit_button("Auf zu Runde 1!")
        
#         if submitted:
#             st.session_state["spiele"] = spiele
#             st.session_state["participants_df"] = participants_df

# # Generate Pairs for Round 1
# if st.session_state["spiele"] is not None:
#     with st.form("paarung"):
#         spiele = st.session_state["spiele"]
#         participants_df=st.session_state["participants_df"]
        if number > 0 and spiele in [2, 3]:
            random_index = np.arange(int(number))
            np.random.shuffle(random_index)

            columns = [
                "Spieler:in 1 - Vorname", "Spieler:in 1 - Nachname",
                "Spieler:in 2 - Vorname", "Spieler:in 2 - Nachname"
            ]
            columns += [f"Spielergebnis - Spiel {i + 1}" for i in range(int(spiele))]

            pairs_round1_df = pd.DataFrame(columns=columns)

            for i in range(int(number // 2)):
                pairs_round1_df.loc[i] = [
                    participants_df.loc[random_index[2 * i], "Vorname"],
                    participants_df.loc[random_index[2 * i], "Nachname"],
                    participants_df.loc[random_index[2 * i + 1], "Vorname"],
                    participants_df.loc[random_index[2 * i + 1], "Nachname"],
                ] + [np.nan] * int(spiele)

            if number % 2 == 1:
                pairs_round1_df.loc[len(pairs_round1_df)] = [
                    participants_df.loc[random_index[-1], "Vorname"],
                    participants_df.loc[random_index[-1], "Nachname"],
                    "Freilos", "Freilos"
                ] + [np.nan] * int(spiele)


        #st.dataframe(pairs_round1_df)
        einverstanden=st.form_submit_button("Auf zu Runde 1!")

        if einverstanden:
            st.session_state["pairs_round1_df"] = pairs_round1_df
            st.session_state["spiele"] = spiele
            st.session_state["topcut"] = topcut
            st.session_state["participants_df"] = participants_df



    # Form for Round 1
if (st.session_state["pairs_round1_df"] is not None) and (st.session_state["round1"] is None):
    with st.form("round1_form"):
        st.header("Runde 1")
        st.write("Es geht los. In dieser Tabelle findest du die Spielerpaarungen für Runde 1. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
        st.write("*0 - unentschieden; 1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2; 3 - das Spiel musste aus Zeitgründen abgebrochen werden*")
        st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
        pairs_round1_df_edited = st.data_editor(st.session_state["pairs_round1_df"],key="round1_editor")
        #pairs_round1_df_edited = st.data_editor(pairs_round1_df,key="round1_editor")
        fertig = st.form_submit_button("fertig")

        if fertig:
            st.session_state["pairs_round1_df_edited"] = pairs_round1_df_edited
            st.session_state["pairs_round1_df"] = pairs_round1_df_edited
            st.session_state["round1"] = "round1"
            st.success("Ergebnisse gespeichert!")
            #st.write("Aktuelle gespeicherte Ergebnisse:")
            #st.dataframe(st.session_state["pairs_round1_df"])
            #st.dataframe(st.session_state["pairs_round1_df"])
                

# Debug: Show saved data
#if st.session_state["pairs_round1_df_edited"] is not None:




# scores after first round
if (st.session_state["round1"] is not None) and (st.session_state["pairsRunde 2"] is None):
    with st.form("scores_round1"):
        participants_df=st.session_state["participants_df"]
        pairs_round1_df_edited=st.session_state["pairs_round1_df"]
        scores_df=participants_df.copy()
        for i in pairs_round1_df_edited.index:
            spieler1_index=participants_df[(participants_df['Vorname']==pairs_round1_df_edited.loc[i,'Spieler:in 1 - Vorname'])&(participants_df['Nachname']==pairs_round1_df_edited.loc[i,'Spieler:in 1 - Nachname'])].index[0]
            if pairs_round1_df_edited.loc[i,'Spieler:in 2 - Vorname']!='Freilos':
                spieler2_index=participants_df[(participants_df['Vorname']==pairs_round1_df_edited.loc[i,'Spieler:in 2 - Vorname'])&(participants_df['Nachname']==pairs_round1_df_edited.loc[i,'Spieler:in 2 - Nachname'])].index[0]
                punkte_spieler_1=0
                punkte_spieler_2=0
                siege_spieler_1=0
                niederlagen_spieler_1=0
                unentschieden_spieler_1=0
                siege_spieler_2=0
                niederlagen_spieler_2=0
                unentschieden_spieler_2=0
                if spiele == 2:
                    for spiel in range(int(spiele)):
                        if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]==0):
                            unentschieden_spieler_1=unentschieden_spieler_1+1
                            unentschieden_spieler_2=unentschieden_spieler_2+1
                        elif (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]==1):
                            siege_spieler_1=siege_spieler_1+1
                            niederlagen_spieler_2=niederlagen_spieler_2+1
                            punkte_spieler_1=punkte_spieler_1+3 
                        elif (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]==2):
                            siege_spieler_2=siege_spieler_2+1
                            niederlagen_spieler_1=niederlagen_spieler_1+1
                            punkte_spieler_2=punkte_spieler_2+3 
                        elif (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]==3):
                            if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]==1):
                                punkte_spieler_1=punkte_spieler_1+3
                                unentschieden_spieler_1=unentschieden_spieler_1+1
                                unentschieden_spieler_2=unentschieden_spieler_2+1
                            if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]==2):
                                punkte_spieler_2=punkte_spieler_2+3
                                unentschieden_spieler_1=unentschieden_spieler_1+1
                                unentschieden_spieler_2=unentschieden_spieler_2+1
                    if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]==1) & (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 2"]==1):
                        punkte_spieler_1=punkte_spieler_1+1
                    if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]==2) & (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 2"]==2):
                        punkte_spieler_2=punkte_spieler_2+1

                elif spiele == 3:
                    for s in range(spiele+1):
                        ausgang=[pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"],
                                pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 2"],
                                pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 3"]]
                        if ausgang.count(1) == 2:
                            punkte_spieler_1=3
                            punkte_spieler_2=0
                        else:
                            punkte_spieler_2=3
                            punkte_spieler_1=0
                        siege_spieler_1=ausgang.count(1)
                        niederlagen_spieler_1=ausgang.count(2)
                        unentschieden_spieler_1=ausgang.count(0)
                        siege_spieler_2=ausgang.count(2)
                        niederlagen_spieler_2=ausgang.count(1)
                        unentschieden_spieler_2=ausgang.count(0)
                scores_df.loc[spieler1_index, "Punktestand"]=punkte_spieler_1
                scores_df.loc[spieler2_index, "Punktestand"]=punkte_spieler_2
                scores_df.loc[spieler1_index, "Siege"]=siege_spieler_1
                scores_df.loc[spieler2_index, "Siege"]=siege_spieler_2
                scores_df.loc[spieler1_index, "Niederlagen"]=niederlagen_spieler_1
                scores_df.loc[spieler2_index, "Niederlagen"]=niederlagen_spieler_2
                scores_df.loc[spieler1_index, "Unentschieden"]=unentschieden_spieler_1
                scores_df.loc[spieler2_index, "Unentschieden"]=unentschieden_spieler_2
                scores_df.loc[spieler1_index, "Freilose"]=0
                scores_df.loc[spieler2_index, "Freilose"]=0
                scores_df.loc[spieler1_index, "Gegner:in Runde 1 - Vorname"]=pairs_round1_df_edited.loc[i,'Spieler:in 2 - Vorname']
                scores_df.loc[spieler1_index, "Gegner:in Runde 1 - Nachname"]=pairs_round1_df_edited.loc[i,'Spieler:in 2 - Nachname']
                scores_df.loc[spieler2_index, "Gegner:in Runde 1 - Vorname"]=pairs_round1_df_edited.loc[i,'Spieler:in 1 - Vorname']
                scores_df.loc[spieler2_index, "Gegner:in Runde 1 - Nachname"]=pairs_round1_df_edited.loc[i,'Spieler:in 1 - Nachname']
            else:
                scores_df.loc[spieler1_index, "Punktestand"]=6
                scores_df.loc[spieler1_index, "Siege"]=0
                scores_df.loc[spieler1_index, "Niederlagen"]=0
                scores_df.loc[spieler1_index, "Unentschieden"]=0
                scores_df.loc[spieler1_index, "Freilose"]=1
                scores_df.loc[spieler1_index, "Gegner:in Runde 1 - Nachname"]="Freilos"
                scores_df.loc[spieler1_index, "Gegner:in Runde 1 - Vorname"]="Freilos"

            
            
        
        round1_finished=st.form_submit_button("Spielstand nach Runde 1...")
        if round1_finished:
            st.session_state["round1_scores"]=scores_df



if st.session_state["round1_scores"] is not None:
    for runde in range(2,int(runden+1)):
        if (st.session_state["round"+str(runde-1)+"_scores"] is not None) & (st.session_state["round"+str(runde)+"_scores"] is None):
            #st.write("Spielstand nach Runde "+str(runde)+":")
            scores_df=st.session_state["round"+str(runde-1)+"_scores"]
            scores_df=scores_df.sort_values(['Punktestand', 'Siege'], ascending=[False, False])
            scores_df.index=np.arange(1, len(scores_df)+1)
            st.dataframe(scores_df)
            runden_title="Runde "+str(runde)
            with st.form(runden_title):
                st.header("Runde "+str(runde))

                columns = [
                        "Spieler:in 1 - Vorname", "Spieler:in 1 - Nachname",
                        "Spieler:in 2 - Vorname", "Spieler:in 2 - Nachname"
                    ]
                columns += [f"Spielergebnis - Spiel {i + 1}" for i in range(int(spiele))]

                pairs_round_df = pd.DataFrame(columns=columns)
                #scores_df=st.session_state["round1_scores"]

                pair=0
                for i in scores_df.index:
                    if i%2 == 1:
                        pairs_round_df.loc[pair,"Spieler:in 1 - Vorname"] = scores_df.loc[i,"Vorname"]
                        pairs_round_df.loc[pair,"Spieler:in 1 - Nachname"] = scores_df.loc[i,"Nachname"]
                        
                    else:
                        pairs_round_df.loc[pair,"Spieler:in 2 - Vorname"] = scores_df.loc[i,"Vorname"]
                        pairs_round_df.loc[pair,"Spieler:in 2 - Nachname"] = scores_df.loc[i,"Nachname"]
                        pair=pair+1
                        
                if i%2==1:
                    pairs_round_df.loc[pair,"Spieler:in 2 - Vorname"] = "Freilos"
                    pairs_round_df.loc[pair,"Spieler:in 2 - Nachname"] = "Freilos"

                #st.dataframe(pairs_round1_df)
                button_title="Los geht's mit "+runden_title+"!"
                runde_teilnehmer=st.form_submit_button(button_title)

                if runde_teilnehmer:
                    st.session_state["pairs"+runden_title] = pairs_round_df

            if (st.session_state["pairs"+runden_title] is not None):
                with st.form("round"+str(runde)+"_form"):
                    st.write("Weiter geht's. In dieser Tabelle findest du die Spielerpaarungen für Runde " +str(runde)+ ". Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                    st.write("*0 - unentschieden; 1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                    st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
                    pairs_round_df_edited = st.data_editor(st.session_state["pairs"+runden_title],key="round"+str(runde)+"_editor")
                    #pairs_round1_df_edited = st.data_editor(pairs_round1_df,key="round1_editor")
                    button_title="Runde "+str(runde)+" beendet"
                    fertig = st.form_submit_button(button_title)

                    if fertig:
                        st.session_state["pairs_round"+str(runde)+"_df"] = pairs_round_df_edited
                        #st.session_state["pairs_round1_df"] = pairs_round1_df_edited
                        #st.session_state["round1"] = "round1"
                        st.success("Ergebnisse gespeichert!")
                        #st.write("Aktuelle gespeicherte Ergebnisse:")
                        #st.dataframe(st.session_state["pairs_round"+str(runde)+"_df"])

            if st.session_state["pairs_round"+str(runde)+"_df"] is not None:
                with st.form("scores_round"+str(runde)):
                    spiele=st.session_state["spiele"]
                    participants_df=st.session_state["participants_df"]
                    pairs_round_df_edited=st.session_state["pairs_round"+str(runde)+"_df"]
                    scores_old_df=st.session_state["round"+str(runde-1)+"_scores"]
                    scores_df=participants_df.copy()
                    for i in pairs_round_df_edited.index:
                        spieler1_index=participants_df[(participants_df['Vorname']==pairs_round_df_edited.loc[i,'Spieler:in 1 - Vorname'])&(participants_df['Nachname']==pairs_round_df_edited.loc[i,'Spieler:in 1 - Nachname'])].index[0]
                        spieler1_index_scores=scores_old_df[(scores_old_df['Vorname']==pairs_round_df_edited.loc[i,'Spieler:in 1 - Vorname'])&(scores_old_df['Nachname']==pairs_round_df_edited.loc[i,'Spieler:in 1 - Nachname'])].index[0]
                        if pairs_round_df_edited.loc[i,'Spieler:in 2 - Vorname']!='Freilos':
                            spieler2_index=participants_df[(participants_df['Vorname']==pairs_round_df_edited.loc[i,'Spieler:in 2 - Vorname'])&(participants_df['Nachname']==pairs_round_df_edited.loc[i,'Spieler:in 2 - Nachname'])].index[0]
                            spieler2_index_scores=scores_old_df[(scores_old_df['Vorname']==pairs_round_df_edited.loc[i,'Spieler:in 2 - Vorname'])&(scores_old_df['Nachname']==pairs_round_df_edited.loc[i,'Spieler:in 2 - Nachname'])].index[0]
                            punkte_spieler_1=scores_old_df.loc[spieler1_index_scores,"Punktestand"]
                            punkte_spieler_2=scores_old_df.loc[spieler2_index_scores,"Punktestand"]
                            siege_spieler_1=scores_old_df.loc[spieler1_index_scores,"Siege"]
                            niederlagen_spieler_1=scores_old_df.loc[spieler1_index_scores,"Niederlagen"]
                            unentschieden_spieler_1=scores_old_df.loc[spieler1_index_scores,"Unentschieden"]
                            freilose_spieler_1=scores_old_df.loc[spieler1_index_scores,"Freilose"]
                            siege_spieler_2=scores_old_df.loc[spieler2_index_scores,"Siege"]
                            niederlagen_spieler_2=scores_old_df.loc[spieler2_index_scores,"Niederlagen"]
                            unentschieden_spieler_2=scores_old_df.loc[spieler2_index_scores,"Unentschieden"]
                            freilose_spieler_2=scores_old_df.loc[spieler2_index_scores,"Freilose"]
                            punkte_spieler_1_runde=0
                            punkte_spieler_2_runde=0
                            if spiele == 2:
                                for spiel in range(int(spiele)):
                                    if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]=="0"):
                                        unentschieden_spieler_1=unentschieden_spieler_1+1
                                        unentschieden_spieler_2=unentschieden_spieler_2+1
                                    elif (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]=="1"):
                                        siege_spieler_1=siege_spieler_1+1
                                        niederlagen_spieler_2=niederlagen_spieler_2+1
                                        punkte_spieler_1_runde=punkte_spieler_1_runde+3 
                                        punkte_spieler_1=punkte_spieler_1+3
                                    elif (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]=="2"):
                                        siege_spieler_2=siege_spieler_2+1
                                        niederlagen_spieler_1=niederlagen_spieler_1+1
                                        punkte_spieler_2_runde=punkte_spieler_2_runde+3 
                                        punkte_spieler_2=punkte_spieler_2+3
                                    elif (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]=="3"):
                                        if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="1"):
                                            punkte_spieler_1=punkte_spieler_1+3
                                            unentschieden_spieler_1=unentschieden_spieler_1+1
                                            unentschieden_spieler_2=unentschieden_spieler_2+1
                                        if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="2"):
                                            punkte_spieler_2=punkte_spieler_2+3
                                            unentschieden_spieler_1=unentschieden_spieler_1+1
                                            unentschieden_spieler_2=unentschieden_spieler_2+1
                                if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="1") & (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 2"]=="1"):
                                    punkte_spieler_1=punkte_spieler_1+1
                                if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="2") & (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 2"]=="2"):
                                    punkte_spieler_2=punkte_spieler_2+1

                            elif spiele == 3:
                                for s in range(spiele+1):
                                    ausgang=[int(pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]),
                                            int(pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 2"]),
                                            int(pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 3"])]
                                    if ausgang.count(1) == 2:
                                        punkte_spieler_1=punkte_spieler_1+3
                                        punkte_spieler_2=punkte_spieler_2
                                    else:
                                        punkte_spieler_2=punkte_spieler_2+3
                                        punkte_spieler_1=punkte_spieler_1
                                    siege_spieler_1=siege_spieler_1+ausgang.count(1)
                                    niederlagen_spieler_1=niederlagen_spieler_1+ausgang.count(2)
                                    unentschieden_spieler_1=unentschieden_spieler_1+ausgang.count(0)
                                    siege_spieler_2=siege_spieler_2+ausgang.count(2)
                                    niederlagen_spieler_2=ausgang.count(1)
                                    unentschieden_spieler_2=unentschieden_spieler_2+ausgang.count(0)
                            scores_df.loc[spieler1_index, "Punktestand"]=punkte_spieler_1
                            scores_df.loc[spieler2_index, "Punktestand"]=punkte_spieler_2
                            scores_df.loc[spieler1_index, "Siege"]=siege_spieler_1
                            scores_df.loc[spieler2_index, "Siege"]=siege_spieler_2
                            scores_df.loc[spieler1_index, "Niederlagen"]=niederlagen_spieler_1
                            scores_df.loc[spieler2_index, "Niederlagen"]=niederlagen_spieler_2
                            scores_df.loc[spieler1_index, "Unentschieden"]=unentschieden_spieler_1
                            scores_df.loc[spieler2_index, "Unentschieden"]=unentschieden_spieler_2
                            scores_df.loc[spieler1_index, "Freilose"]=freilose_spieler_1
                            scores_df.loc[spieler2_index, "Freilose"]=freilose_spieler_2
                            for vorrunde in range(1,runde):
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)+" - Vorname"]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Vorname"]
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)+" - Nachname"]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Nachname"]
                                scores_df.loc[spieler2_index, "Gegner:in Runde "+str(vorrunde)+" - Vorname"]=scores_old_df.loc[spieler2_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Vorname"]
                                scores_df.loc[spieler2_index, "Gegner:in Runde "+str(vorrunde)+" - Nachname"]=scores_old_df.loc[spieler2_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Nachname"]
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)+" - Vorname"]=pairs_round_df_edited.loc[i,'Spieler:in 2 - Vorname']    
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)+" - Nachname"]=pairs_round_df_edited.loc[i,'Spieler:in 2 - Nachname']
                            scores_df.loc[spieler2_index, "Gegner:in Runde "+str(runde)+" - Vorname"]=pairs_round_df_edited.loc[i,'Spieler:in 1 - Vorname']
                            scores_df.loc[spieler2_index, "Gegner:in Runde "+str(runde)+" - Nachname"]=pairs_round_df_edited.loc[i,'Spieler:in 1 - Nachname']
                            
                        else:
                            scores_df.loc[spieler1_index, "Punktestand"]=scores_old_df.loc[spieler1_index_scores,"Punktestand"]+6
                            scores_df.loc[spieler1_index, "Siege"]=scores_old_df.loc[spieler1_index_scores,"Siege"]
                            scores_df.loc[spieler1_index, "Niederlagen"]=scores_old_df.loc[spieler1_index_scores,"Niederlagen"]
                            scores_df.loc[spieler1_index, "Unentschieden"]=scores_old_df.loc[spieler1_index_scores,"Unentschieden"]
                            scores_df.loc[spieler1_index, "Freilose"]=scores_old_df.loc[spieler1_index_scores,"Freilose"]+1
                            for vorrunde in range(1,runde):
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)+" - Vorname"]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Vorname"]
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)+" - Nachname"]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)+" - Nachname"]
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)+" - Vorname"]="Freilos"
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)+" - Nachname"]="Freilos"
                            

                        
                    if runde + 1 <= runden:    
                    
                        round_finished=st.form_submit_button("Spielstand nach Runde "+str(runde)+"...")
                        if round_finished:
                            st.session_state["round"+str(runde)+"_scores"]=scores_df
                    
                    else:
                        if topcut == 0:
                            round_finished=st.form_submit_button("Finaler Punktestand!")
                            if round_finished:
                                st.session_state["round"+str(runde)+"_scores"]=scores_df
                                st.dataframe(st.session_state["round"+str(runde)+"_scores"])
                        else:
                            round_finished=st.form_submit_button("Zum finalem Punktestand vorm Topcut")
                            if round_finished:
                                st.session_state["topcut_start"]="start"
                                st.session_state["round"+str(runde)+"_scores"]=scores_df
                                st.dataframe(st.session_state["round"+str(runde)+"_scores"])

if st.session_state["topcut_start"] == "start":
    st.header("Topcut")
                    
            #st.dataframe(st.session_state["pairs_round1_df"])


    #         #     if spiele == 3:
    #         # scores_df.loc[spieler1_index,"Punktestand"]=0
    #         # scores_df[spieler1_index,"Anzahl Siege"]=0
    #     scores_df_edited=st.data_editor(scores_df)

# #st.rerun()
