import csv
import streamlit as st
from db_utils import get_connection, close_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from country_list import countries_for_language
from db_utils import show_logged_in_user
import statsmodels.api as sm
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


show_logged_in_user()

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

df['age'] = pd.to_numeric(df['age'], errors='coerce')

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

platform_standard = {
    "Coursera": "Coursera",
    "Udemy": "Udemy",
    "edX": "edX",
    "LinkedIn Learning": "LinkedIn Learning",
    "Khan Academy": "Khan Academy",
    "YouTube": "YouTube",
    "TikTok": "TikTok",
    "Platforma de la facultate/scoala (Moodle)": "Platforma de la facultate/scoala",
    "My university's platform" : "Platforma de la facultate/scoala",
    # "Altele": "Altele",
    # "Others": "Altele",

}

couses_standard = {
        "Tehnic (Programare, Data Science)" : "Tehnic (Programare, Data Science)",
        "Business & Management" : "Business & Management", 
        "Finanțe & Economie" : "Finanțe & Economie",
        "Lingvistică & Limbi Străine": "Lingvistică & Limbi Străine", 
        "Psihologie & Comportament Uman" : "Psihologie & Comportament Uman", 
        "Tehnologii Emergente (AI, Blockchain, etc.)" : "Tehnologii Emergente",
        "Mediu & Sustenabilitate" : "Mediu & Sustenabilitate", 
        "Design & Grafică" : "Design & Grafică", 
        "Călătorii & Turism" : "Călătorii & Turism", 
        "Antreprenoriat"    : "Antreprenoriat", 
        "Dezvoltare Personală" : "Dezvoltare Personală", 
        "Artă & Științe Umaniste" : "Artă & Științe Umaniste", 
        "Sănătate & Medicină"   : "Sănătate & Medicină", 
        "Activități Sportive" : "Activități Sportive",
        "Îngrijirea copilului și viața de familie" : "Îngrijirea copilului și viața de familie",  
        # "Altele" : "Altele",
        "Technical (Programming, Data Science)" : "Tehnic (Programare, Data Science)",
        "Business & Management" : "Business & Management", 
        "Finance & Economics" : "Finanțe & Economie", 
        "Finan?e & Economie" : "Finanțe & Economie",
        "Linguistics & Foreign Languages" : "Lingvistică & Limbi Străine", 
        "Lingvistic? & Limbi Str?ine" : "Lingvistică & Limbi Străine",
        "Psychology & Human Behavior"   : "Psihologie & Comportament Uman", 
        "Emerging Technologies (AI, Blockchain, etc.)" : "Tehnologii Emergente", 
        "Environment & Sustainability"  : "Mediu & Sustenabilitate", 
        "Design & Graphics" : "Design & Grafică",
        "Design & Grafic?" : "Design & Grafică",
        "Travel & Tourism"  : "Călătorii & Turism", 
        "C?al?tori?i & Turism" : "Călătorii & Turism",
        "Entrepreneurship" : "Antreprenoriat", 
        "Personal Development"  : "Dezvoltare Personală", 
        "Dezvoltare Personal?" : "Dezvoltare Personală",
        "Arts & Humanities" : "Artă & Științe Umaniste",
        "Art? & ?tiin?e Umaniste" : "Artă & Științe Umaniste",
        "Health & Medicine" : "Sănătate & Medicină", 
        "Săn?tate & Medicin?" : "Sănătate & Medicină",
        "Sports Activities" : "Activități Sportive", 
        "Activit??i Sportive" : "Activități Sportive",
        "Childcare & Family Life"   : "Îngrijirea copilului și viața de familie", 
        "?ngrijirea copilului ?i via?a de familie" : "Îngrijirea copilului și viața de familie",
        # "Others" : "Altele",

}

reasons_standard = {
    "Locul de muncă": "Locul de muncă",
    "Locul de munc?": "Locul de muncă",       
    "Interes personal": "Interes personal",
    "Școală": "Școală",
    "?coală": "Școală",                       
    "?coal?": "Școală",
    "Job Purposes": "Locul de muncă",
    "Personal interest": "Interes personal",
    "School purposes": "Școală",
    "Locul de munc?": "Locul de muncă",
}

