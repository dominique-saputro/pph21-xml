import streamlit as st
import pandas as pd
from lxml import etree
import calendar
import datetime
import os
from streamlit_gsheets import GSheetsConnection
import calc_pph as pph

# functions
def check_inputs(*data):
    npwp = data[0]
    file = data[7]

    if not len(npwp) == 16:
        st.error("NPWP harus 16-digit.")
        return False
    if not file and filetype == 'Excel':
        st.error("File Excel belum diupload.")
        return False
    if not file and filetype == 'Google Sheet':
        st.error("Link Google Sheet kosong.")
        return False
    return True

def create_bp_bulk_xml(tin, data_list, bp_type, filename):
    NSMAP = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    if bp_type == 'bpmp':
        root_label = 'MmPayrollBulk'
        list_label = 'ListOfMmPayroll'
        entry_label = 'MmPayroll'
    else:
        root_label = 'Bp21Bulk'
        list_label = 'ListOfBp21'
        entry_label = 'Bp21'
        
    # Root element with namespace and schema
    root = etree.Element(
        root_label,
        nsmap=NSMAP,
        attrib={
            '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'schema.xsd'
        }
    )
    
    # Add TIN
    tin_el = etree.SubElement(root, 'TIN')
    tin_el.text = tin

    # List of Bp21
    list_of_bp = etree.SubElement(root, list_label)

    for entry in data_list:
        bp = etree.SubElement(list_of_bp, entry_label)

        for tag, value in entry.items():
            el = etree.SubElement(bp, tag)
            el.text = str(value)

    # Convert to XML string
    tree = etree.ElementTree(root)
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def create_bp_excel(entries, filename):
    needed = ['nik', 'nitku', 'nama', 'ptkp', 'gross', 'tarif', 'pajak']
    entries['pajak'] = round(entries['tarif'] * entries['gross'],0)
    existing_cols = [col for col in needed if col in entries.columns]
    df = entries[existing_cols]
    df = pd.DataFrame(df)
    df.to_excel(filename, index=False) 
    st.dataframe(df)

# set session placeholders
today = datetime.datetime.now()
if today.day < 25:
    month = today.month -1
else:
    month = today.month
year = today.year

# form contents
st.title('Convert Excel to XML - PPh21')
npwp = st.text_input('NPWP (16 Digit)',max_chars=16)
if npwp:
    nitku_var = (str(npwp)+"000000",str(npwp)+"000001",str(npwp)+"000002",str(npwp)+"000003")
    nitku = st.selectbox('NITKU Pemotong',nitku_var)
col1,col2 = st.columns(2)
with col1:
    masa = st.number_input('Masa Pajak',value=month, format="%d")
with col2:
    tahun = st.number_input('Tahun Pajak',value=year, format="%d")
gross = {'Gross Up': True, 'Non Gross':False}[
    st.radio('Perhitungan',['Gross Up','Non Gross'],horizontal=True)
]
tahunan = {'Bulanan':False,'Tahunan':True}[
    st.radio('Jenis',['Bulanan','Tahunan'],horizontal=True)
]
bupot_value = {'Pegawai Tetap (BPMP)': 'bpmp', 'Selain Pegawai Tetap (BP21)': 'bp21'}[
    st.radio('Bukti Potong', ['Pegawai Tetap (BPMP)', 'Selain Pegawai Tetap (BP21)'], horizontal=True)
]
filetype = st.segmented_control(
            "Data",
            options=['Excel','Google Sheet'],
            selection_mode="single",
        )
if filetype:
    match filetype:
        case 'Excel':
            file = st.file_uploader('Excel File', type=['xlsx','xls','csv'])
        case 'Google Sheet':
            file = st.text_input('Google Sheet Link')

