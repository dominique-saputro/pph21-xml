import pandas as pd
from lxml import etree

import utils.calc_tahunan as a1


def test_cert_is_per_employee(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    npwp = '0010001519052000'
    df = pd.DataFrame([
        [1, 12, '1111', 'TK/0', 150000000, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 12, '2222', 'TK/0', 60000000, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    a1.do_tahunan(npwp, '0' * 22, False, df, 12, 2025)

    root = etree.parse(str(tmp_path / 'temp' / ('a1_' + npwp + '.xml')))
    assert root.xpath('//A1/TaxCertificate/text()') == ['N/A', 'DTP']