def fix_diacritics(text):
    if pd.isna(text):
        return text
    return text.replace("?", "ă").replace("??", "ș").replace("?coala", "Școala").replace("ăcoală", "Școală").replace("ăcoală", "Școală").replace("Locul de munc?", "Locul de muncă").replace("Personal interest", "Interes personal").replace("School purposes", "Școală")

df['selected_usage'] = df['selected_usage'].apply(fix_diacritics)

reasons_standard = {
    "Locul de muncă" : "Locul de muncă", 
    "Interes personal" : "Interes personal", 
    "Școală" : "Școală",
    "Job Purposes" : "Locul de muncă",
    "Personal interest" : "Interes personal", 
    "School purposes" : "Școală",
    "?coal?" : "Școală",
    "ăcoală" : "Școală",
    "Locul de munc?" : "Locul de muncă",
}

df['reasons_standard'] = df['selected_usage'].replace(reasons_standard)

ro_countries = dict(countries_for_language('ro')) 

iso_to_ro = ro_countries.copy()
english_to_iso = {v: k for k, v in countries_for_language('en')} 

country_standard = {}

for eng_name, iso_code in english_to_iso.items():
    if iso_code in iso_to_ro:
        country_standard[eng_name] = iso_to_ro[iso_code]

for iso_code, ro_name in iso_to_ro.items():
    country_standard[iso_code] = ro_name


def fix_platforms(text):
    if pd.isna(text):
        return text
    return (text
        .replace("Platforma de la facultate/scoala (Moodle)", "Platforma de la facultate/scoala")
        .replace("Platforma de la facultate/scoala", "Platforma de la facultate/scoala")
        .replace("My university's platform", "Platforma de la facultate/scoala")
        .replace("google", "Google")
        # .replace("Altele", "Altele")
        # .replace("Others", "Altele")
    )

def fix_courses(text):
    if pd.isna(text):
        return text
    return (text
        .replace("Technical (Programming, Data Science)", "Tehnic (Programare & Data Science)")
        .replace("Tehnic (Programare, Data Science)", "Tehnic (Programare & Data Science)")
        # .replace("Tehnic (Programare", "Tehnic (Programare & Data Science)")
        # .replace("Tehnic (Programare & Tehnic (Programare", "Tehnic (Programare & Data Science)")
        # .replace("Data Science)", "Tehnic (Programare & Data Science)")
        .replace("Business & Management", "Business & Management")
        .replace("Finance & Economics", "Finanțe & Economie")
        .replace("Finan?e & Economie", "Finanțe & Economie")
        .replace("Linguistics & Foreign Languages", "Lingvistică & Limbi Străine")
        .replace("Lingvistic? & Limbi Str?ine", "Lingvistică & Limbi Străine")
        .replace("Psychology & Human Behavior", "Psihologie & Comportament Uman")
        .replace("Emerging Technologies (AI, Blockchain, etc.)", "Tehnologii Emergente")
        .replace("Tehnologii Emergente (AI", "Tehnologii Emergente")
        .replace("Blockchain", "Tehnologii Emergente")
        .replace("etc.)", "Tehnologii Emergente")
        .replace("Environment & Sustainability", "Mediu & Sustenabilitate")
        .replace("Design & Graphics", "Design & Grafică")
        .replace("Design & Grafic?", "Design & Grafică")
        .replace("Travel & Tourism", "Călătorii & Turism")
        .replace("C?l?torii & Turism", "Călătorii & Turism")
        .replace("Entrepreneurship", "Antreprenoriat")
        .replace("Personal Development", "Dezvoltare Personală")
        .replace("Dezvoltare Personal?", "Dezvoltare Personală")
        .replace("Arts & Humanities", "Artă & Științe Umaniste")
        .replace("Art? & ?tiin?e Umaniste", "Artă & Științe Umaniste")
        .replace("Health & Medicine", "Sănătate & Medicină")
        .replace("Săn?tate & Medicin?", "Sănătate & Medicină")
        .replace("S?n?tate & Medicin?", "Sănătate & Medicină")
        .replace("Îngrijirea copilului ?i via?a de familie", "Îngrijirea copilului și viața de familie")
        .replace("Sports Activities", "Activități Sportive")
        .replace("Activit??i Sportive", "Activități Sportive")
        .replace("Childcare & Family Life", "Îngrijirea copilului și viața de familie")
        .replace("?ngrijirea copilului ?i via?a de familie", "Îngrijirea copilului și viața de familie")
    )

