import streamlit as st
import pandas as pd
import numpy as np
import random

# Title and Image
st.set_page_config(layout="wide")
st.title("Kassel Illumineers - Swiss Rounds")
st.image("logo.jpg", width=250)


# Session State for Results
if "pairs_round1_df" not in st.session_state:
    st.session_state["pairs_round1_df"] = None
if "participants_drop" not in st.session_state:
    st.session_state["participants_drop"] = None
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
if "Viertelfinale" not in st.session_state:
    st.session_state["Viertelfinale"] = None
if "Halbfinale" not in st.session_state:
    st.session_state["Halbfinale"] = None
if "Finale" not in st.session_state:
    st.session_state["Finale"] = None
if "result_Viertelfinale" not in st.session_state:
    st.session_state["result_Viertelfinale"] = None
if "result_Halbfinale" not in st.session_state:
    st.session_state["result_Halbfinale"] = None
if "result_Finale" not in st.session_state:
    st.session_state["result_Finale"] = None

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
        
    letsgo = st.form_submit_button("Los geht's!")
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
        
        if topcut not in [0,4,8]:
            st.warning("Bitte korrigiere das Topcut-Format. Zulässige Werte: 0, 4, 8.")


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
        participants_df = st.data_editor(df, height=35*len(df)+38, hide_index=True)
        participants_df ["Name"]= participants_df["Vorname"] + " " + participants_df["Nachname"]
        participants_df = participants_df.drop(['Vorname','Nachname'], axis=1)

        # submitted = st.form_submit_button("Auf zu Runde 1!")
        
        # if submitted:
        #     st.session_state["spiele"] = spiele
        #     st.session_state["participants_df"] = participants_df

# # Generate Pairs for Round 1
# if st.session_state["spiele"] is not None:
#     with st.form("paarung"):
#         spiele = st.session_state["spiele"]
#         participants_df=st.session_state["participants_df"]
        if number > 0 and spiele in [2, 3]:
            random_index = np.arange(int(number))
            np.random.shuffle(random_index)

            columns = [
                "Spieler:in 1", 
                "Spieler:in 2",
            ]
            columns += [f"Spielergebnis - Spiel {i + 1}" for i in range(int(spiele))]

            pairs_round1_df = pd.DataFrame(columns=columns)

            for i in range(int(number // 2)):
                pairs_round1_df.loc[i] = [
                    participants_df.loc[random_index[2 * i], "Name"],
                    participants_df.loc[random_index[2 * i + 1], "Name"],
                ] + [np.nan] * int(spiele)

            if number % 2 == 1:
                pairs_round1_df.loc[len(pairs_round1_df)] = [
                    participants_df.loc[random_index[-1], "Name"],
                                "Freilos",
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
        st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2; 3 - unentschieden oder Abbruch aus Zeitgründen*")
        st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
        pairs_round1_df_edited = st.data_editor(st.session_state["pairs_round1_df"],key="round1_editor", height=35*len(st.session_state["pairs_round1_df"])+38, hide_index=True)
        #pairs_round1_df_edited = st.data_editor(pairs_round1_df,key="round1_editor")
        fertig = st.form_submit_button("Runde 1 beendet")

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
        runde=1
        for i in pairs_round1_df_edited.index:
            spieler1_index=participants_df[(participants_df['Name']==pairs_round1_df_edited.loc[i,'Spieler:in 1'])].index[0]
            if pairs_round1_df_edited.loc[i,'Spieler:in 2']!='Freilos':
                spieler2_index=participants_df[(participants_df['Name']==pairs_round1_df_edited.loc[i,'Spieler:in 2'])].index[0]
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
                        if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]==1):
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
                                siege_spieler_1=siege_spieler_1+1
                                niederlagen_spieler_2=niederlagen_spieler_2+1
                            if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]==2):
                                punkte_spieler_2=punkte_spieler_2+3
                                siege_spieler_2=siege_spieler_2+1
                                niederlagen_spieler_1=niederlagen_spieler_1+1
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
                            siege_spieler_1=ausgang.count(1)
                            niederlagen_spieler_1=ausgang.count(2)
                            siege_spieler_2=ausgang.count(2)
                            niederlagen_spieler_2=ausgang.count(1)
                        elif ausgang.count(2) == 2:
                            punkte_spieler_2=3
                            punkte_spieler_1=0
                            siege_spieler_1=ausgang.count(1)
                            niederlagen_spieler_1=ausgang.count(2)
                            siege_spieler_2=ausgang.count(2)
                            niederlagen_spieler_2=ausgang.count(1)                            
                        elif ausgang.count(3) > 0:
                            punkte_spieler_2=1
                            punkte_spieler_1=1
                            siege_spieler_1=1
                            niederlagen_spieler_1=1
                            siege_spieler_2=1
                            niederlagen_spieler_2=1                       
                            unentschieden_spieler_1=1
                            unentschieden_spieler_2=1
                        nicht_beendet=ausgang.count(3)
                scores_df.loc[spieler1_index, "Punktestand"]=punkte_spieler_1
                scores_df.loc[spieler2_index, "Punktestand"]=punkte_spieler_2
                scores_df.loc[spieler1_index, "Siege"]=siege_spieler_1
                scores_df.loc[spieler2_index, "Siege"]=siege_spieler_2
                scores_df.loc[spieler1_index, "Niederlagen"]=niederlagen_spieler_1
                scores_df.loc[spieler2_index, "Niederlagen"]=niederlagen_spieler_2
                scores_df.loc[spieler1_index, "Unentschieden"]=unentschieden_spieler_1
                scores_df.loc[spieler2_index, "Unentschieden"]=unentschieden_spieler_2
                if (niederlagen_spieler_1 == 0) & (unentschieden_spieler_1==0):
                    scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=1
                    scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=0
                elif (niederlagen_spieler_2 == 0) & (unentschieden_spieler_2==0):
                    scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=0
                    scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=1
                else:
                    scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=0
                    scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=0
                scores_df.loc[spieler1_index, "Freilose"]=0
                scores_df.loc[spieler2_index, "Freilose"]=0
                scores_df.loc[spieler1_index, "Gegner:in Runde 1"]=pairs_round1_df_edited.loc[i,'Spieler:in 2']
                scores_df.loc[spieler2_index, "Gegner:in Runde 1"]=pairs_round1_df_edited.loc[i,'Spieler:in 1']
                
            else:
                if spiele ==2:
                    scores_df.loc[spieler1_index, "Punktestand"]=7
                else:
                    scores_df.loc[spieler1_index, "Punktestand"]=3
                scores_df.loc[spieler1_index, "Siege"]=0
                scores_df.loc[spieler1_index, "Niederlagen"]=0
                scores_df.loc[spieler1_index, "Unentschieden"]=0
                scores_df.loc[spieler1_index, "Freilose"]=1
                scores_df.loc[spieler1_index, "Gegner:in Runde 1"]="Freilos"
                scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=0
       
        scores_df['Punktestand der Gegner:innen der Gegner:innen']=""
        scores_df['Punktestand der Gegner:innen']=""
        for i in scores_df.index:
            punkte_alle_gegner=0
            punkte_alle_gegnergegner=0
            for r in range(1,runde+1):
                gegner=scores_df.loc[i, "Gegner:in Runde "+str(r)]
                if gegner != "Freilos":
                    punkte_gegner=scores_df[(scores_df["Name"]==gegner)]['Punktestand'].values[0]
                    punkte_alle_gegner=punkte_alle_gegner+punkte_gegner
                    gegner_index=scores_df[(scores_df["Name"]==gegner)].index[0]
                    for x in range(1,runde+1):
                        gegnergegner=scores_df.loc[gegner_index, "Gegner:in Runde "+str(x)]
                        if gegnergegner != "Freilos":
                            punkte_gegnergegner=scores_df[(scores_df["Name"]==gegnergegner)]['Punktestand'].values[0]
                            punkte_alle_gegnergegner=punkte_alle_gegnergegner+punkte_gegnergegner 
            scores_df.loc[i,'Punktestand der Gegner:innen']=punkte_alle_gegner
            scores_df.loc[i,'Punktestand der Gegner:innen der Gegner:innen']=punkte_alle_gegnergegner         
            
        
        round1_finished=st.form_submit_button("Spielstand nach Runde 1...")
        if round1_finished:
            st.session_state["round1_scores"]=scores_df



