import base64
from pathlib import Path
from typing import Dict, List

import pandas as pd
import streamlit as st


@st.cache_data
def load_profiles(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path).fillna("")
    needed = ["Job Family", "Sub Job Family", "Job Profile", "Global Grade", "Role Description"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        st.error(f"Colunas ausentes no Job Profile.xlsx: {', '.join(missing)}")
        return pd.DataFrame(columns=needed)
    return df


@st.cache_data
def list_ppts(ppts_dir: Path) -> List[Path]:
    return sorted(ppts_dir.glob("*.pptx"))


def match_ppts(ppt_paths: List[Path], job_family: str, sub_family: str, job_profile: str) -> List[Path]:
    targets = [job_profile.lower(), sub_family.lower(), job_family.lower()]
    matched = []
    for ppt in ppt_paths:
        name = ppt.stem.lower()
        if any(t and t in name for t in targets):
            matched.append(ppt)
    return matched


def fmt_title(text: str) -> str:
    return text.strip() if text else "—"


def render_card(profile: Dict, attachments: List[Path]) -> None:
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e0ddd6; border-radius:10px; padding:14px; background:#ffffff; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                <div style="font-size:18px; font-weight:700; margin-bottom:4px;">{fmt_title(profile['Job Profile'])}</div>
                <div style="color:#555; margin-bottom:8px;">{fmt_title(profile['Sub Job Family'])} · {fmt_title(profile['Job Family'])}</div>
                <div style="font-size:13px; color:#777; margin-bottom:6px;">Global Grade: {fmt_title(str(profile.get('Global Grade', '—')))}</div>
                <div style="font-size:14px; line-height:1.4; color:#222; margin-bottom:10px;">
                    {fmt_title(profile.get('Role Description', '')[:280]) + ('...' if len(profile.get('Role Description', '')) > 280 else '')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if attachments:
            cols = st.columns(len(attachments))
            for idx, ppt in enumerate(attachments):
                with ppt.open("rb") as f:
                    data = f.read()
                cols[idx].download_button(
                    label=f"Baixar PPT",
                    data=data,
                    file_name=ppt.name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key=f"dl-{ppt.name}-{idx}",
                )


def main():
    st.set_page_config(page_title="Career Path Explorer", layout="wide")

    data_path = Path("data") / "Job Profile.xlsx"
    ppts_dir = Path("ppts")
    df = load_profiles(data_path)
    ppt_paths = list_ppts(ppts_dir)

    st.title("Career Path Explorer")
    st.markdown(
        "Navegue pelas job families, subáreas e cargos e acesse os infográficos (PPT) sem precisar abrir a intranet."
    )

    if df.empty:
        st.stop()

    families = sorted(df["Job Family"].dropna().unique().tolist())
    sel_family = st.selectbox("Job Family", families)
    sub_df = df[df["Job Family"] == sel_family]
    sub_options = ["All"] + sorted(sub_df["Sub Job Family"].dropna().unique().tolist())
    sel_sub = st.selectbox("Sub Job Family", sub_options)

    if sel_sub != "All":
        sub_df = sub_df[sub_df["Sub Job Family"] == sel_sub]

    profiles = sub_df.to_dict(orient="records")

    if not profiles:
        st.info("Nenhum cargo encontrado para essa seleção.")
        return

    cols = st.columns(3)
    for idx, prof in enumerate(profiles):
        attachments = match_ppts(ppt_paths, prof["Job Family"], prof["Sub Job Family"], prof["Job Profile"])
        with cols[idx % 3]:
            render_card(prof, attachments)


if __name__ == "__main__":
    main()
