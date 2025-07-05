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

df['country_standard'] = df['country'].replace(country_standard)
    

df['educatie_standard'] = df['education'].replace(educatie_standard)
df['gender_standard'] = df['gender'].replace(gender_standard)
df['country_standard'] = df['country'].replace(country_standard)
df['platform_standard'] = df['selected_platforms'].replace(platform_standard).str.split(',').apply(lambda lst: [x.strip() for x in lst] if isinstance(lst, list) else [])
df['course_standard'] = df['selected_courses'].replace(couses_standard).str.split(',').apply(lambda lst: [x.strip() for x in lst] if isinstance(lst, list) else [])
df['reasons_standard'] = df['selected_usage'].replace(reasons_standard).str.split(',').apply(lambda lst: [x.strip() for x in lst] if isinstance(lst, list) else [])

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
    disabled_opts = [opt != "Toate" and "Toate" in current for opt in options]
    
    new_selection = st.multiselect(label, options=options, default=current, key=key, disabled=disabled_opts)

    if "Toate" in new_selection and len(new_selection) > 1:
        st.session_state[key] = ["Toate"]
        st.rerun()

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
        filtru_platform = pd.Series(True, index=df.index)
    else:
        filtru_platform = df['platform_standard'].apply(lambda x: any(p in x for p in platform_sel))

    if "Toate" in courses_sel:
        filtru_courses = pd.Series(True, index=df.index)
    else:
        filtru_courses = df['courses_standard'].apply(lambda x: any(c in x for c in courses_sel))

    if "Toate" in reasons_sel:
        filtru_reasons = pd.Series(True, index=df.index)
    else:
        filtru_reasons = df['reasons_standard'].apply(lambda x: any(r in x for r in reasons_sel))

    return df[filtru_platform & filtru_courses & filtru_reasons]

if not df.empty:
    # col_filters, col_table = st.columns([1, 3])   
    
    
    if demografics_data:
        col_filters_sex, col_filters_education, col_filters_country = st.columns(3)
        with col_filters_sex: 
            selected_sex = st.multiselect("Genul:", options=gender_options, default=["Toate"])
        with col_filters_education:
            selected_education = st.multiselect("Nivelul de educație:", options=education_options, default=["Toate"])
        with col_filters_country:
            selected_country = st.multiselect("țara:", options=country_options, default=["Toate"])

    else:
        selected_sex = ["Toate"]
        selected_education = ["Toate"]
        selected_country = ["Toate"]

    if elearning_data:
        col_filters_platform, col_filters_courses, col_filters_reasons, col_filters_others = st.columns(4)
        with col_filters_platform:
            selected_platform = st.multiselect("platforma de e-learning:", options=platform_options, default=["Toate"])
        with col_filters_courses:
            selected_courses = st.multiselect("Tipul cursurilor:", options=course_options, default=["Toate"])
        with col_filters_reasons:
            selected_reasons = st.multiselect("motivele pentru e-learning:", options=reasons_options, default=["Toate"])
        with col_filters_others:
            pass
    else:
        selected_platform = ["Toate"]
        selected_courses = ["Toate"]
        selected_reasons = ["Toate"]

Button = st.button("Afișează datele filtrate")
if Button:
    st.subheader("Date filtrate")

    filtered_df = filtreaza_date_demografics(df, selected_sex, selected_education, selected_country)

    filtered_df_1 = filtreaza_date_elearning(filtered_df, selected_platform, selected_courses, selected_reasons)

    if not filtered_df.empty:

        if demografics_data:
            st.markdown("### 📊 Date demografice")

            # Gen
            st.write("#### Distribuția pe genuri")
            gender_counts = filtered_df['gender_standard'].value_counts()
            st.bar_chart(gender_counts)

            # Educație
            st.write("#### Distribuția pe nivel de educație")
            education_counts = filtered_df['educatie_standard'].value_counts()
            st.bar_chart(education_counts)

            # Țară
            st.write("#### Distribuția pe țări")
            country_counts = filtered_df['country_standard'].value_counts().head(10)
            st.bar_chart(country_counts)

            st.write("#### Distribuția pe vârste")
            fig_age = px.histogram(
                    filtered_df, x='age', nbins=20,
                    labels={'age': 'Vârstă', 'count': 'Număr respondenți'},
                    # title='Distribuția vârstelor în funcție de filtre'
                )
            st.plotly_chart(fig_age, use_container_width=True)


        # if elearning_data and not filtered_df_1.empty:
        #     st.markdown("### 💻 Date despre e-learning")

        #     # Platforme
        #     st.write("#### Platforme folosite")
        #     platform_counts = filtered_df_1['platform_standard'].explode().value_counts()
        #     st.bar_chart(platform_counts)

        #     # Cursuri
        #     st.write("#### Tipuri de cursuri urmate")
        #     course_counts = filtered_df_1['course_standard'].explode().value_counts().head(10)
        #     st.bar_chart(course_counts)

        #     # Motive
        #     st.write("#### Motive pentru care folosesc e-learning")
        #     reason_counts = filtered_df_1['reasons_standard'].explode().value_counts().head(10)
        #     st.bar_chart(reason_counts)

        if elearning_data and not filtered_df_1.empty:
            st.markdown("### 💻 Date despre e-learning")

            # Platforme
            st.write("#### Platforme folosite")
            platform_counts = filtered_df_1['platform_standard'].explode().value_counts()
            st.bar_chart(platform_counts)

            # Cursuri - bar chart grupat pe sexe
            st.write("#### Tipuri de cursuri urmate (distribuție pe sexe)")
            df_courses = filtered_df_1.explode('course_standard')
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
                title='Cursuri urmarite pentru nivelul de educatie: Master'
            )
            fig_courses.update_layout(xaxis_title='Tip curs', yaxis_title='Număr respondenți', xaxis_tickangle=45)
            st.plotly_chart(fig_courses, use_container_width=True)

            # Motive
            st.write("#### Motive pentru care folosesc e-learning")
            reason_counts = filtered_df_1['reasons_standard'].explode().value_counts().head(10)
            st.bar_chart(reason_counts)


    else:
        st.warning("Nu există date pentru selecția curentă.")


