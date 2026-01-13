import streamlit as st
import os
import pandas as pd
import numpy as np
import datetime
from lxml import etree

ptkp = {
    "TK/0" : 54000000,
    "TK/1" : 58500000,
    "TK/2" : 63000000,
    "TK/3" : 67500000,
    "K/0" : 58500000,
    "K/1" : 63000000,
    "K/2" : 67500000,
    "K/3" : 72000000,
}

def calc_ng(df):
    pph_list = []
    cap1 =   60000000
    cap2 =  250000000
    cap3 =  500000000
    cap4 = 5000000000
    
    for pkp in df['pkp']:
        if (pkp < 0):
            pph = 0
        elif (pkp <= cap1):
            pph = pkp * 0.05
        elif (pkp <= cap2):
            pph = 3000000+((pkp-cap1) * 0.15)
        elif (pkp <= cap3):
            pph = 31500000 +((pkp-cap2) * 0.25)
        elif (pkp <= cap4):
            pph = 94000000 +((pkp-cap3) * 0.3)
        elif (pkp > cap4):
            pph = 1444000000 +((pkp-cap4) * 0.35)
    
        pph_list.append(pph)
    return pph_list

def create_a1_bulk_xml(tin, data_list, filename):
    NSMAP = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    
    root_label = 'A1Bulk'
    list_label = 'ListOfA1'
    entry_label = 'A1'
        
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

    # List of A1
    list_of_bp = etree.SubElement(root, list_label)

    for entry in data_list:
        bp = etree.SubElement(list_of_bp, entry_label)

        for tag, value in entry.items():
            el = etree.SubElement(bp, tag)
            el.text = str(value)

    # Convert to XML string
    tree = etree.ElementTree(root)
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def create_a1_excel(entries, filename, gross):
    if gross:
        needed = ['masa_awal','masa_akhir','nik','ptkp','gaji','tunj_gross','penambah','bruto','jabatan','pengurang','netto','ptkp_num','pkp','pph','estimasi_bayar']
    else:
        needed = ['masa_awal','masa_akhir','nik','ptkp','gaji','tunj_pph','penambah','bruto','jabatan','pengurang','netto','ptkp_num','pkp','pph','estimasi_bayar']
    entries['estimasi_bayar'] = np.where(
        entries['pph'] > 0,
        entries['pph'] - entries['tunj_pph'],
        entries['tunj_pph'] * -1
    )
    entries['pkp'] = np.where(
        entries['pkp'] < 0,
        0,
        entries['pkp']
    )
    existing_cols = [col for col in needed if col in entries.columns]
    df = entries[existing_cols]
    df = pd.DataFrame(df)
    df.to_excel(filename, index=False) 
    st.dataframe(df)

