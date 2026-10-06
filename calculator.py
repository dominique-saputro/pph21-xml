import streamlit as st
import utils.calc_pph as pph
import utils.calc_tahunan as a1

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "Mei",
    6: "Jun",
    7: "Jul",
    8: "Agu",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Des",
}
ptkp_map = {
    "TK/0" : 54000000,
    "TK/1" : 58500000,
    "TK/2" : 63000000,
    "TK/3" : 67500000,
    "K/0" : 58500000,
    "K/1" : 63000000,
    "K/2" : 67500000,
    "K/3" : 72000000,
}

#### FORM
st.title('Kalkulator TER PPh21')

col1,col2 = st.columns(2)
with col1:
    tahunan = {'Bulanan':False,'Tahunan':True}[
        st.radio('Jenis',['Bulanan','Tahunan'],horizontal=True)
    ]
with col2:
    gross = {'Gross Up': True, 'Non Gross':False}[
        st.radio('Perhitungan',['Gross Up','Non Gross'],horizontal=True)
    ]

gaji = st.number_input(label='Penghasilan (12 Bulan jika Tahunan)',placeholder=0,step=1,format='%.d')
ptkp = st.selectbox(label='Status PTKP',options=['TK/0','TK/1','TK/2','TK/3','K/0','K/1','K/2','K/3'])

if tahunan:
    masa_awal, masa_akhir = st.select_slider(
        "Masa Pajak",
        options=list(months.keys()),
        value=(1, 12),
        format_func=lambda x: months[x],
    )
    
    plus,minus = st.columns(2)
    with plus:
        st.write("Penambah")
        # masa_awal = st.number_input(label='Masa Pajak Awal',placeholder=1,step=1,min_value=1,max_value=12,format='%.d')
        
        tunj_pph = st.number_input(label='Tunjangan PPh',placeholder=0,step=1,format='%.d')
        extra1 = st.number_input(label='Tunjangan Lainnya / Lembur',placeholder=0,step=1,format='%.d')
        extra2 = st.number_input(label='Honorarium',placeholder=0,step=1,format='%.d')
        extra3 = st.number_input(label='Asuransi',placeholder=0,step=1,format='%.d')
        extra4 = st.number_input(label='Natura',placeholder=0,step=1,format='%.d')
        extra5 = st.number_input(label='Tantiem, Bonus, Gratifikasi, THR',placeholder=0,step=1,format='%.d')
    with minus:
        st.write("Pengurang")
        # masa_akhir = st.number_input(label='Masa Pajak Awal',placeholder=12,step=1,min_value=1,max_value=12,format='%.d')
        # st.number_input(label='Biaya Jabatan',value=jabatan,format='%.d',disabled=True)
        
        minus1 = st.number_input(label='Iuran Pensiun atau Biaya THT/JHT',placeholder=0,step=1,format='%.d')
        minus2 = st.number_input(label='Zakat',placeholder=0,step=1,format='%.d')
        

#### RUN
if st.button('Hitung'):
    status,n = ptkp.split('/')
    
    ### DO TAHUNAN
    if tahunan:
        bruto = gaji+tunj_pph+extra1+extra2+extra3+extra4+extra5
        masa_n = masa_akhir - masa_awal + 1
        jabatan = min(bruto * 0.05,500_000 * masa_n)
        netto = bruto - minus1 - minus2 - jabatan
        ptkp_num = ptkp_map[ptkp]
        pkp_raw = max(netto - ptkp_num,0)
        pkp = (pkp_raw // 1000) * 1000
        pph_tahunan,tax_rate = a1.calc_ng_one(pkp)
        
        if gross:
            tunj_gross = 0
            while pph_tahunan != tunj_gross:
                tunj_gross = pph_tahunan
                bruto = gaji+tunj_gross+extra1+extra2+extra3+extra4+extra5
                jabatan = min(bruto * 0.05,500_000 * masa_n)
                netto = bruto - minus1 - minus2 - jabatan
                pkp_raw = max(netto - ptkp_num,0)
                pkp = (pkp_raw // 1000) * 1000
                pph_tahunan,tax_rate = a1.calc_ng_one(pkp)

        if pph_tahunan == 0:
            bruto = gaji+extra1+extra2+extra3+extra4+extra5
            jabatan = min(bruto * 0.05,500_000 * masa_n)
            
        st.write('Tahunan')     
        with st.container(height=350):
            x1,x2 = st.columns(2)
            with x1:
                st.write("Penghasilan Bruto (Gaji + Penambah)")
                st.write("Biaya Jabatan")
                st.write("Penghasilan Netto (Bruto - Jabatan - Pengurang)")
                st.write("PTKP")
                st.write("PKP")
                st.write(f"Pajak Tahunan {tax_rate*100}%")
                st.write("Estimasi Bayar")
            with x2:
                st.write(f": {bruto:,.0f}")
                st.write(f": {jabatan:,.0f}")
                st.write(f": {netto:,.0f}")
                st.write(f": {ptkp_num:,.0f}")
                if (pkp < 0):
                    st.write(": 0")
                else:
                    st.write(f": {pkp:,.0f}")
                st.write(f": {pph_tahunan:,.0f}")
                if (pph_tahunan > 0):
                    st.write(f": {(pph_tahunan-tunj_pph):,.0f}")
                else:
                    st.write(f": {(tunj_pph*-1):,.0f}")
        
        
    ### DO BULANAN
    else:
        gol_ter = pph.get_table(status.lower(),int(n))
        bracket_table = pph.find_ter(status.lower(),int(n))
        tax_rate = pph.calc_tarif(gaji, bracket_table)

        if gross:
            new_tarif, grossup_income = pph.calc_grossup(gaji, tax_rate, bracket_table)
            tax_rate = new_tarif
            out_income = grossup_income
        else:
            out_income = gaji
        st.write('Bulanan')
        
        with st.container(height=200):
            x1,x2 = st.columns(2)
            with x1:
                st.write("Penghasilan")
                st.write("Perhitungan Pajak")
                st.write("Pajak")
            with x2:
                st.write(f": {out_income:,.0f}")
                st.write(f": TER {gol_ter} - Tarif {tax_rate*100}%")
                st.write(f": {round(out_income*tax_rate,0):,.0f}")