if st.session_state["round1_scores"] is not None:
    for runde in range(2,int(runden+1)):
        if (st.session_state["round"+str(runde-1)+"_scores"] is not None) & (st.session_state["round"+str(runde)+"_scores"] is None):
            #st.write("Spielstand nach Runde "+str(runde)+":")
            scores_df=st.session_state["round"+str(runde-1)+"_scores"]
            scores_df=scores_df.sort_values(['Punktestand',"Streaks (Runden ohne Niederlage)", 'Punktestand der Gegner:innen','Punktestand der Gegner:innen der Gegner:innen'], ascending=[False, False,False,False])
            scores_df.index=np.arange(1, len(scores_df)+1)
            st.dataframe(scores_df, height=35*len(scores_df)+38)
            runden_title="Runde "+str(runde)
            with st.form(runden_title):
                st.header("Runde "+str(runde))

                         
                # if i%2==1:
                #     pairs_round_df.loc[pair,"Spieler:in 2 - Vorname"] = "Freilos"
                #     pairs_round_df.loc[pair,"Spieler:in 2 - Nachname"] = "Freilos"

                #st.dataframe(pairs_round1_df)
                button_title="Los geht's mit "+runden_title+"!"
                st.write('Bevor die nächste Runde startet, setzt bitte in folgender Tabelle ein Häckchen hinter den jeweiligen Namen, falls jemand nicht weiterspielen möchte:')
                if st.session_state["participants_drop"] is None:
                    dropped_participants_df=participants_df.copy()
                    dropped_participants_df['aufgegeben?']=[False for n in range(len(dropped_participants_df))]
                else:
                    dropped_participants_df=st.session_state["participants_drop"]
                
                dropped_participants_df=st.data_editor(dropped_participants_df,
                                        column_config={
                                            "aufgegeben?": st.column_config.CheckboxColumn(
                                                "aufgegeben?",
                                                help="Wähle alle Spieler:innen aus, die aufgegeben haben",
                                                default=False,
                                            )
                                        },
                                        disabled=["widgets"],
                                        hide_index=True, height=35*len(dropped_participants_df)+38
                                    )
                participants_drop=dropped_participants_df.copy()
                dropped_participants_df=dropped_participants_df[dropped_participants_df['aufgegeben?']==True]
                
                runde_teilnehmer=st.form_submit_button(button_title)

                if runde_teilnehmer:
                    pairs_round_df=pd.DataFrame()
                    st.session_state["pairs"+runden_title] = pairs_round_df
                    st.session_state["participants_drop"]=participants_drop

            if (st.session_state["pairs"+runden_title] is not None) and (st.session_state["pairs_round"+str(runde)+"_df"] is None):
                with st.form("round"+str(runde)+"_form"):
                    columns = [
                        "Spieler:in 1", 
                        "Spieler:in 2",
                    ]
                    columns += [f"Spielergebnis - Spiel {i + 1}" for i in range(int(spiele))]

                    pairs_round_df = pd.DataFrame(columns=columns)
                    #scores_df=st.session_state["round1_scores"]
                    scores_df_continue=scores_df.copy()
                    scores_df_continue=scores_df_continue[~scores_df_continue['Name'].isin(dropped_participants_df['Name'])]
                    #st.dataframe(scores_df_continue)

                    # Initialize dataframes and sets
                    df = scores_df_continue
                    played_matches=set()
                    for y in range(1,runde):
                        played_matches_runde = set(
                            tuple(sorted([row["Name"], row["Gegner:in Runde "+str(y)]])) for _, row in df.iterrows()
                                        )
                        played_matches=played_matches.union(played_matches_runde)
                    freilos_tracker = []  # Set to track players who have already received "freilos"
                    freilos_names=scores_df_continue[scores_df_continue["Freilose"]==1]['Name']
                    for n in freilos_names:
                        freilos_tracker.append(n)

                    # Sort players by scores (descending)
                    df = df.sort_values(by="Punktestand", ascending=False).reset_index(drop=True)

                    # Pair players without redundancy
                    pairs = []
                    unpaired = []
                    paired = []

                    for i, player1 in df.iterrows():
                        if (player1["Name"] in unpaired) or (player1["Name"] in paired):
                            print("x")
                        elif i == (len(df)-1):
                            unpaired.append(player1["Name"])
                        else:
                            for j, player2 in df[i+1:].iterrows():
                                #if player1["Punktestand"] == player2["Punktestand"]:
                                if (player2["Name"] not in unpaired) and (player2["Name"] not in paired):
                                    pair = tuple(sorted([player1["Name"], player2["Name"]]))
                                    if pair not in played_matches:
                                        pairs.append(pair)
                                        played_matches.add(pair)
                                        paired.append(player1["Name"])
                                        paired.append(player2["Name"])  # Mark player2 as paired
                                        break
                                    else:
                                        if j == (len(df)-1):
                                            unpaired.append(player1["Name"])  # Mark player1 as unpaired

                    # Assign "freilos" if the number of players is uneven
                    freilos_warning=[]
                    if len(unpaired) % 2 == 1:
                        freilos_assigned = False
                        remaining_unpaired = []

                        for player in unpaired:
                            if not freilos_assigned and player not in freilos_tracker:
                                pairs.append((player, "Freilos"))
                                freilos_tracker.append(player)
                                freilos_assigned = True
                            elif not freilos_assigned and player == unpaired[-1]:
                                pairs.append((player, "Freilos"))
                                freilos_tracker.append(player)
                                freilos_assigned = True
                                freilos_warning.append(player)
                            else:
                                remaining_unpaired.append(player)

                        unpaired = remaining_unpaired

                    # Pair remaining unpaired players randomly
                    redundant_pairs=[]
                    while len(unpaired) > 1:
                        player1 = unpaired.pop(0)
                        player2 = unpaired.pop(0)
                        pair = tuple(sorted([player1, player2]))
                        pairs.append((player1, player2))

                        if pair in played_matches:
                            redundant_pairs.append(pair)



                    # Output the pairs
                    for p,pair in enumerate(pairs):
                        pairs_round_df.loc[p,"Spieler:in 1"]=pair[0]
                        pairs_round_df.loc[p,"Spieler:in 2"]=pair[1]
                    #print("Pairs for this round:", pairs)
                    #print("Players with 'freilos':", freilos_tracker)

                    #######
                    # pair=0
                    
                    # if len(scores_df_continue)%2!=0:
                    #     df=scores_df_continue.sort_values(['Punktestand',"Streaks (Runden ohne Niederlage)", 'Punktestand der Gegner:innen','Punktestand der Gegner:innen der Gegner:innen'],ascending=[True,True,True,True])
                    #     df1=df[df['Punktestand']==df.iloc[0]['Punktestand']]
                    #     df1=df1[df1['Freilose']==0]
                    #     # if len(df1)>0:
                    #     #     worst_random=random.choice([x for x in df1.index])
                    #     # else:
                    #     n=1
                    #     while len(df1)==0:
                    #         score=sorted(df['Punktestand'].unique())[n]
                    #         df1=df[df['Punktestand']==score]
                    #         df1=df1[df1['Freilose']==0]
                    #         n=n+1
                    #     worst_random=random.choice([x for x in df1.index])
                    #     pairs_round_df.loc[pair,"Spieler:in 1"] = scores_df.loc[worst_random,"Name"]
                    #     pairs_round_df.loc[pair,"Spieler:in 2"] = "Freilos"
                    #     pair=pair+1

                    #     scores_df_continue=scores_df_continue.drop(worst_random)
                    # scores_df_continue.index=np.arange(1, len(scores_df_continue)+1)

                    # for i in scores_df_continue.index:
                    #     if i%2 == 1:
                    #         pairs_round_df.loc[pair,"Spieler:in 1"] = scores_df_continue.loc[i,"Name"]
                            
                    #     else:
                    #         pairs_round_df.loc[pair,"Spieler:in 2"] = scores_df_continue.loc[i,"Name"]
                    #         pair=pair+1
                    ######

                    st.write("Weiter geht's. In dieser Tabelle findest du die Spielerpaarungen für Runde " +str(runde)+ ". Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                    st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2; 3 - unentschieden oder Abbruch aus Zeitgründen*")
                    st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
                    
                    if len(redundant_pairs)>=1:
                        st.write("Achtung! Folgende Spieler:innenpaare sind bereits in einer der vorherigen Runden aufeinander getroffen:"+str(redundant_pairs))
                        st.write("Nimm gegebenenfalls manuelle Anpassungen an den redundanten Spielerpaarungen vor.")
                        st.write("Hier nochmal ein Überblick, wer bereits gegen wen gespielt hat:")
                        columns=["Name"]
                        for y in range(1,runde):
                            columns.append("Gegner:in Runde "+str(y))
                        st.dataframe(scores_df[columns], height=35*len(scores_df)+38, hide_index=True)
                    elif len(freilos_warning)>=1:
                        st.write("Achtung! Folgende:r Spieler:in wurde erneut ein Freilos zugeordnet: "+freilos_warning[0])
                        st.write("Nimm gegebenenfalls manuelle Anpassungen an der Freiloszuordnung und den Spielerpaarungen vor.")
                        st.write("Hier nochmal ein Überblick, wer bereits gegen wen gespielt hat:")
                        columns=["Name"]
                        for y in range(1,runde):
                            columns.append("Gegner:in Runde "+str(y))
                        st.dataframe(scores_df[columns], height=35*len(scores_df)+38, hide_index=True)
                    st.session_state["pairs"+runden_title]=pairs_round_df
                    
                    
                    pairs_round_df_edited = st.data_editor(pairs_round_df,key="round"+str(runde)+"_editor", height=35*len(pairs_round_df)+38, hide_index=True)
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
                        spieler1_index=participants_df[(participants_df['Name']==pairs_round_df_edited.loc[i,'Spieler:in 1'])].index[0]
                        spieler1_index_scores=scores_old_df[(scores_old_df['Name']==pairs_round_df_edited.loc[i,'Spieler:in 1'])].index[0]
                        if pairs_round_df_edited.loc[i,'Spieler:in 2']!='Freilos':
                            spieler2_index=participants_df[(participants_df['Name']==pairs_round_df_edited.loc[i,'Spieler:in 2'])].index[0]
                            spieler2_index_scores=scores_old_df[(scores_old_df['Name']==pairs_round_df_edited.loc[i,'Spieler:in 2'])].index[0]
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
                                ausgang=[]
                                for spielergebnis in ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2"]:
                                    if pd.isna(pairs_round_df_edited.loc[i, spielergebnis]) or (pairs_round_df_edited.loc[i, spielergebnis] == ""):
                                        ausgang.append(0)
                                    else:
                                        ausgang.append(int(pairs_round_df_edited.loc[i,spielergebnis]))
                                for spiel in range(int(spiele)):
                                    if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel "+str(spiel+1)]=="1"):
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
                                        if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="1"):
                                            punkte_spieler_1=punkte_spieler_1+3
                                            siege_spieler_1=siege_spieler_1+1
                                            niederlagen_spieler_2=niederlagen_spieler_2+1
                                        if (pairs_round1_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="2"):
                                            punkte_spieler_2=punkte_spieler_2+3
                                            siege_spieler_2=siege_spieler_2+1
                                            niederlagen_spieler_1=niederlagen_spieler_1+1
                                if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="1") & (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 2"]=="1"):
                                    punkte_spieler_1=punkte_spieler_1+1
                                if (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 1"]=="2") & (pairs_round_df_edited.loc[i,"Spielergebnis - Spiel 2"]=="2"):
                                    punkte_spieler_2=punkte_spieler_2+1

                            elif spiele == 3: 
                                ausgang=[]
                                for spielergebnis in ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]:
                                    if pd.isna(pairs_round_df_edited.loc[i, spielergebnis]) or (pairs_round_df_edited.loc[i, spielergebnis] == ""):
                                        ausgang.append(0)
                                    else:
                                        ausgang.append(int(pairs_round_df_edited.loc[i,spielergebnis]))
                                if ausgang.count(1) == 2:
                                    punkte_spieler_1=punkte_spieler_1+3
                                    punkte_spieler_2=punkte_spieler_2
                                    siege_spieler_1=siege_spieler_1+ausgang.count(1)
                                    niederlagen_spieler_1=niederlagen_spieler_1+ausgang.count(2)
                                    siege_spieler_2=siege_spieler_2+ausgang.count(2)
                                    niederlagen_spieler_2=niederlagen_spieler_2+ausgang.count(1)
                                elif ausgang.count(2) == 2:
                                    punkte_spieler_2=punkte_spieler_2+3
                                    punkte_spieler_1=punkte_spieler_1+0
                                    siege_spieler_1=siege_spieler_1+ausgang.count(1)
                                    niederlagen_spieler_1=niederlagen_spieler_1+ausgang.count(2)
                                    siege_spieler_2=siege_spieler_2+ausgang.count(2)
                                    niederlagen_spieler_2=niederlagen_spieler_2+ausgang.count(1)                            
                                elif ausgang.count(3) > 0:
                                    punkte_spieler_2=punkte_spieler_2+1
                                    punkte_spieler_1=punkte_spieler_1+1
                                    siege_spieler_1=siege_spieler_1+1
                                    niederlagen_spieler_1=niederlagen_spieler_1+1
                                    siege_spieler_2=siege_spieler_2+1
                                    niederlagen_spieler_2=niederlagen_spieler_2+1                       
                                    unentschieden_spieler_1=unentschieden_spieler_1+1
                                    unentschieden_spieler_2=unentschieden_spieler_1+1
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
                            if (ausgang.count(2) == 0) & (ausgang.count(3)==0):
                                scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler1_index_scores,"Streaks (Runden ohne Niederlage)"]+1
                                scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler2_index_scores,"Streaks (Runden ohne Niederlage)"]
                            elif (ausgang.count(1) == 0) & (ausgang.count(3)==0):
                                scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler2_index_scores,"Streaks (Runden ohne Niederlage)"]+1
                                scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler1_index_scores,"Streaks (Runden ohne Niederlage)"]
                            else:
                                scores_df.loc[spieler2_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler2_index_scores,"Streaks (Runden ohne Niederlage)"]
                                scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler1_index_scores,"Streaks (Runden ohne Niederlage)"]
                            for vorrunde in range(1,runde):
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)]
                                scores_df.loc[spieler2_index, "Gegner:in Runde "+str(vorrunde)]=scores_old_df.loc[spieler2_index_scores,"Gegner:in Runde "+str(vorrunde)]
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)]=pairs_round_df_edited.loc[i,'Spieler:in 2']    
                            scores_df.loc[spieler2_index, "Gegner:in Runde "+str(runde)]=pairs_round_df_edited.loc[i,'Spieler:in 1']
                            
                        else:
                            if spiele == 2:
                                scores_df.loc[spieler1_index, "Punktestand"]=scores_old_df.loc[spieler1_index_scores,"Punktestand"]+7
                            if spiele == 3:
                                scores_df.loc[spieler1_index, "Punktestand"]=scores_old_df.loc[spieler1_index_scores,"Punktestand"]+3
                            scores_df.loc[spieler1_index, "Siege"]=scores_old_df.loc[spieler1_index_scores,"Siege"]
                            scores_df.loc[spieler1_index, "Streaks (Runden ohne Niederlage)"]=scores_old_df.loc[spieler1_index_scores,"Streaks (Runden ohne Niederlage)"]
                            scores_df.loc[spieler1_index, "Niederlagen"]=scores_old_df.loc[spieler1_index_scores,"Niederlagen"]
                            scores_df.loc[spieler1_index, "Unentschieden"]=scores_old_df.loc[spieler1_index_scores,"Unentschieden"]
                            scores_df.loc[spieler1_index, "Freilose"]=scores_old_df.loc[spieler1_index_scores,"Freilose"]+1
                            for vorrunde in range(1,runde):
                                scores_df.loc[spieler1_index, "Gegner:in Runde "+str(vorrunde)]=scores_old_df.loc[spieler1_index_scores,"Gegner:in Runde "+str(vorrunde)]
                            scores_df.loc[spieler1_index, "Gegner:in Runde "+str(runde)]="Freilos"

                    for i in scores_df.index:
                        if pd.isnull(scores_df.loc[i,'Siege'])==True:
                            scores_df.loc[i]=scores_old_df[scores_old_df['Name']==scores_df.loc[i,'Name']].iloc[0]
                    
                    for i in scores_df.index:
                        punkte_alle_gegner=0
                        punkte_alle_gegnergegner=0
                        for r in range(1,runde+1):
                            gegner=scores_df.loc[i, "Gegner:in Runde "+str(r)]
                            if (gegner != "Freilos") & (gegner in scores_df['Name'].values):
                                punkte_gegner=scores_df[(scores_df["Name"]==gegner)]['Punktestand'].values[0]
                                punkte_alle_gegner=punkte_alle_gegner+punkte_gegner
                                gegner_index=scores_df[(scores_df["Name"]==gegner)].index[0]
                                for x in range(1,runde+1):
                                    gegnergegner=scores_df.loc[gegner_index, "Gegner:in Runde "+str(x)]
                                    if (gegnergegner != "Freilos") & (gegnergegner in scores_df['Name'].values):
                                        punkte_gegnergegner=scores_df[(scores_df["Name"]==gegnergegner)]['Punktestand'].values[0]
                                        punkte_alle_gegnergegner=punkte_alle_gegnergegner+punkte_gegnergegner 
                        scores_df.loc[i,'Punktestand der Gegner:innen']=punkte_alle_gegner
                        scores_df.loc[i,'Punktestand der Gegner:innen der Gegner:innen']=punkte_alle_gegnergegner    

                        
                        
                    if runde + 1 <= runden:    
                    
                        round_finished=st.form_submit_button("Spielstand nach Runde "+str(runde)+"...")
                        if round_finished:
                            st.session_state["round"+str(runde)+"_scores"]=scores_df
                    
                    else:
                        if topcut == 0:
                            round_finished=st.form_submit_button("Finaler Punktestand!")
                            if round_finished:
                                scores_df=scores_df.sort_values(['Punktestand', "Streaks (Runden ohne Niederlage)",'Punktestand der Gegner:innen','Punktestand der Gegner:innen der Gegner:innen'], ascending=[False,False,False,False])
                                scores_df.index=np.arange(1, len(scores_df)+1)
                                st.session_state["round"+str(runde)+"_scores"]=scores_df
                                st.write("Der 1. Platz geht an "+scores_df.loc[1,"Name"]+"! 🥳")
                                st.dataframe(st.session_state["round"+str(runde)+"_scores"], height=35*len(scores_df)+38)
                        else:
                            round_finished=st.form_submit_button("Zum finalem Punktestand vorm Topcut")
                            if round_finished:
                                st.session_state["topcut_start"]="start"
                                scores_df=scores_df.sort_values(['Punktestand',"Streaks (Runden ohne Niederlage)", 'Punktestand der Gegner:innen','Punktestand der Gegner:innen der Gegner:innen'], ascending=[False,False, False,False])
                                scores_df.index=np.arange(1, len(scores_df)+1)
                                st.session_state["round"+str(runde)+"_scores"]=scores_df
                                st.dataframe(st.session_state["round"+str(runde)+"_scores"], height=35*len(scores_df)+38)

