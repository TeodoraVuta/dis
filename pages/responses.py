import streamlit as st
from db_utils import get_connection, close_connection
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from country_list import countries_for_language
from db_utils import show_logged_in_user

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


def afiseaza_date_elearning(filtered_df):
    st.markdown("### 💻 Date despre e-learning")

    # Platforme
    st.write("#### Platforme folosite")
    df_platforms = filtered_df.explode('platform_standard')
    platform_counts = df_platforms['platform_standard'].value_counts()
    st.bar_chart(platform_counts)

    # Cursuri grupate pe sexe
    st.write("#### Tipuri de cursuri urmate (distribuție pe sexe)")
    df_courses = filtered_df.explode('course_standard')
    df_courses = df_courses.dropna(subset=['course_standard', 'gender_standard']).copy()
    df_courses = df_courses[df_courses['course_standard'] != '']

    course_sex_counts = df_courses.groupby(['course_standard', 'gender_standard']).size().reset_index(name='count')
    top_courses = df_courses['course_standard'].value_counts().index.tolist()
    course_sex_counts = course_sex_counts[course_sex_counts['course_standard'].isin(top_courses)]

    fig_courses = px.bar(
        course_sex_counts,
        x='course_standard',
        y='count',
        color='gender_standard',
        barmode='group',
        labels={'course_standard': 'Tip curs', 'count': 'Număr respondenți'},
        title='Cursuri urmarite în funcție de gen'
    )
    fig_courses.update_layout(xaxis_title='Tip curs', yaxis_title='Număr respondenți', xaxis_tickangle=45)
    st.plotly_chart(fig_courses, use_container_width=True)

    # Motive
    st.write("#### Motive pentru care folosesc e-learning")
    df_reasons = filtered_df.explode('reasons_standard')
    reason_counts = df_reasons['reasons_standard'].value_counts().head(10)
    st.bar_chart(reason_counts)


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

    # Filtrare e-learning
    if "Toate" not in platform_sel:
        df_filtered = df_filtered[df_filtered['platform_standard'].apply(lambda lst: any(x in lst for x in platform_sel))]
    if "Toate" not in courses_sel:
        df_filtered = df_filtered[df_filtered['course_standard'].apply(lambda lst: any(x in lst for x in courses_sel))]
    if "Toate" not in reasons_sel:
        df_filtered = df_filtered[df_filtered['reasons_standard'].apply(lambda lst: any(x in lst for x in reasons_sel))]

    return df_filtered


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


def afiseaza_date_elearning(df):
    st.markdown("### 💻 Date despre e-learning")

    # Platforme
    st.write("#### Platforme folosite")
    st.bar_chart(pd.Series([item for sublist in df['platform_standard'] for item in sublist]).value_counts())

    # Cursuri pe gen
    st.write("#### Tipuri de cursuri urmate (distribuție pe sexe)")
    exploded = df.explode('course_standard')
    exploded = exploded.dropna(subset=['course_standard', 'gender_standard'])
    counts = exploded.groupby(['course_standard', 'gender_standard']).size().reset_index(name='count')
    top_courses = exploded['course_standard'].value_counts().head(10).index
    counts = counts[counts['course_standard'].isin(top_courses)]

    fig = px.bar(counts, x='course_standard', y='count', color='gender_standard', barmode='group')
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Motive
    st.write("#### Motive pentru care folosesc e-learning")
    st.bar_chart(pd.Series([item for sublist in df['reasons_standard'] for item in sublist]).value_counts().head(10))


# 🔘 Interfață de rulare
if st.button("Afișează datele filtrate"):
    st.subheader("Date filtrate")

    # fallback dacă nu e selectat nimic
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
        # age_range = (min, max) dacă vrei și slider pe vârstă
    )

    if not df_filtrat.empty:
        if demografics_data:
            afiseaza_date_demografice(df_filtrat)
        if elearning_data:
            afiseaza_date_elearning(df_filtrat)
    else:
        st.warning("Nu există date pentru selecția curentă.")