df['country_standard'] = df['country'].replace(country_standard).str.upper().dropna()
df['educatie_standard'] = df['education'].replace(educatie_standard).str.upper().dropna()
df['gender_standard'] = df['gender'].replace(gender_standard).str.upper().dropna()
df['platform_standard'] = df['selected_platforms'].apply(fix_platforms).str.upper().str.split(',').apply(
    lambda lst: [x.strip() for x in lst if x.strip()] if isinstance(lst, list) else [])
df['course_standard'] = df['selected_courses'].apply(fix_courses).str.upper().str.split(',').apply(
    lambda lst: [x.strip() for x in lst if x.strip()] if isinstance(lst, list) else [])
df['reasons_standard'] = df['selected_usage'].replace(reasons_standard).str.upper().str.split(',').apply(
    lambda lst: [x.strip() for x in lst if x.strip()] if isinstance(lst, list) else [])

education_options = ['Toate'] + sorted(df['educatie_standard'].dropna().unique().tolist())
gender_options = ['Toate'] + sorted(df['gender_standard'].dropna().unique().tolist())
country_options = ['Toate'] + sorted(df['country_standard'].dropna().unique().tolist())
platform_options = ['Toate'] + sorted(df['platform_standard'].explode().dropna().unique().tolist())
course_options = ['Toate'] + sorted(df['course_standard'].explode().dropna().unique().tolist())
reasons_options = ['Toate'] + sorted(df['reasons_standard'].explode().dropna().unique().tolist())


st.markdown("### Customizeaza selectia:")

demografics_data = st.checkbox("Date demografice", value=True)
elearning_data = st.checkbox("Despre e-learning", value=False)

def handle_multiselect(label, key, options):
    current = st.session_state.get(key, [])

    if "Toate" in current and len(current) > 1:
        st.warning("Pentru a selecta opțiuni individuale, elimină 'Toate'.")
        # Nu modificăm direct session_state[key], ci folosim callback
        st.experimental_rerun()

    # opțiuni „dezactivate vizual” dacă e selectat „Toate”
    fake_options = (
        ["Toate"] + [f"{opt} (dezactivat)" for opt in options if opt != "Toate"]
        if "Toate" in current else options
    )

    # selectăm doar ce e valid
    default_selection = [opt for opt in current if opt in options]

    new_selection = st.multiselect(
        label=label,
        options=fake_options,
        default=default_selection,
        key=key,
        placeholder="Selectează..."
    )

    # curățăm selecția de opțiuni „dezactivate” simulate
    clean_selection = [opt for opt in new_selection if not opt.endswith("(dezactivat)")]

    # salvăm indirect, cu workaround (fără să atingem direct session_state[key])
    if clean_selection != current:
        st.session_state.update({key: clean_selection})
        st.experimental_rerun()


def filtreaza_date_demografics(df, sex_sel, educ_sel, country_sel, age_range=None):
    if "Toate" in sex_sel:
        filtru_sex = df.index == df.index
    else:
        filtru_sex = df['gender_standard'].isin(sex_sel)
    if "Toate" in educ_sel:
        filtru_educ = df.index == df.index
    else:
        filtru_educ = df['educatie_standard'].isin(educ_sel)
    if "Toate" in country_sel:
        filtru_country = df.index == df.index
    else:
        filtru_country = df['country_standard'].isin(country_sel)
    
    if age_range is not None:
        filtru_age = df['age'].between(age_range[0], age_range[1])
    else:
        filtru_age = df.index == df.index
    return df[filtru_sex & filtru_educ & filtru_country & filtru_age]


