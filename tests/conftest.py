import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

st = MagicMock()
st.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
sys.modules['streamlit'] = st