if st.session_state["topcut_start"] == "start":
    st.header("Topcut")

    topcut=st.session_state["topcut"]
    score_swissrounds=st.session_state["round"+str(runde)+"_scores"]
    spieler_topcut=score_swissrounds.sort_values(['Punktestand',"Streaks (Runden ohne Niederlage)", 'Punktestand der Gegner:innen','Punktestand der Gegner:innen der Gegner:innen'], ascending=[False,False, False,False])
    st.dataframe(spieler_topcut.iloc[:topcut].reset_index(drop=True))

    if topcut == 4:
        #Halbfinale: 2 Spiele
        if type(st.session_state["result_Halbfinale"]) != pd.DataFrame:
            with st.form("Halbfinale"):
                st.header("Halbfinale")
                if st.session_state["Halbfinale"] == None:
                    #pair first last and middle two
                    pairing_halbfinale=pd.DataFrame(columns=['Spieler:in 1', 'Spieler:in 2',
                                                            "Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"])
                    pairing_halbfinale.loc[0, 'Spieler:in 1']= spieler_topcut.loc[1,"Name"]
                    pairing_halbfinale.loc[0, 'Spieler:in 2']= spieler_topcut.loc[4,"Name"]
                    pairing_halbfinale.loc[1, 'Spieler:in 1']= spieler_topcut.loc[2,"Name"]
                    pairing_halbfinale.loc[1, 'Spieler:in 2']= spieler_topcut.loc[3,"Name"]

                    st.write("Weiter geht's mit dem Halbfinale. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                    st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                    st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
                    pairs_halbfinale_edited = st.data_editor(pairing_halbfinale, height=35*len(pairing_halbfinale)+38, hide_index=True)
                    #st.dataframe(pairing_halbfinale)

                            #st.dataframe(pairs_round1_df)
                    halbfinale=st.form_submit_button("Halbfinale beendet")

                    if halbfinale:
                        st.session_state["result_Halbfinale"] = pairs_halbfinale_edited
            
        #Finale und Spiel um Platz 3: 2 Spiele
        if type(st.session_state["result_Halbfinale"]) == pd.DataFrame:
            with st.form("Finale"):   
                st.header("Finale")
                result_Halbfinale=st.session_state["result_Halbfinale"]
                ergebnisse_runde1=result_Halbfinale.loc[0, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                ergebnisse_runde2=result_Halbfinale.loc[1, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                pairing_finale=pd.DataFrame(columns=['Spieler:in 1', 
                                                     'Spieler:in 2',
                                                     "Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"],
                                                     index=["Finale"])
                if ergebnisse_runde1.count(1) > ergebnisse_runde1.count(2):
                    pairing_finale.loc["Finale", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 1']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 2']
                else:
                    pairing_finale.loc["Finale", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 2']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 1']
                if ergebnisse_runde2.count(1) > ergebnisse_runde2.count(2):
                    pairing_finale.loc["Finale", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 1']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 2']
                else:
                    pairing_finale.loc["Finale", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 2']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 1']
                    
                st.write("Weiter geht's mit dem Halbfinale. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")

                pairs_finale_edited = st.data_editor(pairing_finale, height=35*len(pairing_finale)+38, hide_index=True)
                finale=st.form_submit_button("Finale beendet")

                if finale:
                    st.session_state["result_Finale"] = pairs_finale_edited
                    ergebnisse_runde1=pairs_finale_edited.loc["Finale", ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                    #ergebnisse_runde2=pairs_finale_edited.loc["Spiel um Platz 3", ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].to_list()

                    if ergebnisse_runde1.count(1) > ergebnisse_runde1.count(2):
                        st.header("Finaler Punktestand")
                        st.write("🥳 1. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 1'])
                        #st.write("2. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 2'])
                    else:
                        st.write("🥳 1. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 2'])
                        #st.write("2. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 1'])

                    #if ergebnisse_runde2.count(1) > ergebnisse_runde2.count(2):
                        #st.write("3. Platz: "+pairs_finale_edited.loc["Spiel um Platz 3",'Spieler:in 1'])
                    #else:
                        #st.write("3. Platz: "+pairs_finale_edited.loc["Spiel um Platz 3",'Spieler:in 2'])
                        
                    st.write(" ")
                    st.write("Hier nochmal der Stand vor den Playoffs:")
                    st.dataframe(st.session_state["round"+str(runde)+"_scores"], height=35*len(st.session_state["round"+str(runde)+"_scores"])+38)

    elif topcut == 8:
        #Viertelfinale: 4 Spiele
        if type(st.session_state["result_Viertelfinale"]) != pd.DataFrame:
            with st.form("Viertelfinale"):
                st.header("Viertelfinale")
                if st.session_state["Viertelfinale"] == None:
                    #pair first last and middle two
                    pairing_viertelfinale=pd.DataFrame(columns=['Spieler:in 1'
                                                            'Spieler:in 2',
                                                            "Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"])
                    pairing_viertelfinale.loc[0, 'Spieler:in 1']= spieler_topcut.loc[1,"Name"]
                    pairing_viertelfinale.loc[0, 'Spieler:in 2']= spieler_topcut.loc[8,"Name"]
                    pairing_viertelfinale.loc[1, 'Spieler:in 1']= spieler_topcut.loc[2,"Name"]
                    pairing_viertelfinale.loc[1, 'Spieler:in 2']= spieler_topcut.loc[7,"Name"]
                    pairing_viertelfinale.loc[2, 'Spieler:in 1']= spieler_topcut.loc[3,"Name"]
                    pairing_viertelfinale.loc[2, 'Spieler:in 2']= spieler_topcut.loc[6,"Name"]
                    pairing_viertelfinale.loc[3, 'Spieler:in 1']= spieler_topcut.loc[4,"Name"]
                    pairing_viertelfinale.loc[3, 'Spieler:in 2']= spieler_topcut.loc[5,"Name"]

                    st.write("Weiter geht's mit dem Viertelfinale. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                    st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                    st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
                    pairs_viertelfinale_edited = st.data_editor(pairing_viertelfinale, height=35*len(pairing_viertelfinale)+38, hide_index=True)
                    #st.dataframe(pairing_halbfinale)

                            #st.dataframe(pairs_round1_df)
                    viertelfinale=st.form_submit_button("Viertelfinale beendet")

                    if viertelfinale:
                        st.session_state["result_Viertelfinale"] = pairs_viertelfinale_edited
        #Halbfinale: 2 Spiele
        if (type(st.session_state["result_Viertelfinale"]) == pd.DataFrame) & (type(st.session_state["result_Halbfinale"]) != pd.DataFrame):
            with st.form("Halbfinale"):
                st.header("Halbfinale")
                if st.session_state["Halbfinale"] == None:
                    #pair first last and middle two
                    pairs_viertelfinale_edited = st.session_state["result_Viertelfinale"]
                    sieger_viertelfinale=[]
                    for i in pairs_viertelfinale_edited.index:
                        count_1=pairs_viertelfinale_edited.loc[i, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist().count(1)
                        count_2=pairs_viertelfinale_edited.loc[i, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist().count(2)
                        if count_1 > count_2:
                            sieger_viertelfinale.append(1)
                        else:
                            sieger_viertelfinale.append(2)
                    pairing_halbfinale=pd.DataFrame(columns=['Spieler:in 1', 
                                                            'Spieler:in 2',
                                                            "Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"])
                    pairing_halbfinale.loc[0, 'Spieler:in 1']= pairs_viertelfinale_edited.loc[0, 'Spieler:in '+str(sieger_viertelfinale[0])]
                    pairing_halbfinale.loc[0, 'Spieler:in 2']= pairs_viertelfinale_edited.loc[1, 'Spieler:in '+str(sieger_viertelfinale[1])]
                    pairing_halbfinale.loc[1, 'Spieler:in 1']= pairs_viertelfinale_edited.loc[2, 'Spieler:in '+str(sieger_viertelfinale[2])]
                    pairing_halbfinale.loc[1, 'Spieler:in 2']= pairs_viertelfinale_edited.loc[3, 'Spieler:in '+str(sieger_viertelfinale[3])]
                    
                    st.write("Weiter geht's mit dem Halbfinale. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                    st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                    st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")
                    pairs_halbfinale_edited = st.data_editor(pairing_halbfinale, height=35*len(pairing_halbfinale)+38, hide_index=True)
                    #st.dataframe(pairing_halbfinale)

                            #st.dataframe(pairs_round1_df)
                    halbfinale=st.form_submit_button("Halbfinale beendet")

                    if halbfinale:
                        st.session_state["result_Halbfinale"] = pairs_halbfinale_edited
        #Finale und Spiel um Platz 3: 2 Spiele
        st.header("Finale")
        if type(st.session_state["result_Halbfinale"]) == pd.DataFrame:
            with st.form("Finale"):   
                st.header("Finale")
                result_Halbfinale=st.session_state["result_Halbfinale"]
                ergebnisse_runde1=result_Halbfinale.loc[0, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                ergebnisse_runde2=result_Halbfinale.loc[1, ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                pairing_finale=pd.DataFrame(columns=['Spieler:in 1', 
                                                     'Spieler:in 2',
                                                     "Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"],
                                                     index=["Finale"])
                if ergebnisse_runde1.count(1) > ergebnisse_runde1.count(2):
                    pairing_finale.loc["Finale", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 1']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 2']
                else:
                    pairing_finale.loc["Finale", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 2']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 1']=result_Halbfinale.loc[0, 'Spieler:in 1']
                if ergebnisse_runde2.count(1) > ergebnisse_runde2.count(2):
                    pairing_finale.loc["Finale", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 1']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 2']
                else:
                    pairing_finale.loc["Finale", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 2']
                    #pairing_finale.loc["Spiel um Platz 3", 'Spieler:in 2']=result_Halbfinale.loc[1, 'Spieler:in 1']
                
                st.write("Weiter geht's mit dem Halbfinale. Bitte trage nach der Runde in die Spielergebnis-Spalten den Ausgang des jeweiligen Spiels ein.")
                st.write("*1 - Sieg von Spieler:in 1; 2 - Sieg von Spieler:in 2*")
                st.write("Falls die Spielergebnis-Spalten nicht sichtbar sein sollten, bitte nach rechts sliden oder die Tabelle maximieren.")

                pairs_finale_edited = st.data_editor(pairing_finale, height=35*len(pairing_finale)+38, hide_index=True)
                finale=st.form_submit_button("Finale beendet - weiter zum Ranking")

                if finale:
                    st.session_state["result_Finale"] = pairs_finale_edited
                    ergebnisse_runde1=pairs_finale_edited.loc["Finale", ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].values.astype(int).tolist()
                    #ergebnisse_runde2=pairs_finale_edited.loc["Spiel um Platz 3", ["Spielergebnis - Spiel 1","Spielergebnis - Spiel 2","Spielergebnis - Spiel 3"]].to_list()

                    if ergebnisse_runde1.count(1) > ergebnisse_runde1.count(2):
                        st.header("Finaler Punktestand")
                        st.write("🥳 1. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 1'])
                        #st.write("2. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 2'])
                    else:
                        st.write("🥳 1. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 2'])
                        #st.write("2. Platz: "+pairs_finale_edited.loc["Finale",'Spieler:in 1'])

                    # if ergebnisse_runde2.count(1) > ergebnisse_runde2.count(2):
                    #     st.write("3. Platz: "+pairs_finale_edited.loc["Spiel um Platz 3",'Spieler:in 1'])
                    # else:
                    #     st.write("3. Platz: "+pairs_finale_edited.loc["Spiel um Platz 3",'Spieler:in 2'])
                        
                    st.write(" ")
                    st.write("Hier nochmal der Stand vor den Playoffs:")
                    st.dataframe(st.session_state["round"+str(runde)+"_scores"], height=35*len(st.session_state["round"+str(runde)+"_scores"])+38)

            #st.dataframe(st.session_state["pairs_round1_df"])


    #         #     if spiele == 3:
    #         # scores_df.loc[spieler1_index,"Punktestand"]=0
    #         # scores_df[spieler1_index,"Anzahl Siege"]=0
    #     scores_df_edited=st.data_editor(scores_df)

# #st.rerun()