def filtreaza_date_elearning(df, platform_sel, courses_sel, reasons_sel):
    if "Toate" in platform_sel:
        filtru_platform = df.index == df.index
    else:
        filtru_platform = df['platform_standard'].isin(platform_sel)

    if "Toate" in courses_sel:
        filtru_courses = df.index == df.index
    else:
        filtru_courses = df['courses_standard'].isin(courses_sel)

    if "Toate" in reasons_sel:
        filtru_reasons = df.index == df.index
    else:
        filtru_reasons = df['reasons_standard'].isin(reasons_sel)

    return df[filtru_platform & filtru_courses & filtru_reasons]

if not df.empty:
    if demografics_data:
        col_filters_sex, col_filters_education, col_filters_country = st.columns(3)

        with col_filters_sex:
            handle_multiselect("Genul:", "selected_sex", gender_options)
        with col_filters_education:
            handle_multiselect("Nivelul de educație:", "selected_education", education_options)
        with col_filters_country:
            handle_multiselect("țara:", "selected_country", country_options)

        selected_sex = st.session_state["selected_sex"]
        selected_education = st.session_state["selected_education"]
        selected_country = st.session_state["selected_country"]
    else:
        selected_sex = ["Toate"]
        selected_education = ["Toate"]
        selected_country = ["Toate"]

    if elearning_data:
        col_filters_platform, col_filters_courses, col_filters_reasons= st.columns(3)
        with col_filters_platform:
            handle_multiselect("Platforma de e-learning:", "selected_platform", platform_options)
        with col_filters_courses:
            handle_multiselect("Tipul cursurilor:", "selected_courses", course_options)
        with col_filters_reasons:
            handle_multiselect("Motivele pentru e-learning:", "selected_reasons", reasons_options)

        selected_platform = st.session_state["selected_platform"]
        selected_courses = st.session_state["selected_courses"]
        selected_reasons = st.session_state["selected_reasons"]
    else:
        selected_platform = ["Toate"]
        selected_courses = ["Toate"]
        selected_reasons = ["Toate"]


def afiseaza_date_demografice(filtered_df):
    st.markdown("### 📊 Date demografice")

    st.write("#### Distribuția pe genuri")
    gender_counts = filtered_df['gender_standard'].value_counts()
    st.bar_chart(gender_counts)

    st.write("#### Distribuția pe nivel de educație")
    education_counts = filtered_df['educatie_standard'].value_counts()
    st.bar_chart(education_counts)

    st.write("#### Distribuția pe țări")
    country_counts = filtered_df['country_standard'].value_counts().head(10)
    st.bar_chart(country_counts)

    st.write("#### Distribuția pe vârste")
    fig_age = px.histogram(
        filtered_df, x='age', nbins=20,
        labels={'age': 'Vârstă', 'count': 'Număr respondenți'},
    )
    st.plotly_chart(fig_age, use_container_width=True)

def stacked_bar_cursuri(df):
    st.write("#### Cursuri urmarite în funcție de dimensiunea selectată")

    dim_options = ["Gen", "Țară", "Nivel de educație"]
    coloane = {
        "Gen": "gender_standard",
        "Țară": "country_standard",
        "Nivel de educație": "educatie_standard"
    }

    selected_dim = st.selectbox("Alege dimensiunea pentru stacked bar:", dim_options)
    coloana = coloane[selected_dim]

    df_courses = df.explode('course_standard')
    df_courses = df_courses.dropna(subset=['course_standard', coloana])
    df_courses = df_courses[df_courses['course_standard'] != '']

    selected_courses = st.session_state.get("selected_courses", ["Toate"])
    if selected_courses and "Toate" not in selected_courses:
        df_courses = df_courses[df_courses['course_standard'].isin(selected_courses)]

    top_courses = df_courses['course_standard'].value_counts().nlargest(10).index.tolist()
    df_courses = df_courses[df_courses['course_standard'].isin(top_courses)]
    course_counts = df_courses.groupby(['course_standard', coloana]).size().reset_index(name='count')

    if course_counts.empty:
        st.info("Nu există suficiente date pentru afișarea graficului.")
        return

    # 📊 Plot
    fig = px.bar(
        course_counts,
        x='course_standard',
        y='count',
        color=coloana,
        barmode='stack',
        labels={'course_standard': 'Tip curs', 'count': 'Număr respondenți'},
        title=f'Cursuri urmarite în funcție de {selected_dim.lower()}'
    )
    fig.update_layout(xaxis_title='Tip curs', yaxis_title='Număr respondenți', xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)