if st.button('Run'):
    # Only process data if form is submitted and inputs are non-empty
    if check_inputs(npwp,nitku,masa,tahun,gross,tahunan,bupot_value,file):
        # Extract data from File
        match filetype:
            case 'Excel':
                # Read selected sheet
                xls = pd.ExcelFile(file)
                sheet_names = xls.sheet_names
                df = pd.read_excel(file,sheet_name=sheet_names[0])
            case 'Google Sheet':
                # Create a connection to Google Sheet
                conn = st.connection("gsheets", type=GSheetsConnection)
                df = conn.read(spreadsheet=file,ttl=0)
        # Normalize data headers
        if len(df.columns) == 6:
            with_nitku = True
            df.columns=['nik','nitku','nama','ptkp','x','gaji']
        else:
            with_nitku = False
            df.columns=['nik','nama','ptkp','x','gaji']
            df['nitku']= df.iloc[:, 0].apply(lambda x: str(x)+"000000")
        df[['status','n']]= df['ptkp'].str.split('/',expand=True)
        
        # st.header('Before Calc')
        # st.dataframe(df)
        
        # Prepare common variables
        if npwp == '0010001519052000':
            cert = 'DTP'
        else:
            cert = 'N/A'
        eod = datetime.datetime(tahun, masa, calendar.monthrange(year, month)[1])
        eod = eod.strftime('%Y-%m-%d')
        filename_xml = bupot_value + '_' + datetime.datetime(tahun,masa,15).strftime('%Y%m')+ '_' + str(npwp) + '.xml'
        if gross:
            filename_excel = 'grossup_' + datetime.datetime(tahun,masa,15).strftime('%Y%m')+ '_' + str(npwp) + '.xlsx'
        else:
            filename_excel = 'nongross_' + datetime.datetime(tahun,masa,15).strftime('%Y%m')+ '_' + str(npwp) + '.xlsx'
        # Calculate taxes
        tarif_list = []
        gross_list = []
        for index,row in df.iterrows():
            gaji = int(row['gaji'])
            status = str(row['status']).lower()
            n = int(row['n'])

            bracket_table = pph.find_ter(status, n)
            tax_rate = pph.calc_tarif(gaji, bracket_table)

            if gross:
                new_tarif, grossup_income = pph.calc_grossup(gaji, tax_rate, bracket_table)
                tarif_list.append(new_tarif)
                gross_list.append(grossup_income)
            else:
                tarif_list.append(tax_rate)
                gross_list.append(gaji)
        df['tarif'] = tarif_list
        df['gross'] = gross_list
        
        # st.header('After Calc')
        # st.dataframe(df)
        
        # Create BP21 / BPMP Data
        bp_list = []
        if bupot_value == 'bpmp':
            for index,row in df.iterrows():
                if cert == 'DTP' and row['gaji'] > 8000000:
                    cert = 'N/A'
                bpmp_item = { 
                                'TaxPeriodMonth': masa,
                                'TaxPeriodYear': tahun,
                                'CounterpartOpt': 'Resident',
                                'CounterpartPassport': None,
                                'CounterpartTin': row['nik'],
                                'StatusTaxExemption': row['ptkp'],
                                'Position': 'Karyawan',
                                'TaxCertificate': cert,
                                'TaxObjectCode': '21-100-01',
                                'Gross': row['gross'],
                                'Rate': row['tarif'],
                                'IDPlaceOfBusinessActivity': nitku,
                                'WithholdingDate': eod
                            }
                bp_list.append(bpmp_item)
        else:
            for index,row in df.iterrows():
                if cert == 'DTP' and row['gaji'] > 8000000:
                    cert = 'N/A'
                bp21_item = { 
                                'TaxPeriodMonth': masa,
                                'TaxPeriodYear': tahun,
                                'CounterpartTin': row['nik'],
                                'IDPlaceOfBusinessActivityOfIncomeRecipient': row['nitku'],
                                'StatusTaxExemption': row['ptkp'],
                                'TaxCertificate': cert,
                                'TaxObjectCode': '21-100-35',
                                'Gross': row['gross'],
                                'Deemed': 100,
                                'Rate': row['tarif'],
                                'Document': 'PaymentProof',
                                'DocumentNumber': 'Bukti Pembayaran',
                                'DocumentDate': eod,
                                'IDPlaceOfBusinessActivity': nitku,
                                'WithholdingDate': eod
                            }
                bp_list.append(bp21_item)

        # Create data exports
        create_bp_bulk_xml(npwp, bp_list,bupot_value, 'temp/' + filename_xml)
        create_bp_excel(df, 'temp/' + filename_excel)

        # Download Buttons
        col1,col2 = st.columns(2)
        with col1:
            with open('temp/' + filename_xml, "rb") as f:
                st.download_button("📄 Download XML", f, filename_xml, mime="application/xml")
        with col2:
            with open('temp/' + filename_excel, "rb") as f:
                st.download_button("📊 Download XLSX", f, filename_excel, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error('Oops! Something went wrong 😵‍💫')

    # Delete created XML and Excel files
    del_path = 'temp/'
    for filename in os.listdir(del_path):
        file_path = os.path.join(del_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
