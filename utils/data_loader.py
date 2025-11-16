# utils/data_loader.py
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

# Mapeamento dos arquivos da pasta data/
DATA_FILES = {
    "career_bands_levels": "Career Bands & Levels.xlsx",
    "gi_position_descriptions": "GI Position Descriptions.xlsx",
    "job_family": "Job Family.xlsx",
    "job_profile": "Job Profile.xlsx",
    "level_structure": "Level Structure.xlsx",
    "qualifications": "Qualifications.xlsx",
}


def load_excel_data(data_dir: Path | None = None) -> dict:
    """
    Carrega os arquivos .xlsx configurados em DATA_FILES a partir da pasta `data`
    e devolve um dicionário: { chave: DataFrame }.

    - Ignora silenciosamente arquivos que não existirem.
    - Permite passar um data_dir customizado, mas por padrão usa <raiz>/data.
    """
    if data_dir is None:
        data_dir = Path(__file__).parents[1] / "data"

    data = {}
    for key, filename in DATA_FILES.items():
        path = data_dir / filename
        if path.exists():
            data[key] = pd.read_excel(path)

    return data