def stacked_bar_platforme(df):
    st.write("#### Platforme folosite (în funcție de dimensiune)")

    dim_options = ["Gen", "Țară", "Nivel de educație"]
    coloane = {
        "Gen": "gender_standard",
        "Țară": "country_standard",
        "Nivel de educație": "educatie_standard"
    }

    selected_dim = st.selectbox(
        "Alege dimensiunea pentru platforme:",
        dim_options,
        index=dim_options.index("Gen")
    )

    coloana = coloane[selected_dim]

    df_platforms = df.explode('platform_standard')
    df_platforms = df_platforms.dropna(subset=['platform_standard', coloana])
    df_platforms = df_platforms[df_platforms['platform_standard'] != '']

    platform_counts = df_platforms.groupby(['platform_standard', coloana]).size().reset_index(name='count')
    top_platforms = df_platforms['platform_standard'].value_counts().nlargest(10).index.tolist()
    platform_counts = platform_counts[platform_counts['platform_standard'].isin(top_platforms)]

    fig = px.bar(
        platform_counts,
        x='platform_standard',
        y='count',
        color=coloana,
        barmode='stack',
        labels={'platform_standard': 'Platformă', 'count': 'Număr respondenți'},
        title=f'Platforme în funcție de {selected_dim.lower()}'
    )
    fig.update_layout(xaxis_title='Platformă', yaxis_title='Număr respondenți', xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)


def stacked_bar_motive(df):
    st.write("#### Motive pentru folosirea e-learningului (în funcție de dimensiune)")

    dim_options = ["Gen", "Țară", "Nivel de educație"]
    coloane = {
        "Gen": "gender_standard",
        "Țară": "country_standard",
        "Nivel de educație": "educatie_standard"
    }

    # Select box dinamic
    selected_dim = st.selectbox(
        "Alege dimensiunea pentru motive:",
        dim_options,
        index=dim_options.index(st.session_state.get("motive_dim", "Gen")),
        key="dimensiune_motive_selectata"
    )

    # Salvăm în session_state
    st.session_state["motive_dim"] = selected_dim
    coloana = coloane[selected_dim]

    # 🔄 Explode + curățare
    df_reasons = df.explode('reasons_standard')
    df_reasons = df_reasons.dropna(subset=['reasons_standard', coloana])
    df_reasons = df_reasons[df_reasons['reasons_standard'].str.strip() != '']

    # 🔝 Top 10 motive din datele deja filtrate
    top_reasons = df_reasons['reasons_standard'].value_counts().nlargest(10).index.tolist()
    df_top = df_reasons[df_reasons['reasons_standard'].isin(top_reasons)]

    # Grupare
    reason_counts = df_top.groupby(['reasons_standard', coloana]).size().reset_index(name='count')

    # 📊 Plot
    fig = px.bar(
        reason_counts,
        x='reasons_standard',
        y='count',
        color=coloana,
        barmode='stack',
        labels={'reasons_standard': 'Motiv', 'count': 'Număr respondenți'},
        title=f'Motive pentru e-learning în funcție de {selected_dim.lower()}'
    )
    fig.update_layout(xaxis_title='Motiv', yaxis_title='Număr respondenți', xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)



def afiseaza_date_elearning_charts(filtered_df):
    st.markdown("### 💻 Date despre e-learning")

    stacked_bar_platforme(filtered_df)
    stacked_bar_cursuri(filtered_df) 
    stacked_bar_motive(filtered_df)




