# Importing our libraries
import pandas as pd  # Data manipulation
import numpy as np   # Numerical operations
import matplotlib.pyplot as plt  # Data visualization
import plotly.express as px
import streamlit as st # streamlit


# load data
df = pd.read_csv('resource/ObservationData_lavlqce.csv')
# cleaning column names
df.columns = df.columns.str.replace("  ", " ")
#
df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year



# load data

# trend
economic_trend = [
        "Year",
        "Real per Capita GDP Growth Rate (annual %)",
        "Real GDP growth (annual %)",
        "Gross domestic product, (constant prices US$)",
        "Gross domestic product, current prices (current US$)",
        "Final consumption expenditure (current US$)",
        "Gross capital formation (current US$)",
        "Exports of goods and services (current US$)",
        "Imports of goods and services (current US$)",
        "Final consumption expenditure (% of GDP)",
        "Gross capital formation (% of GDP)",
        "Exports of goods and services (% of GDP)",
        "Imports of goods and services (% of GDP)",
        "Inflation, consumer prices (annual %)"
    ]

trend_df = df.loc[:,economic_trend]
trend_df.dropna(inplace=True)

# comparative
comparative_trend = [
        'Year',
        'Country',
        'Central government, Fiscal Balance (Current US $)',
        'Central government, Fiscal Balance (% of GDP)',
        'Central government, total revenue and grants (Current US $)',
        'Central government, total revenue and grants (% of GDP)',
        'Central government, total expenditure and net lending (Current US $)',
        'Central government, total expenditure and net lending (% of GDP)',
        'General government final consumption expenditure (current US$)',
        'Household final consumption expenditure (current US$)',
        'Final consumption expenditure (% of GDP)',
        'General government final consumption expenditure (% of GDP)',
        'Household final consumption expenditure (% of GDP)',
        'Current account balance (Net, BoP, cur. US$)',
        'Current account balance (As % of GDP)',
        'Gross capital formation, Private sector (current US$)',
        'Gross capital formation, Private sector (% GDP)'
    ]

comparative_df = df.loc[:, comparative_trend]
# clean Nan value
comparative_df.dropna(inplace=True)

# sector of comparative

economic_categories = {
    "Fiscal Balances": [
        "Central government, Fiscal Balance (Current US $)",
        "Central government, Fiscal Balance (% of GDP)",
        "Central government, total revenue and grants (Current US $)",
        "Central government, total revenue and grants (% of GDP)",
        "Central government, total expenditure and net lending (Current US $)",
        "Central government, total expenditure and net lending (% of GDP)"
    ],
    "Government Finances": [
        "General government final consumption expenditure (current US$)",
        "Household final consumption expenditure (current US$)",
        "Final consumption expenditure (% of GDP)",
        "General government final consumption expenditure (% of GDP)",
        "Household final consumption expenditure (% of GDP)"
    ],
    "Current Account Balances": [
        "Current account balance (Net, BoP, cur. US$)",
        "Current account balance (As % of GDP)"
    ],
    "Government Spending": [
        "General government final consumption expenditure (current US$)",
        "Central government, total expenditure and net lending (Current US $)",
        "General government final consumption expenditure (% of GDP)",
        "Central government, total expenditure and net lending (% of GDP)"
    ],
    "Household Consumption": [
        "Household final consumption expenditure (current US$)",
        "Household final consumption expenditure (% of GDP)"
    ],
    "Private Sector Investment": [
        "Gross capital formation, Private sector (current US$)",
        "Gross capital formation, Private sector (% GDP)"
    ]
}

# sectoral
sectoral_columns = [
    'Year',
    'Country',
    'General government final consumption expenditure (current US$)',
    'Central government, total expenditure and net lending (Current US $)',
    'General government final consumption expenditure (% of GDP)',
    'Central government, total expenditure and net lending (% of GDP)',
    'Household final consumption expenditure (current US$)',
    'Household final consumption expenditure (% of GDP)',
    'Gross capital formation, Private sector (current US$)',
    'Gross capital formation, Private sector (% GDP)'
]

