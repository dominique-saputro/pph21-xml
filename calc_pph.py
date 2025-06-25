import streamlit as st

# TER Table
gol_a = [
    [0, 5400000, 0.0000],
    [5400001, 5650000, 0.0025],
    [5650001, 5950000, 0.0050],
    [5950001, 6300000, 0.0075],
    [6300001, 6750000, 0.0100],
    [6750001, 7500000, 0.0125],
    [7500001, 8550000, 0.0150],
    [8550001, 9650000, 0.0175],
    [9650001, 10050000, 0.0200],
    [10050001, 10350000, 0.0225],
    [10350001, 10700000, 0.0250],
    [10700001, 11050000, 0.0300],
    [11050001, 11600000, 0.0350],
    [11600001, 12500000, 0.0400],
    [12500001, 13750000, 0.0500],
    [13750001, 15100000, 0.0600],
    [15100001, 16950000, 0.0700],
    [16950001, 19750000, 0.0800],
    [19750001, 24150000, 0.0900],
    [24150001, 26450000, 0.1000],
    [26450001, 28000000, 0.1100],
    [28000001, 30050000, 0.1200],
    [30050001, 32400000, 0.1300],
    [32400001, 35400000, 0.1400],
    [35400001, 39100000, 0.1500],
    [39100001, 43850000, 0.1600],
    [43850001, 47800000, 0.1700],
    [47800001, 51400000, 0.1800],
    [51400001, 56300000, 0.1900],
    [56300001, 62200000, 0.2000],
    [62200001, 68600000, 0.2100],
    [68600001, 77500000, 0.2200],
    [77500001, 89000000, 0.2300],
    [89000001, 103000000, 0.2400],
    [103000001, 125000000, 0.2500],
    [125000001, 157000000, 0.2600],
    [157000001, 206000000, 0.2700],
    [206000001, 337000000, 0.2800],
    [337000001, 454000000, 0.2900],
    [454000001, 550000000, 0.3000],
    [550000001, 695000000, 0.3100],
    [695000001, 910000000, 0.3200],
    [910000001, 1400000000, 0.3300],
    [1400000001, 2147483647, 0.3400]
]

gol_b = [
    [0, 6200000, 0.0000],
    [6200001, 6500000, 0.0025],
    [6500001, 6850000, 0.0050],
    [6850001, 7300000, 0.0075],
    [7300001, 9200000, 0.0100],
    [9200001, 10750000, 0.0150],
    [10750001, 11250000, 0.0200],
    [11250001, 11600000, 0.0250],
    [11600001, 12600000, 0.0300],
    [12600001, 13600000, 0.0400],
    [13600001, 14950000, 0.0500],
    [14950001, 16400000, 0.0600],
    [16400001, 18450000, 0.0700],
    [18450001, 21850000, 0.0800],
    [21850001, 26000000, 0.0900],
    [26000001, 27700000, 0.1000],
    [27700001, 29350000, 0.1100],
    [29350001, 31450000, 0.1200],
    [31450001, 33950000, 0.1300],
    [33950001, 37100000, 0.1400],
    [37100001, 41100000, 0.1500],
    [41100001, 45800000, 0.1600],
    [45800001, 49500000, 0.1700],
    [49500001, 53800000, 0.1800],
    [53800001, 58500000, 0.1900],
    [58500001, 64000000, 0.2000],
    [64000001, 71000000, 0.2100],
    [71000001, 80000000, 0.2200],
    [80000001, 93000000, 0.2300],
    [93000001, 109000000, 0.2400],
    [109000001, 129000000, 0.2500],
    [129000001, 163000000, 0.2600],
    [163000001, 211000000, 0.2700],
    [211000001, 374000000, 0.2800],
    [374000001, 459000000, 0.2900],
    [459000001, 555000000, 0.3000],
    [555000001, 704000000, 0.3100],
    [704000001, 957000000, 0.3200],
    [957000001, 1405000000, 0.3300],
    [1405000001, 2147483647, 0.3400]
]

