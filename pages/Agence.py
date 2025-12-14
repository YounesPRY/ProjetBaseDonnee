from db import get_connection
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Agences de voyage" ,layout="wide")
st.title("Agences de voyage") 

connection = get_connection()

st.subheader("📊 Indicateurs clés")

c1, c2, c3 = st.columns(3)

nbr_agences_distinct = pd.read_sql("select distinct count(*) from AGENCE_DE_VOYAGE", connection)
nbr_villes_distinct = pd.read_sql("select distinct count(*) from AGENCE_DE_VOYAGE", connection)
ville_max_agences = pd.read_sql(
    "select VILLE_Nom_Ville from AGENCE_DE_VOYAGE GROUP by VILLE_Nom_Ville "
    "having count(*) = (select max(nbr) from "
    "(select count(*) as nbr from AGENCE_DE_VOYAGE GROUP by VILLE_Nom_Ville) as t1)", connection
)

nbr_agences = nbr_agences_distinct.iloc[0, 0]
nbr_villes_distinct = nbr_villes_distinct.iloc[0, 0]

# display metrics using columns
c1.metric("Nombre d'agences", nbr_agences, delta=f"{nbr_agences} total")
c2.metric("Nombre de villes", nbr_villes_distinct)
c3.metric("Ville avec le plus d'agences", ville_max_agences.iloc[0,0] if not ville_max_agences.empty else "N/A")



# --- MAP ---
st.subheader("🗺 Localisation des agences")
data_frame_map = pd.read_sql(
    "select Longitude , Latitude from VILLE v, AGENCE_DE_VOYAGE ag where v.Nom_Ville = ag.VILLE_Nom_Ville", connection
)
st.map(data_frame_map.rename(columns={"Latitude": "lat", "Longitude": "lon"}))

st.markdown("---")

# --- TABLE OF ALL AGENCIES ---
st.subheader("Liste complète des agences")
data_frame_all_agences = pd.read_sql(
    "select Cod_A , Site_web , Telephone , CONCAT(Adresse_Num_A , ' ' , Adresse_Rue_A ,' ',  VILLE_Nom_Ville ,' ',  Adresse_Pays_A, ' ,' ,Adresse_Code_Postal) as Adresse "
    "from AGENCE_DE_VOYAGE", connection
)

st.dataframe(
    data_frame_all_agences[["Cod_A", "Adresse", "Telephone", "Site_web"]],
    use_container_width=True,
    height=350
)

st.markdown("---")

# --- SEARCH BY CITY ---
st.subheader("Rechercher des agences par ville")
ville_recherchee = st.text_input("Nom de la ville", placeholder="Ex : Rome, Bruxelles, Paris")

if ville_recherchee:
    sqlQuery = (
        "select Cod_A , Site_web , Telephone , CONCAT(Adresse_Num_A , ' ' , Adresse_Rue_A ,' ',  VILLE_Nom_Ville ,' ',  Adresse_Pays_A, ' ,' ,Adresse_Code_Postal) as Adresse "
        "from AGENCE_DE_VOYAGE "
        "where VILLE_Nom_Ville like %s"
    )
    data_frame_agences_ville = pd.read_sql(sqlQuery, connection, params=[ville_recherchee])
    
    if data_frame_agences_ville.empty:
        st.warning("Aucune agence trouvée dans cette ville.")
    else:
        st.dataframe(
            data_frame_agences_ville[["Cod_A", "Adresse", "Telephone", "Site_web"]],
            use_container_width=True,
        )
else:
    st.info("Veuillez entrer le nom d'une ville pour rechercher des agences.")

connection.close()
