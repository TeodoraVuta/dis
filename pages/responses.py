import streamlit as st
from db_utils import get_connection, close_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from country_list import countries_for_language


st.title("📋 Răspunsuri colectate")

def get_survey_data():
    conn, cursor = get_connection()
    if conn is None:
        st.error("Nu s-a putut stabili conexiunea la baza de date.")
        return pd.DataFrame()  
    query = "SELECT * FROM responses"
    df = pd.read_sql(query, conn)
    close_connection(conn, cursor)
    return df

df = get_survey_data()

educatie_standard = {
    "Bachelor's Degree": "Licență",
    "Licenta": "Licență",
    "Licen??" : "Licență",
    "licență": "Licență",
    "Master's Degree": "Master",
    "Master": "Master",
    "masterat": "Master",
    "High School": "Liceu",
    "Liceu": "Liceu",
    "PhD": "Doctorat",
    "Doctorat": "Doctorat", 
    "?coala Primar?" : "Școală Primară",
    "?coala General?" : "Școală Generală",
}
    
gender_standard = {
    "Female": "Feminin",
    "Male": "Masculin",
    "Non-binary/Third gender": "Non-binary",
    "Prefer not to say" : "Prefer să nu spun",
    "Feminin" : "Feminin",
    "Masculin" : "Masculin",
    "Non-binar/Al treilea gen" : "Non-binary",
    "Prefer s? nu spun" : "Prefer să nu spun",
}

ro_countries = dict(countries_for_language('ro'))
country_standard = {v: k for k, v in ro_countries.items()}
country_standard["România"] = "Romania"  # Asigură-te că România este inclusă corect

    

df['educatie_standard'] = df['education'].replace(educatie_standard)
df['gender_standard'] = df['gender'].replace(gender_standard)
df['country_standard'] = df['country'].replace(country_standard)

# Construiește listele de opțiuni, incluzând "Toate"
education_options = ['Toate'] + sorted(df['educatie_standard'].dropna().unique().tolist())
gender_options = ['Toate'] + sorted(df['gender_standard'].dropna().unique().tolist())
country_options = ['Toate'] + sorted(df['country_standard'].dropna().unique().tolist())


if not df.empty:
    col_filters, col_table = st.columns([1, 3])

    with col_filters: 
        selected_sex = st.multiselect("Selectează sexul:", options=gender_options, default=["Toate"])
        selected_education = st.multiselect("Selectează nivelul de educație:", options=education_options, default=["Toate"])
        selected_country = st.multiselect("Selectează țara:", options=country_options, default=["Toate"])


    # Funcție de filtrare care ține cont de "Toate" ca valoare specială
    def filtreaza_date(df, sex_sel, educ_sel, country_sel):
        if "Toate" in sex_sel:
            filtru_sex = df.index == df.index  # True pentru toate rândurile
        else:
            filtru_sex = df['gender_standard'].isin(sex_sel)

        if "Toate" in educ_sel:
            filtru_educ = df.index == df.index
        else:
            filtru_educ = df['educatie_standard'].isin(educ_sel)
        
        if "Toate" in country_sel:
            filtru_country = df.index == df.index
        else:
            filtru_country = df['country_standard'].isin(selected_country)

        return df[filtru_sex & filtru_educ & filtru_country]

    filtered_df = filtreaza_date(df, selected_sex, selected_education, selected_country)

    with col_table:
        if not filtered_df.empty:
            counts = filtered_df['educatie_standard'].value_counts()
            st.bar_chart(counts)
        else:
            st.warning("Nu există date pentru selecția curentă.")

else:
    st.warning("Nu există date disponibile pentru afișare.")