def do_tahunan(npwp,nitku,gross,df):
    # Prepare common variables
    today = datetime.datetime.now()
    year = today.year - 1
    eod = str(year) + '-12-31'
    if npwp == '0010001519052000':
        cert = 'DTP'
    else:
        cert = 'N/A'
    filename_xml = 'a1_' + str(npwp) + '.xml'
    filename_excel = 'a1_' + str(npwp) + '.xlsx'
        
    # Normalize data headers
    df.columns=['masa_awal','masa_akhir','nik','ptkp','gaji','tunj_pph','extra1','extra2','extra3','extra4','extra5','minus1','minus2']
    to_num = ['masa_awal','masa_akhir','gaji','tunj_pph','extra1','extra2','extra3','extra4','extra5','minus1','minus2']
    
    df[to_num] = (
        df[to_num]
        .replace({',': ''}, regex=True)   
        .apply(pd.to_numeric, errors='coerce')
    )
    
    bruto_cols = ['gaji','tunj_pph','extra1','extra2','extra3','extra4','extra5']
    df['bruto'] = df[bruto_cols].sum(axis=1)   
    penambah_cols = ['extra1','extra2','extra3','extra4','extra5']
    df['penambah'] = df[penambah_cols].sum(axis=1) 
    
    df['masa_n'] = df['masa_akhir'] - df['masa_awal'] + 1

    df['jabatan'] = np.minimum(
        df['bruto'] * 0.05,
        500_000 * df['masa_n']
    )

    df['netto'] = df['bruto'] - df['minus1'] - df['minus2'] - df['jabatan']
    df['pengurang'] = (df['minus1'] + df['minus2']) * -1
    df['ptkp_num'] = df['ptkp'].map(ptkp)
    pkp_raw = (df['netto'] - df['ptkp_num']).clip(lower=0)
    df['pkp'] = (pkp_raw // 1000) * 1000
    
    #Calculate Taxes
    df['pph'] = calc_ng(df) 
    if gross:
        df['tunj_gross'] = 0
        while not df['pph'].equals(df['tunj_gross']):
            df['tunj_gross'] = df['pph']      
            bruto_cols = ['gaji','tunj_gross','extra1','extra2','extra3','extra4','extra5']
            df['bruto'] = df[bruto_cols].sum(axis=1)   
            df['jabatan'] = np.minimum(
                df['bruto'] * 0.05,
                500_000 * df['masa_n']
            )
            df['netto'] = df['bruto'] - df['minus1'] - df['minus2'] - df['jabatan']
            pkp_raw = (df['netto'] - df['ptkp_num']).clip(lower=0)
            df['pkp'] = (pkp_raw // 1000) * 1000
            df['pph'] = calc_ng(df)
                
    #Create A1 Bupot data
    a1_list = []
    for index,row in df.iterrows():
        # --------------------------------- What is the DTP limit for tahunan???
        if cert == 'DTP' and row['gaji'] > 130000000:
            cert = 'N/A'
        if row['masa_awal'] == 1 and row['masa_akhir'] == 12:
            status = 'FullYear'
            masa_n = 0
        else:
            status = 'PartialYear'
            masa_n = 0
            
        a1_item = {
                    'WorkForSecondEmployer': 'No',
                    'TaxPeriodMonthStart': row['masa_awal'],
                    'TaxPeriodMonthEnd': row['masa_akhir'],
                    'TaxPeriodYear': year,
                    'CounterpartOpt': 'Resident',
                    'CounterpartPassport': '',
                    'CounterpartTin': row['nik'],
                    'TaxExemptOpt': row['ptkp'],
                    'StatusOfWithholding': status,
                    'CounterpartPosition': 'STAFF',
                    'TaxObjectCode': '21-100-01',
                    'NumberOfMonths': masa_n,
                    'SalaryPensionJhtTht': row['gaji'],
                    'GrossUpOpt': 'Yes' if gross else 'No',
                    'IncomeTaxBenefit': row['tunj_pph'],
                    'OtherBenefit': row['extra1'],
                    'Honorarium': row['extra2'],
                    'InsurancePaidByEmployer': row['extra3'],
                    'Natura': row['extra4'],
                    'TantiemBonusThr': row['extra5'],
                    'PensionContributionJhtThtFee': row['minus1'],
                    'Zakat': row['minus2'],
                    'PrevWhTaxSlip': '',
                    'TaxCertificate': cert,
                    'Article21IncomeTax': '0',
                    'IDPlaceOfBusinessActivity': nitku,
                    'WithholdingDate': eod
                    }
        a1_list.append(a1_item)
    
    
    # Create data exports
    os.makedirs('temp', exist_ok=True)
    create_a1_bulk_xml(npwp, a1_list, 'temp/' + filename_xml)
    create_a1_excel(df, 'temp/' + filename_excel,gross)

    # Download Buttons
    col1,col2 = st.columns(2)
    with col1:
        with open('temp/' + filename_xml, "rb") as f:
            st.download_button("📄 Download XML", f, filename_xml, mime="application/xml")
    with col2:
        with open('temp/' + filename_excel, "rb") as f:
            st.download_button("📊 Download XLSX", f, filename_excel, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    