def filtreaza_toate_datele(df, sex_sel, educ_sel, country_sel, platform_sel, courses_sel, reasons_sel, age_range=None):
    df_filtered = df.copy()

    # Filtre demografice
    if "Toate" not in sex_sel:
        df_filtered = df_filtered[df_filtered['gender_standard'].isin(sex_sel)]
    if "Toate" not in educ_sel:
        df_filtered = df_filtered[df_filtered['educatie_standard'].isin(educ_sel)]
    if "Toate" not in country_sel:
        df_filtered = df_filtered[df_filtered['country_standard'].isin(country_sel)]
    if age_range is not None:
        df_filtered = df_filtered[df_filtered['age'].between(age_range[0], age_range[1])]

    # Filtrare e-learning pentru liste
    if "Toate" not in platform_sel:
        df_filtered = df_filtered[df_filtered['platform_standard'].apply(
            lambda lst: any(p in lst for p in platform_sel) if isinstance(lst, list) else False
        )]
    if "Toate" not in courses_sel:
        df_filtered = df_filtered[df_filtered['course_standard'].apply(
            lambda lst: any(c in lst for c in courses_sel) if isinstance(lst, list) else False
        )]
    if "Toate" not in reasons_sel:
        df_filtered = df_filtered[df_filtered['reasons_standard'].apply(
            lambda lst: any(r in lst for r in reasons_sel) if isinstance(lst, list) else False
        )]

    return df_filtered


# def filtreaza_toate_datele(df, sex_sel, educ_sel, country_sel, platform_sel, courses_sel, reasons_sel, age_range=None):
#     df_filtered = df.copy()

#     # Filtre demografice
#     if "Toate" not in sex_sel:
#         df_filtered = df_filtered[df_filtered['gender_standard'].isin(sex_sel)]
#     if "Toate" not in educ_sel:
#         df_filtered = df_filtered[df_filtered['educatie_standard'].isin(educ_sel)]
#     if "Toate" not in country_sel:
#         df_filtered = df_filtered[df_filtered['country_standard'].isin(country_sel)]
#     if age_range is not None:
#         df_filtered = df_filtered[df_filtered['age'].between(age_range[0], age_range[1])]

#     # Filtrare e-learning
#     if "Toate" not in platform_sel:
#         df_filtered = df_filtered[df_filtered['platform_standard'].apply(lambda lst: any(x in lst for x in platform_sel))]
#     if "Toate" not in courses_sel:
#         df_filtered = df_filtered[df_filtered['course_standard'].apply(lambda lst: any(x in lst for x in courses_sel))]
#     if "Toate" not in reasons_sel:
#         df_filtered = df_filtered[df_filtered['reasons_standard'].apply(lambda lst: any(x in lst for x in reasons_sel))]

#     return df_filtered


def afiseaza_date_demografice(df):
    st.markdown("### 📊 Date demografice")

    st.write("#### Distribuția pe genuri")
    st.bar_chart(df['gender_standard'].value_counts())

    st.write("#### Distribuția pe nivel de educație")
    st.bar_chart(df['educatie_standard'].value_counts())

    st.write("#### Distribuția pe țări")
    st.bar_chart(df['country_standard'].value_counts().head(10))

    st.write("#### Distribuția pe vârste")
    fig = px.histogram(df, x='age', nbins=20, labels={'age': 'Vârstă'})
    st.plotly_chart(fig, use_container_width=True)


# 🔘 Butonul principal
if st.button("Afișează datele filtrate"):
    st.subheader("Date filtrate")

    selected_sex = selected_sex or ["Toate"]
    selected_education = selected_education or ["Toate"]
    selected_country = selected_country or ["Toate"]
    selected_platform = selected_platform or ["Toate"]
    selected_courses = selected_courses or ["Toate"]
    selected_reasons = selected_reasons or ["Toate"]

    df_filtrat = filtreaza_toate_datele(
        df,
        selected_sex,
        selected_education,
        selected_country,
        selected_platform,
        selected_courses,
        selected_reasons,
    )

    st.session_state["df_filtrat"] = df_filtrat

    if df_filtrat.empty:
        st.warning("Nu există date pentru selecția curentă.")

if "df_filtrat" in st.session_state and not st.session_state["df_filtrat"].empty:
    df_filtrat = st.session_state["df_filtrat"]

    if demografics_data:
        afiseaza_date_demografice(df_filtrat)
    if elearning_data:
        afiseaza_date_elearning_charts(df_filtrat)
    

