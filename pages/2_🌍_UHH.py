# Libraries
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Dashboard Nerwillis',
                   page_icon=':bar_chart:', layout='wide')
st.title('🌍 UHH (2018 - 2021)')

# ===== Setting =====
hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ===== Use Column in excel =====
excel_file = 'Neraca.xlsx'
sheet_name = 'UHH'

# Perbaiki penggunaan usecols untuk mengambil kolom A hingga E
df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:E',  # Ubah menjadi A:E sesuai struktur file Excel
                   header=0)

df_multi = pd.read_excel(excel_file,
                         sheet_name=sheet_name,
                         usecols='A:E',
                         header=0)

df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols='A:B')
df_participants.dropna(inplace=True)

# ===== Dropdown in Sidebar =====
option = st.sidebar.selectbox(
    'Filter',
    ('All', 'Provinsi'))

if(option == 'All'):
    provinsi = df_multi['Kabupaten/Kota'].unique()
    provinsi_selection = st.multiselect('Provinsi:',
                                        provinsi,
                                        default=provinsi)

    if len(provinsi_selection) <= 1:  # Ganti kondisi ini untuk memungkinkan 1 pilihan
        st.warning('Pilih 2 Provinsi atau lebih untuk membandingkan.')

    else:
        if(provinsi_selection):
            filter_provinsi_df = df_multi[df_multi['Kabupaten/Kota'].isin(
                provinsi_selection)]
            c1, c2 = st.columns(2)

            with c1:
                st.bar_chart(filter_provinsi_df, x='Kabupaten/Kota', y=['Tahun 2018', 'Tahun 2020'])
            with c2:
                st.bar_chart(filter_provinsi_df, x='Kabupaten/Kota', y=['Tahun 2019', 'Tahun 2021'])

elif(option == 'Provinsi'):
    provinsi = df['Kabupaten/Kota'].unique().tolist()
    provinsi_selection = st.selectbox('Pilih Provinsi : ', provinsi)
    m1, m2, m3 = st.columns((1, 1, 1))
    todf = pd.read_excel(excel_file, sheet_name='UHH')
    to = todf[(todf['Kabupaten/Kota'] == provinsi_selection)]

    deltaResult = float(to['Tahun 2021']) - float(to['Tahun 2020'])
    format_float = "{:,.2f}".format(deltaResult)
    deltaFormat = format_float + "%"

    tigaTahun = df["Tahun 2021"].mean()
    formatTigaTahun = "{:,.2f}".format(tigaTahun)

    m1.metric(label='Tahun 2021', value=float(
        to['Tahun 2021'].map('{:,.2f}'.format)), delta=deltaFormat)
    m2.metric(label='Rata-Rata 4 Tahun Terakhir',
              value=float(to['Rata2'].map('{:,.2f}'.format)))
    m3.metric(label='Rata-Rata UHH di seluruh Kota/Kabupaten 2021',
              value=formatTigaTahun)

    yearList = []
    for i in range(2018, 2022):
        yearList.append(i)

    single_row_df = to[0:1]
    listValuesUHH = []
    list_from_df = single_row_df.values.tolist()[0]
    for i in range(1, 5):
        listValuesUHH.append(list_from_df[i])

    provinsi_UHH = pd.DataFrame({
        'UHH': listValuesUHH
    }, index=yearList)

    st.line_chart(provinsi_UHH,  y='UHH', use_container_width=True)
