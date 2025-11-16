# ==========================================================
# PARTE 2 — FUNÇÕES E PREPARAÇÃO DO DATAFRAME
# ==========================================================

from utils.data_loader import load_excel_data   # ✔ IMPORT CORRIGIDO

# LOAD DATA
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado ou vazio.")
    st.stop()

# PREPARAÇÃO DO DATAFRAME
df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan', 'None', '<NA>'], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

df = df[(df["Job Family"] != "") & (df["Job Profile"] != "") & (df["Global Grade"] != "")]


# ==========================================================
# CORES DISCRETAS POR CAMINHO (OPÇÃO 2)
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p:
        return "#4F5D75"      # management
    if "professional" in p:
        return "#2F2F2F"      # professional
    if "tech" in p or "support" in p:
        return "#7C7C7C"      # technical
    return "#5F6C7A"          # project (default)


# ==========================================================
# FILTROS MINIMALISTAS
# ==========================================================
families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", families)
path_filter = colB.selectbox("Career Path", paths)

df_filtered = df.copy()   # ✔ Consistência de nome

if fam_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == fam_filter]

if path_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path_filter]


# ==========================================================
# FUNÇÃO PRINCIPAL DO MAPA — CORRIGIDA
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df):

    families_order = sorted(df["Job Family"].unique())
    grades = sorted(
        df["Global Grade"].unique(),
        key=lambda x: int(x) if str(x).isdigit() else 999,
        reverse=True
    )

    # --- MAPA DE SUBFAMÍLIAS ---
    submap = {}
    col_index = 2
    header_spans = {}

    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        header_spans[fam] = len(subs)
        for s in subs:
            submap[(fam, s)] = col_index
            col_index += 1

    # --- AGRUPAMENTO DOS CARDS ---
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # --- MERGE VERTICAL ---
    content_map = {}
    span_map = {}
    skip_set = set()

    for g in grades:
        for (fam, sf), c_idx in submap.items():
            rec = cards.get((fam, sf, g), [])
            if rec:
                content_map[(g, c_idx)] = "|".join(
                    sorted(set(f"{r['Job Profile']}{r['Career Path']}" for r in rec))
                )
            else:
                content_map[(g, c_idx)] = None

    for (fam, sf), c_idx in submap.items():
        for i, g in enumerate(grades):

            if (g, c_idx) in skip_set:
                continue

            current_sig = content_map[(g, c_idx)]

            if current_sig is None:
                span_map[(g, c_idx)] = 1
                continue

            span = 1
            for next_g in grades[i+1:]:
                if content_map[(next_g, c_idx)] == current_sig:
                    span += 1
                    skip_set.add((next_g, c_idx))
                else:
                    break

            span_map[(g, c_idx)] = span

    # ======================================================
    # CONSTRUÇÃO DO HTML
    # ======================================================
    html = []
    html.append("<div class='map-wrapper'><div class='jobmap-grid'>")

    # HEADER GG
    html.append(
        "<div class='gg-header' style='grid-column:1; grid-row:1 / span 2; width:160px;'>GG</div>"
    )

    # HEADER FAMÍLIAS
    col = 2
    for fam in families_order:
        span = header_spans[fam]
        html.append(
            f"<div class='header-family' style='grid-row:1; grid-column:{col} / span {span};'>{fam}</div>"
        )
        col += span

    # HEADER SUBFAMÍLIAS
    for (fam, sf), c_idx in submap.items():
        html.append(
            f"<div class='header-subfamily' style='grid-row:2; grid-column:{c_idx};'>{sf}</div>"
        )

    # LINHAS DO MAPA
    row_idx = 3
    for g in grades:

        # GG LABEL
        html.append(
            f"<div class='gg-cell' style='grid-row:{row_idx}; grid-column:1;'>GG {g}</div>"
        )

        for (fam, sf), c_idx in submap.items():

            if (g, c_idx) in skip_set:
                continue

            span = span_map.get((g, c_idx), 1)
            row_span = (
                f"grid-row:{row_idx} / span {span};"
                if span > 1 else f"grid-row:{row_idx};"
            )

            records = cards.get((fam, sf, g), [])
            cards_html = ""

            for rec in records:
                color = get_path_color(rec["Career Path"])
                cards_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rec['Job Profile']}</b>"
                    f"<span>{rec['Career Path']}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; {row_span}'>{cards_html}</div>"
            )

        row_idx += 1

    html.append("</div></div>")
    return "".join(html)