def genereaza_insighturi(df):
    st.subheader("📍 Insight-uri automate")
    
    if df.empty:
        st.info("Nu există date filtrate pentru a genera insight-uri.")
        return

    try:
        # GEN
        gender_counts = df['gender_standard'].dropna().value_counts()
        if not gender_counts.empty:
            top_gender = gender_counts.idxmax().capitalize()
            top_gender_pct = gender_counts.max() / gender_counts.sum() * 100
            st.markdown(f"👥 **{top_gender}** reprezintă **{top_gender_pct:.1f}%** dintre respondenți.")

        # ȚARĂ
        country_counts = df['country_standard'].dropna().value_counts()
        if not country_counts.empty:
            top_country = country_counts.idxmax().title()
            top_country_pct = country_counts.max() / country_counts.sum() * 100
            st.markdown(f"🌍 Cei mai mulți respondenți sunt din **{top_country}** (**{top_country_pct:.1f}%**).")

        # EDUCAȚIE
        edu_counts = df['educatie_standard'].dropna().value_counts()
        if not edu_counts.empty:
            top_edu = edu_counts.idxmax().capitalize()
            st.markdown(f"🎓 Nivelul de educație predominant este **{top_edu}**.")

        # PLATFORME
        platforme = df.explode('platform_standard')
        platform_counts = platforme['platform_standard'].dropna().str.strip().value_counts()
        if not platform_counts.empty:
            top_platforms = platform_counts.head(2).index.tolist()
            st.markdown(f"💻 Platformele cele mai utilizate sunt: **{top_platforms[0]}** și **{top_platforms[1]}**.")

        # CURSURI
        cursuri = df.explode('course_standard')
        course_counts = cursuri['course_standard'].dropna().str.strip().value_counts()
        if not course_counts.empty:
            top_courses = course_counts.head(2).index.tolist()
            st.markdown(f"📚 Cele mai frecvente tipuri de cursuri urmate sunt: **{top_courses[0]}** și **{top_courses[1]}**.")

        # MOTIVE
        motive = df.explode('reasons_standard')
        reason_counts = motive['reasons_standard'].dropna().str.strip().value_counts()
        if not reason_counts.empty:
            top_reasons = reason_counts.head(2).index.tolist()
            st.markdown(f"🎯 Motivele principale pentru care e-learning este ales sunt: **{top_reasons[0]}** și **{top_reasons[1]}**.")
    
    except Exception as e:
        st.error(f"Eroare la generarea insight-urilor: {e}")


col1, col2 = st.columns(2)
with col1:
    if st.button("Generează insight-uri"):
        if "df_filtrat" not in st.session_state or st.session_state["df_filtrat"].empty:
            st.warning("Nu există date filtrate pentru a genera insight-uri.")
        else:
            if "df_filtrat" in st.session_state and not st.session_state["df_filtrat"].empty:
                genereaza_insighturi(st.session_state["df_filtrat"])
            else:
                st.info("Afișează întâi datele filtrate pentru a vedea evoluția notelor.")


with col2:
    if "df_filtrat" in st.session_state and not st.session_state["df_filtrat"].empty:
        csv_data = st.session_state["df_filtrat"].to_csv(index=False)
        st.download_button(
            label="📥 Exportă datele filtrate (CSV)",
            data=csv_data,
            file_name='filtered_survey_data.csv',
            mime='text/csv'
        )
    else:
        st.warning("Nu există date filtrate pentru export.")

def boxplot_note(df):
    st.subheader("📊 Distribuția notelor înainte și după curs (normalizate la 10)")

    for col in ['grade_before', 'max_grade_before', 'grade_after', 'max_grade_after']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['grade_before', 'max_grade_before', 'grade_after', 'max_grade_after'])

    df['nota_inainte_10'] = (df['grade_before'] / df['max_grade_before'].replace(0, np.nan)) * 10
    df['nota_dupa_10'] = (df['grade_after'] / df['max_grade_after'].replace(0, np.nan)) * 10

    df = df[(df['nota_inainte_10'].between(0, 10)) & (df['nota_dupa_10'].between(0, 10))]
    df_long = pd.melt(
        df[['nota_inainte_10', 'nota_dupa_10']],
        var_name='Moment',
        value_name='Notă'
    )
    df_long['Moment'] = df_long['Moment'].replace({
        'nota_inainte_10': 'Înainte de curs',
        'nota_dupa_10': 'După curs'
    })

    fig = px.box(
        df_long,
        x='Moment',
        y='Notă',
        color='Moment',
        points='all',  # arată și punctele
        title='Distribuția notelor înainte și după curs',
        labels={'Notă': 'Notă (din 10)'}
    )
    fig.update_layout(showlegend=False, yaxis=dict(range=[0, 10]))

    st.plotly_chart(fig, use_container_width=True)