sectoral_df = df[sectoral_columns]
sectoral_df.dropna(inplace=True)

sectoral_categories = {
    "Government Spending": [
        "General government final consumption expenditure (current US$)",
        "Central government, total expenditure and net lending (Current US $)",
        "General government final consumption expenditure (% of GDP)",
        "Central government, total expenditure and net lending (% of GDP)"
    ],
    "Household Consumption": [
        "Household final consumption expenditure (current US$)",
        "Household final consumption expenditure (% of GDP)"
    ],
    "Private Sector Investment": [
        "Gross capital formation, Private sector (current US$)",
        "Gross capital formation, Private sector (% GDP)"
    ]
}

# extract necessary columns

# build app


#st.line_chart(data=df)

# analysis

analysis_type = [
'Trend analysis','Comparative analysis'
]

analysis_sidebar = st.sidebar.selectbox('Select analysis',(analysis_type))

#

if analysis_sidebar == 'Trend analysis':

    # trend analysis

    # select country
    country = st.sidebar.selectbox('Country', df['Country'].unique())
   
    # plot
    def trend_analysis(country):

        country_df = trend_df[df['Country'] == country]

        return country_df

    # filtered country dataset
    country_dataset = trend_analysis(country)


    corr_checker = st.sidebar.toggle('Check correlation')
    # select country
    if corr_checker:

        # correlation
        df1 = country_dataset.select_dtypes(include=['number'])

        corr_matrix = df1.corr()

        st.dataframe(corr_matrix)

    else:
        # select trend to check
        trend_type = st.sidebar.selectbox('Select Economic parameter',(country_dataset.columns[1:]))
        # title
        st.title(f'{trend_type} of {country}')

        # line plot
        fig = px.line(country_dataset, x='Year', y=trend_type, markers=True)
        st.plotly_chart(fig)

        # bar plot
        fig = px.bar(country_dataset, x='Year', y=trend_type, text_auto='.2s')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig)


elif analysis_sidebar == 'Comparative analysis':
    # select countries
    multiple_countries = st.multiselect('Countries', df['Country'].unique(),placeholder='Select multiple countries',default='Nigeria',)
    st.divider()

    comparative_sector = st.sidebar.selectbox('Sector', [i for i in economic_categories])

    # select sector type
    if comparative_sector:
        econ_parameter = st.sidebar.selectbox('Select Economic parameter', economic_categories[comparative_sector])
    
    st.write(f'Trend of {econ_parameter} of {", ".join(x.upper() for x in multiple_countries)}')

    def comparative_analysis(*country):
        country_df = comparative_df.loc[df['Country'].isin(*country)]

        return country_df

    country_df = comparative_analysis(multiple_countries)

    # plot
    fig = px.line(country_df, x='Year', y=econ_parameter, color=country_df['Country'], markers=True)

    st.plotly_chart(fig)
    
    st.divider()
    # comparing columns against each other
    comp_country = st.selectbox('Countries', df['Country'].unique(),placeholder='Select country')
    comp_df = comparative_df.loc[df['Country'] == comp_country]
 
    col1,col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox('Select X-axis', economic_categories[comparative_sector])
        st.write(x_axis)
    with col2:
        y_axis = st.selectbox('Select Y-axis', economic_categories[comparative_sector])
        st.write(y_axis)

    st.divider()

    fig = px.scatter(comp_df, x=x_axis, y=y_axis)
    st.plotly_chart(fig)


#### support

with st.sidebar:
    st.divider()
    st.markdown('''
    
    
    🌟  If you've enjoyed my work and would like to support me, 
    consider buying me a coffee!    
    Your generosity keeps me inspired and fuels my creativity. 
    Thank you for being a part of my journey. ☕️💫
    ''')

    st.markdown('[Support me on Ko-fi](https://ko-fi.com/onscript)')

    st.divider()