gol_c = [
    [0, 6600000, 0.0000],
    [6600001, 6950000, 0.0025],
    [6950001, 7350000, 0.0050],
    [7350001, 7800000, 0.0075],
    [7800001, 8850000, 0.0100],
    [8850001, 9800000, 0.0125],
    [9800001, 10950000, 0.0150],
    [10950001, 11200000, 0.0175],
    [11200001, 12050000, 0.0200],
    [12050001, 12950000, 0.0300],
    [12950001, 14150000, 0.0400],
    [14150001, 15550000, 0.0500],
    [15550001, 17050000, 0.0600],
    [17050001, 19500000, 0.0700],
    [19500001, 22700000, 0.0800],
    [22700001, 26600000, 0.0900],
    [26600001, 28100000, 0.1000],
    [28100001, 30100000, 0.1100],
    [30100001, 32600000, 0.1200],
    [32600001, 35400000, 0.1300],
    [35400001, 38900000, 0.1400],
    [38900001, 43000000, 0.1500],
    [43000001, 47400000, 0.1600],
    [47400001, 51200000, 0.1700],
    [51200001, 55800000, 0.1800],
    [55800001, 60400000, 0.1900],
    [60400001, 66700000, 0.2000],
    [66700001, 74500000, 0.2100],
    [74500001, 83200000, 0.2200],
    [83200001, 95600000, 0.2300],
    [95600001, 110000000, 0.2400],
    [110000001, 134000000, 0.2500],
    [134000001, 169000000, 0.2600],
    [169000001, 221000000, 0.2700],
    [221000001, 390000000, 0.2800],
    [390000001, 463000000, 0.2900],
    [463000001, 561000000, 0.3000],
    [561000001, 709000000, 0.3100],
    [709000001, 965000000, 0.3200],
    [965000001, 1419000000, 0.3300],
    [1419000001, 2147483647, 0.3400]
]

def calc_tarif(income, bracket_table):
    """
    Calculate the progressive tax based on the given income and tax brackets.

    Parameters:
        income (int): The income to calculate the tariff for.
        bracket_table (list): Each element is [range_bottom, range_top, rate]

    Returns:
        float: Tax rate based on the progressive system.
    """
    tax_rate = 0
    for bottom, top, rate in bracket_table:
        if income > top:
            tax_rate = rate
        elif income >= bottom:
            tax_rate = rate
            break  # Stop after applying the bracket the income falls into
        else:
            break  # Income is below this bracket, no need to continue
    return tax_rate

def find_ter(s,n):
    """
    Determines which bracket will be chosen based on the given status and n.

    Parameters:
        s (str): Martial status
        n (int): Number of dependencies

    Returns:
        list:  Each element is [range_bottom, range_top, rate]
    """
    if s == "tk":
        if n in [0, 1]:
            table = gol_a
        elif n in [2, 3]:
            table = gol_b
    else:
        if n == 0:
            table = gol_a
        elif n in [1, 2]:
            table = gol_b
        elif n == 3:
            table = gol_c
    return table

def calc_grossup(income, tarif, bracket_table):
    """
    Calculate the progressive tax based on the given income and tax brackets.

    Parameters:
        income (int): The income to calculate the tariff for.
        tarif (float): Tax rate before recalculation for gross up
        bracket_table (list): Each element is [range_bottom, range_top, rate]

    Returns:
        new_tarif (float): Tax rate based on the progressive system.
        grossup (float): Marked up income
    """
    loop = True
    new_tarif = tarif

    while loop:
        check = income * (new_tarif / (1 - new_tarif))
        new_tarif = calc_tarif(check + income, bracket_table)

        if round((check + income) * (1 - new_tarif)) == income:
            loop = False
            check = income * (new_tarif / (1 - new_tarif))
        else:
            loop = True

        if check + income > 2_147_483_647:
            loop = False
            new_tarif = 0.34
            check = income * (new_tarif / (1 - new_tarif))
            # infinite loop protection

    grossup = income + round(check,0)
    return new_tarif, grossup

    



#Viewport
# with st.form('calcForm'):
#     st.title('Pyhton ver. Calc PPh21')
#     income = st.number_input('Enter your income', min_value=0)
#     table = st.radio('TER',options=['A','B','C'],horizontal=True)
#     submit = st.form_submit_button('Calculate Tax')

# if submit:
#     match table:
#         case 'A':
#             gol = gol_a
#         case 'B':
#             gol = gol_b
#         case 'C':
#             gol = gol_c
#     tax = calc_tarif(income,gol) * income
#     st.write(f"{tax:,.0f}")