selected_sex_grade = selected_sex or ["Toate"]
selected_education_grade = selected_education or ["Toate"]
selected_country_grade = selected_country or ["Toate"]
selected_platform_grade = selected_platform or ["Toate"]
selected_courses_grade = selected_courses or ["Toate"]
selected_reasons_grade = ["Toate"]

st.markdown("---")
if st.checkbox("📈 Vreau să văd evoluția notelor înainte și după curs (normalizate la 10)"):
    df_grafic = filtreaza_toate_datele(
    df,
    selected_sex_grade, 
    selected_education_grade, 
    selected_country_grade,
    selected_platform_grade, 
    selected_courses_grade,
    selected_reasons_grade
    )

    if not df_grafic.empty:
        boxplot_note(df_grafic)
    else:
        st.info("Nu există suficiente date pentru a genera graficul de evoluție.")



# def afiseaza_wordcloud_specific_course(df):
#     st.subheader("🧠 Cuvintele cele mai frecvente în răspunsurile deschise")
#     text_raw = ' '.join(df['specific_course'].dropna().astype(str).tolist())

#     stopwords = set(STOPWORDS)
#     stopwords.update([
#         "și", "sau", "de", "la", "cu", "pentru", "pe", "în", "din", "care",
#         "a", "este", "fi", "ce", "că", "un", "o", "mai", "nu", "au", "am", "sunt"
#     ])

#     wordcloud = WordCloud(
#         width=800,
#         height=400,
#         background_color='white',
#         stopwords=stopwords,
#         colormap='viridis',
#         max_words=100,
#         prefer_horizontal=1.0,
#         contour_color='black',
#         contour_width=0.3
#     ).generate(text_raw)

# fig, ax = plt.subplots(figsize=(10, 5))
# ax.imshow(wordcloud, interpolation='bilinear')
# ax.axis('off')
# st.pyplot(fig)

def grafic_tehnologii_ai_vr(df):
    st.subheader("🧠 Percepția respondenților față de AI, VR și învățarea imersivă")

    coloane = {
        "Utilizare VR în educație": "vr_usage",
        "Interacțiune live cu profesorul": "live_interaction",
        "Învățare imersivă": "immersive_learning",
        "Înlocuirea educației clasice": "replacement",
        "Asistent AI în învățare": "ai_assistant",
        "Profesor AI în viitor": "ai_professor"
    }

    df_tech = df[list(coloane.values())].copy()
    df_tech = df_tech.apply(lambda col: col.str.strip().str.upper())

    data_long = pd.melt(
        df_tech,
        var_name='Întrebare',
        value_name='Răspuns'
    )

    data_long['Întrebare'] = data_long['Întrebare'].replace({v: k for k, v in coloane.items()})
    data_long = data_long[data_long['Răspuns'].isin(["DA", "NU"])]  # doar DA / NU

    if data_long.empty:
        st.info("Nu există suficiente răspunsuri DA/NU pentru a genera graficul.")
        return

    fig = px.histogram(
        data_long,
        x='Întrebare',
        color='Răspuns',
        barmode='group',
        text_auto=True,
        category_orders={'Întrebare': list(coloane.keys())},
        labels={"Întrebare": "Întrebări despre AI/VR", "count": "Număr răspunsuri"},
        title="Răspunsurile respondenților la întrebările despre AI, VR și educația viitorului"
    )

    fig.update_layout(xaxis_tickangle=25)
    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
if st.checkbox("🧠 Vreau să văd percepția respondenților despre AI, VR și învățarea imersivă"):
    df_grafic = filtreaza_toate_datele(
    df,
    selected_sex_grade, 
    selected_education_grade, 
    selected_country_grade,
    selected_platform_grade, 
    selected_courses_grade,
    selected_reasons_grade
    )
    if not df_grafic.empty:
        grafic_tehnologii_ai_vr(df_grafic)
    else:
        st.info("Nu există suficiente date filtrate pentru acest grafic.")






