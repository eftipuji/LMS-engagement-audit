"""
LMS Berbasis Engagement Audit — Streamlit App
Prototipe deteksi dini Quiet Quitting untuk SMP/SMK
Kerangka: Student Engagement Audit (4 Modul + EWS AI)
Dibuat oleh: Tim Universitas Pekalongan
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LMS Engagement Audit",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}

/* ── Sidebar: TERANG ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 2px solid #E8ECF4;
}
[data-testid="stSidebar"] * {
    color: #1E2761 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #1E2761 !important;
    font-weight: 500;
    font-size: 14px;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div {
    color: #4A5568 !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1.5px solid #E8ECF4;
    border-radius: 14px;
    padding: 16px 20px !important;
    box-shadow: 0 2px 10px rgba(30,39,97,0.07);
}
div[data-testid="metric-container"] label {
    color: #6B7694 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 900 !important;
    color: #1E2761 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F0F3FA;
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #6B7694;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1E2761 !important;
    color: #FFFFFF !important;
    font-weight: 700;
}

/* ── Buttons ── */
.stButton > button {
    background: #1E2761;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 24px;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #F5A623;
    color: #1E2761;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #2EC47F;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

/* ── Custom cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1.5px solid #E8ECF4;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(30,39,97,0.06);
}
.alert-kritis {
    background: rgba(229,83,83,0.08);
    border: 1px solid rgba(229,83,83,0.35);
    border-left: 4px solid #E55353;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.alert-tinggi {
    background: rgba(245,166,35,0.08);
    border: 1px solid rgba(245,166,35,0.35);
    border-left: 4px solid #F5A623;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.badge-kritis { background:#E5535318; color:#E55353; border:1px solid #E5535350; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-tinggi { background:#F5A62318; color:#C47D0A; border:1px solid #F5A62350; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-sedang { background:#F5C84218; color:#A07A05; border:1px solid #F5C84250; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-rendah { background:#2EC47F18; color:#1A8A58; border:1px solid #2EC47F50; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }

/* ── Footer ── */
.footer-box {
    background: #1E2761;
    border-radius: 12px;
    padding: 14px 20px;
    text-align: center;
    margin-top: 8px;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; border: 1px solid #E8ECF4; }

/* ── Form inputs ── */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    border-radius: 8px !important;
    border: 1.5px solid #E8ECF4 !important;
}
.stSlider [data-testid="stSlider"] { accent-color: #1E2761; }
</style>
""", unsafe_allow_html=True)

# ─── WARNA & HELPERS ──────────────────────────────────────────────────────────
COLORS = {"KRITIS": "#E55353", "TINGGI": "#F5A623", "SEDANG": "#F5C842", "RENDAH": "#2EC47F"}

def risk_color(r):
    return COLORS.get(r, "#6B7694")

def bar_h(value, max_val=100, color="#1E2761"):
    pct = int((value / max_val) * 100)
    return f"""
    <div style="margin-bottom:4px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
        <span style="font-size:12px;color:#6B7694;"></span>
        <span style="font-size:13px;font-weight:700;color:{color};">{value}</span>
      </div>
      <div style="background:#EEF1F8;border-radius:99px;height:8px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:99px;"></div>
      </div>
    </div>"""

def gauge_chart(value, title, color="#1E2761", max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#1E2761", "size": 13}},
        number={"font": {"color": color, "size": 28}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#E8ECF4",
                     "tickfont": {"color": "#6B7694"}},
            "bar": {"color": color},
            "bgcolor": "#F8F9FE",
            "bordercolor": "#E8ECF4",
            "steps": [
                {"range": [0, max_val * 0.4], "color": "#EEF1F8"},
                {"range": [max_val * 0.4, max_val * 0.7], "color": "#E4E8F4"},
                {"range": [max_val * 0.7, max_val], "color": "#D8DDEF"},
            ],
        }
    ))
    fig.update_layout(
        height=200, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font={"color": "#1E2761"}
    )
    return fig

PLOT_LAYOUT = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F8F9FE",
    font={"color": "#1E2761"},
    margin=dict(t=30, b=20, l=20, r=20),
)

# ── Gradient warna untuk tabel TANPA matplotlib ──
# (pandas Styler.background_gradient() butuh matplotlib sebagai dependency
#  opsional; di Streamlit Cloud kadang tidak terpasang sehingga memicu
#  ImportError. Fungsi di bawah meniru gradient RdYlGn / RdYlGn_r secara
#  manual, jadi tidak butuh matplotlib sama sekali.)
def _gradient_color(val, vmin, vmax, reverse=False):
    if pd.isna(val):
        return ""
    if vmax == vmin:
        norm = 0.5
    else:
        norm = (val - vmin) / (vmax - vmin)
    norm = max(0.0, min(1.0, norm))
    if reverse:
        norm = 1 - norm
    # interpolasi merah(low) -> kuning(mid) -> hijau(high)
    if norm < 0.5:
        r, g, b = 255, int(255 * (norm * 2)), 0
    else:
        r, g, b = int(255 * (1 - (norm - 0.5) * 2)), 255, 0
    return f"background-color: rgba({r},{g},{b},0.75); color:#1E2761;"

def make_gradient_styler(reverse=False):
    """Pengganti drop-in untuk .style.background_gradient(subset=[...], cmap='RdYlGn'[_r])"""
    def _style_func(s):
        vmin, vmax = s.min(), s.max()
        return [_gradient_color(v, vmin, vmax, reverse) for v in s]
    return _style_func

# ── Helper kompatibilitas rerun ──
# st.rerun() baru ada sejak Streamlit 1.27. Di versi lebih lama (atau
# environment Streamlit Cloud yang belum ter-update) atributnya tidak ada
# sama sekali, sehingga memicu AttributeError tepat saat tombol Simpan/Hapus
# di menu Kualitas Guru ditekan. Fungsi ini mencoba semua nama yang pernah
# dipakai Streamlit, dari yang terbaru ke yang paling lama.
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("⚠️ Versi Streamlit Anda tidak mendukung auto-refresh. Silakan muat ulang halaman secara manual.")

# ── Helper warna rgba dari hex (pengganti trik 'hex + alpha' yang tidak
#    didukung konsisten di semua versi Plotly) ──
def hex_to_rgba(hex_color, alpha=0.16):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Helper cast aman ke int (menghindari ValueError jika nilai NaN/None/string) ──
def safe_int(val, default=0):
    try:
        if pd.isna(val):
            return default
        return int(val)
    except (TypeError, ValueError):
        return default

# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    students = pd.DataFrame([
        {"id": 1,  "Nama": "Andi Pratama",   "Kelas": "VIII-A", "Burnout": 72, "Kognitif": 68, "Fairness": 55, "Engagement": 42, "Risiko": "TINGGI",  "Status": "Quiet Quitting",  "Login_mnt": 12, "Tugas_selesai": 55},
        {"id": 2,  "Nama": "Budi Santoso",   "Kelas": "VIII-A", "Burnout": 34, "Kognitif": 45, "Fairness": 80, "Engagement": 78, "Risiko": "RENDAH",  "Status": "Aktif",           "Login_mnt": 48, "Tugas_selesai": 92},
        {"id": 3,  "Nama": "Citra Dewi",     "Kelas": "VIII-B", "Burnout": 61, "Kognitif": 72, "Fairness": 60, "Engagement": 58, "Risiko": "SEDANG",  "Status": "Beban Kognitif",  "Login_mnt": 22, "Tugas_selesai": 68},
        {"id": 4,  "Nama": "Deni Raharjo",   "Kelas": "VIII-B", "Burnout": 88, "Kognitif": 55, "Fairness": 40, "Engagement": 29, "Risiko": "KRITIS",  "Status": "Exhausted",       "Login_mnt": 7,  "Tugas_selesai": 31},
        {"id": 5,  "Nama": "Eka Putri",      "Kelas": "VIII-A", "Burnout": 45, "Kognitif": 38, "Fairness": 75, "Engagement": 71, "Risiko": "RENDAH",  "Status": "Aktif",           "Login_mnt": 55, "Tugas_selesai": 89},
        {"id": 6,  "Nama": "Fajar Nugroho",  "Kelas": "VIII-C", "Burnout": 77, "Kognitif": 80, "Fairness": 50, "Engagement": 35, "Risiko": "TINGGI",  "Status": "Quiet Quitting",  "Login_mnt": 9,  "Tugas_selesai": 42},
        {"id": 7,  "Nama": "Gita Sari",      "Kelas": "VIII-C", "Burnout": 50, "Kognitif": 60, "Fairness": 65, "Engagement": 62, "Risiko": "SEDANG",  "Status": "Monitor",         "Login_mnt": 33, "Tugas_selesai": 74},
        {"id": 8,  "Nama": "Hendra Wijaya",  "Kelas": "VIII-B", "Burnout": 92, "Kognitif": 88, "Fairness": 35, "Engagement": 18, "Risiko": "KRITIS",  "Status": "Krisis",          "Login_mnt": 4,  "Tugas_selesai": 20},
        {"id": 9,  "Nama": "Indah Lestari",  "Kelas": "VIII-C", "Burnout": 40, "Kognitif": 42, "Fairness": 78, "Engagement": 74, "Risiko": "RENDAH",  "Status": "Aktif",           "Login_mnt": 51, "Tugas_selesai": 88},
        {"id": 10, "Nama": "Joko Saputra",   "Kelas": "VIII-A", "Burnout": 65, "Kognitif": 70, "Fairness": 52, "Engagement": 47, "Risiko": "SEDANG",  "Status": "Monitor",         "Login_mnt": 18, "Tugas_selesai": 60},
    ])

    burnout_trend = pd.DataFrame([
        {"Minggu": "Mgg 1", "Rata-rata": 38, "VIII-A": 32, "VIII-B": 40, "VIII-C": 42},
        {"Minggu": "Mgg 2", "Rata-rata": 42, "VIII-A": 36, "VIII-B": 45, "VIII-C": 45},
        {"Minggu": "Mgg 3", "Rata-rata": 51, "VIII-A": 44, "VIII-B": 55, "VIII-C": 54},
        {"Minggu": "Mgg 4", "Rata-rata": 58, "VIII-A": 50, "VIII-B": 63, "VIII-C": 61},
        {"Minggu": "Mgg 5", "Rata-rata": 61, "VIII-A": 54, "VIII-B": 67, "VIII-C": 62},
        {"Minggu": "Mgg 6", "Rata-rata": 67, "VIII-A": 60, "VIII-B": 72, "VIII-C": 69},
    ])

    teachers = pd.DataFrame([
        {"Nama": "Bu Ratna",  "Mapel": "Matematika", "Respons_jam": 28, "Umpan_balik": 82, "Konsistensi": 91, "Konseling": 3,  "Indeks": 84},
        {"Nama": "Pak Iman",  "Mapel": "IPA",         "Respons_jam": 45, "Umpan_balik": 60, "Konsistensi": 72, "Konseling": 8,  "Indeks": 62},
        {"Nama": "Bu Sinta",  "Mapel": "B. Indonesia","Respons_jam": 18, "Umpan_balik": 91, "Konsistensi": 95, "Konseling": 1,  "Indeks": 91},
        {"Nama": "Pak Doni",  "Mapel": "IPS",         "Respons_jam": 62, "Umpan_balik": 44, "Konsistensi": 58, "Konseling": 15, "Indeks": 45},
    ])

    return students, burnout_trend, teachers


df, df_trend, df_teacher = load_data()

# Inisialisasi data guru di session state agar bisa diupdate
if "df_teacher" not in st.session_state:
    st.session_state.df_teacher = df_teacher.copy()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 16px;'>
        <div style='color:#1E2761;font-weight:900;font-size:18px;letter-spacing:0.5px;'>⚡ LMS ENGAGEMENT</div>
        <div style='color:#6B7694;font-size:12px;margin-top:2px;'>Audit Psikologis Real-Time</div>
        <hr style='border-color:#E8ECF4;margin-top:14px;'>
    </div>
    """, unsafe_allow_html=True)

    halaman = st.radio("Navigasi", [
        "🏠  Dashboard Utama",
        "🔥  Burnout Detection",
        "🧠  Cognitive Load Monitor",
        "👩‍🏫  Kualitas Guru",
        "⚖️  Fairness Perception",
        "🤖  Early Warning AI",
        "📋  Pulse Survey",
        "📊  Laporan & Ekspor",
    ])

    st.markdown("<hr style='border-color:#E8ECF4;'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#6B7694;font-size:11px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Filter Global</div>", unsafe_allow_html=True)
    kelas_filter  = st.multiselect("Kelas",        ["VIII-A", "VIII-B", "VIII-C"],              default=["VIII-A", "VIII-B", "VIII-C"])
    risiko_filter = st.multiselect("Level Risiko", ["KRITIS", "TINGGI", "SEDANG", "RENDAH"],    default=["KRITIS", "TINGGI", "SEDANG", "RENDAH"])

    st.markdown("<hr style='border-color:#E8ECF4;'>", unsafe_allow_html=True)

    # ── Info sekolah ──
    st.markdown("""
    <div style='text-align:center;padding:4px 0 8px;'>
        <div style='color:#1E2761;font-weight:700;font-size:13px;'>SMP Negeri 2 Kota Pekalongan</div>
        <div style='color:#6B7694;font-size:11px;margin-top:2px;'>Tahun Ajaran 2024/2025</div>
        <div style='color:#2EC47F;font-size:11px;margin-top:4px;'>● Sistem Aktif</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#1E2761;border-radius:10px;padding:12px 14px;text-align:center;margin-top:12px;'>
        <div style='color:#FFFFFF;font-size:11px;font-weight:700;letter-spacing:0.5px;'>
            🎓 Tim Universitas Pekalongan
        </div>
        <div style='color:#CADCFC;font-size:10px;margin-top:3px;'>
            FKIP · Pendidikan Matematika
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ─────────────────────────────────────────────────────────────
df_filtered = df[df["Kelas"].isin(kelas_filter) & df["Risiko"].isin(risiko_filter)]


# ════════════════════════════════════════════════════════════
# H A L A M A N  1 : DASHBOARD UTAMA
# ════════════════════════════════════════════════════════════
if halaman == "🏠  Dashboard Utama":
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <h1 style='color:#1E2761;font-size:26px;font-weight:900;margin:0 0 4px;'>
            Dashboard Engagement Audit
        </h1>
        <p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>
            Sistem deteksi dini <em>Quiet Quitting</em> — integrasi data LMS, Dapodik &amp; sosial-ekonomi
        </p>""", unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"<div style='text-align:right;color:#6B7694;font-size:12px;padding-top:28px;'>{datetime.now().strftime('%d %b %Y, %H:%M')}</div>", unsafe_allow_html=True)

    kritis     = len(df[df["Risiko"] == "KRITIS"])
    tinggi     = len(df[df["Risiko"] == "TINGGI"])
    avg_eng    = int(df["Engagement"].mean())
    avg_burnout = int(df["Burnout"].mean())

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🔴 Siswa Kritis",    kritis,           delta="+1 dari minggu lalu", delta_color="inverse")
    with c2: st.metric("⚠️ Risiko Tinggi",   tinggi,           delta="+2 dari minggu lalu", delta_color="inverse")
    with c3: st.metric("📊 Avg Engagement",  f"{avg_eng}/100", delta="-8 poin",             delta_color="inverse")
    with c4: st.metric("🔥 Avg Burnout",     avg_burnout,      delta="+9 poin",             delta_color="inverse")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if kritis > 0:
        st.markdown(f"""
        <div class="alert-kritis">
            🚨 <strong style='color:#E55353;'>PERINGATAN KRITIS:</strong>
            <span style='color:#2D3748;'> {kritis} siswa KRITIS dan {tinggi} siswa TINGGI memerlukan intervensi segera.
            Cek Modul Burnout dan EWS untuk detail tindakan.</span>
        </div>""", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:4px;'>📈 Tren Burnout 6 Minggu</div>", unsafe_allow_html=True)
        fig_trend = px.line(df_trend, x="Minggu", y=["VIII-A", "VIII-B", "VIII-C", "Rata-rata"],
                            color_discrete_map={"VIII-A": "#1E2761", "VIII-B": "#F5A623",
                                                "VIII-C": "#2EC47F", "Rata-rata": "#E55353"},
                            markers=True)
        fig_trend.update_traces(selector=dict(name="Rata-rata"), line=dict(dash="dot", width=3))
        fig_trend.update_layout(**PLOT_LAYOUT, height=280,
                                legend=dict(bgcolor="#F0F3FA"),
                                xaxis=dict(gridcolor="#EEF1F8"),
                                yaxis=dict(gridcolor="#EEF1F8", range=[20, 90]))
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:4px;'>🎯 Distribusi Risiko</div>", unsafe_allow_html=True)
        risk_counts = df["Risiko"].value_counts().reset_index()
        risk_counts.columns = ["Risiko", "Jumlah"]
        fig_pie = px.pie(risk_counts, names="Risiko", values="Jumlah",
                         color="Risiko", color_discrete_map=COLORS, hole=0.55)
        fig_pie.update_traces(textfont_size=13)
        fig_pie.update_layout(**PLOT_LAYOUT, height=280, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin:12px 0 8px;'>🎯 Siswa Prioritas Intervensi</div>", unsafe_allow_html=True)
    priority = df[df["Risiko"].isin(["KRITIS", "TINGGI"])].sort_values("Engagement")
    for _, row in priority.iterrows():
        color      = risk_color(row["Risiko"])
        badge_cls  = f"badge-{row['Risiko'].lower()}"
        st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:space-between;
                    background:#FFFFFF;border:1.5px solid #E8ECF4;border-left:4px solid {color};
                    border-radius:10px;padding:14px 18px;margin-bottom:8px;
                    box-shadow:0 1px 6px rgba(30,39,97,0.06);'>
            <div>
                <div style='color:#1E2761;font-weight:700;font-size:15px;'>{row["Nama"]}</div>
                <div style='color:#6B7694;font-size:12px;'>{row["Kelas"]} · {row["Status"]}</div>
            </div>
            <div style='display:flex;align-items:center;gap:20px;'>
                <div style='text-align:center;'>
                    <div style='color:{color};font-size:24px;font-weight:900;'>{row["Engagement"]}</div>
                    <div style='color:#6B7694;font-size:10px;'>Engagement</div>
                </div>
                <div style='text-align:center;'>
                    <div style='color:#E55353;font-size:20px;font-weight:700;'>{row["Burnout"]}</div>
                    <div style='color:#6B7694;font-size:10px;'>Burnout</div>
                </div>
                <span class='{badge_cls}'>{row["Risiko"]}</span>
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# H A L A M A N  2 : BURNOUT DETECTION
# ════════════════════════════════════════════════════════════
elif halaman == "🔥  Burnout Detection":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>🔥 Modul 1: Burnout Detection Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Mengidentifikasi profil Exhausted-Disengaged 6–12 bulan sebelum siswa menyerah.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Peta Burnout", "📋 Detail Maslach", "📈 Tren per Kelas"])

    with tab1:
        fig_sc = px.scatter(df_filtered, x="Burnout", y="Engagement",
                            color="Risiko", size="Kognitif", hover_name="Nama",
                            hover_data={"Kelas": True, "Status": True, "Risiko": True},
                            color_discrete_map=COLORS, text="Nama")
        fig_sc.update_traces(textposition="top center", textfont_size=10, textfont_color="#1E2761")
        fig_sc.add_hline(y=50, line_dash="dot", line_color="#CADCFC")
        fig_sc.add_vline(x=60, line_dash="dot", line_color="#CADCFC")
        fig_sc.add_annotation(x=20, y=90, text="🟢 Aktif",              showarrow=False, font=dict(color="#2EC47F", size=12))
        fig_sc.add_annotation(x=80, y=90, text="⚠️ Burnout Tersembunyi",showarrow=False, font=dict(color="#F5A623", size=12))
        fig_sc.add_annotation(x=20, y=15, text="😐 Apatis",             showarrow=False, font=dict(color="#6B7694", size=12))
        fig_sc.add_annotation(x=80, y=15, text="🔴 Zona Kritis",        showarrow=False, font=dict(color="#E55353", size=12))
        fig_sc.update_layout(**PLOT_LAYOUT, height=400,
                             xaxis=dict(gridcolor="#EEF1F8", title="Skor Burnout"),
                             yaxis=dict(gridcolor="#EEF1F8", title="Skor Engagement"))
        st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})
        st.caption("💡 Ukuran titik = beban kognitif. Zona kanan-bawah = prioritas intervensi tertinggi.")

    with tab2:
        st.markdown("<p style='color:#6B7694;font-size:13px;'>Pilih siswa untuk melihat profil Maslach Burnout Inventory lengkap.</p>", unsafe_allow_html=True)
        opts = df_filtered["Nama"].tolist()
        if opts:
            sel = st.selectbox("Pilih Siswa", opts)
            row = df[df["Nama"] == sel].iloc[0]
            color = risk_color(row["Risiko"])
            cg1, cg2, cg3 = st.columns(3)
            with cg1: st.plotly_chart(gauge_chart(row["Burnout"], "Kelelahan Emosional", "#E55353"), use_container_width=True, config={"displayModeBar": False})
            with cg2: st.plotly_chart(gauge_chart(row["Kognitif"], "Depersonalisasi", "#F5A623"),    use_container_width=True, config={"displayModeBar": False})
            with cg3: st.plotly_chart(gauge_chart(100 - row["Fairness"], "Rendah Prestasi Diri", "#1E2761"), use_container_width=True, config={"displayModeBar": False})

            if row["Risiko"] == "KRITIS":
                rec = "🚨 Intervensi segera: konseling wajib & koordinasi wali murid. Pertimbangkan pengurangan beban tugas."
            elif row["Risiko"] == "TINGGI":
                rec = "⚠️ Pantau ketat: check-in langsung oleh wali kelas minggu ini. Pulse survey harian direkomendasikan."
            elif row["Risiko"] == "SEDANG":
                rec = "🟡 Monitor reguler: pastikan dukungan sosial memadai. Pulse survey mingguan."
            else:
                rec = "🟢 Kondisi baik: pertahankan motivasi. Beri peran positif di kelas."

            st.markdown(f"""
            <div style='background:#FFFFFF;border:1.5px solid {color}44;border-left:4px solid {color};
                        border-radius:10px;padding:16px 20px;margin-top:8px;
                        box-shadow:0 1px 6px rgba(30,39,97,0.06);'>
                <div style='font-weight:700;color:{color};margin-bottom:6px;'>
                    {row["Nama"]} — {row["Kelas"]}
                    <span style='color:#6B7694;font-weight:400;'> · {row["Status"]}</span>
                </div>
                <div style='color:#2D3748;font-size:14px;line-height:1.8;'>{rec}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Tidak ada data untuk filter yang dipilih.")

    with tab3:
        fig_box = px.box(df, x="Kelas", y="Burnout", color="Kelas",
                         color_discrete_map={"VIII-A": "#1E2761", "VIII-B": "#F5A623", "VIII-C": "#2EC47F"},
                         points="all", hover_name="Nama")
        fig_box.update_layout(**PLOT_LAYOUT, height=360, showlegend=False,
                              xaxis=dict(gridcolor="#EEF1F8"),
                              yaxis=dict(gridcolor="#EEF1F8", title="Skor Burnout"))
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})


# ════════════════════════════════════════════════════════════
# H A L A M A N  3 : COGNITIVE LOAD
# ════════════════════════════════════════════════════════════
elif halaman == "🧠  Cognitive Load Monitor":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>🧠 Modul 2: Cognitive Load Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Mendeteksi batas kerja kognitif dari pola login, durasi, dan konsistensi tugas.</p>", unsafe_allow_html=True)

    avg_login  = int(df_filtered["Login_mnt"].mean()) if len(df_filtered) else 0
    avg_tugas  = int(df_filtered["Tugas_selesai"].mean()) if len(df_filtered) else 0
    overload   = len(df_filtered[df_filtered["Kognitif"] > 70])

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("⏱ Avg Login Harian",           f"{avg_login} mnt", delta=f"{avg_login - 40} dari ideal 40 mnt", delta_color="inverse")
    with c2: st.metric("📚 Tugas Selesai Tepat Waktu",  f"{avg_tugas}%",    delta="-7% dari minggu lalu",                delta_color="inverse")
    with c3: st.metric("🧠 Siswa Overload Kognitif",    overload,           delta="Skor kognitif > 70")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])

    with col_l:
        fig_cog = px.scatter(df_filtered, x="Login_mnt", y="Kognitif",
                             color="Risiko", size="Burnout", hover_name="Nama",
                             hover_data={"Kelas": True, "Tugas_selesai": True},
                             color_discrete_map=COLORS, text="Nama")
        fig_cog.add_vline(x=40, line_dash="dot", line_color="#2EC47F",
                          annotation_text="Ideal ≥40 mnt", annotation_font_color="#2EC47F")
        fig_cog.add_hline(y=70, line_dash="dot", line_color="#E55353",
                          annotation_text="Batas Overload", annotation_font_color="#E55353")
        fig_cog.update_traces(textposition="top center", textfont_size=9, textfont_color="#1E2761")
        fig_cog.update_layout(**PLOT_LAYOUT, height=380,
                              title=dict(text="Login Harian vs Beban Kognitif"),
                              xaxis=dict(gridcolor="#EEF1F8", title="Durasi Login (mnt/hari)"),
                              yaxis=dict(gridcolor="#EEF1F8", title="Skor Beban Kognitif"))
        st.plotly_chart(fig_cog, use_container_width=True, config={"displayModeBar": False})

    with col_r:
        fig_bar = px.bar(df_filtered.sort_values("Tugas_selesai"),
                         x="Tugas_selesai", y="Nama", orientation="h",
                         color="Tugas_selesai",
                         color_continuous_scale=["#E55353", "#F5A623", "#2EC47F"],
                         range_color=[0, 100])
        fig_bar.update_layout(**PLOT_LAYOUT, height=380,
                              title=dict(text="% Tugas Dikumpul Tepat Waktu"),
                              xaxis=dict(gridcolor="#EEF1F8", range=[0, 100]),
                              yaxis=dict(gridcolor="#EEF1F8"),
                              coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:8px;'>📋 Data Lengkap Siswa</div>", unsafe_allow_html=True)
    disp = df_filtered[["Nama", "Kelas", "Kognitif", "Login_mnt", "Tugas_selesai", "Engagement", "Risiko"]].copy()
    disp.columns = ["Nama", "Kelas", "Beban Kognitif", "Login (mnt)", "Tugas (%)", "Engagement", "Risiko"]
    st.dataframe(
        disp.style
            .apply(make_gradient_styler(reverse=True),  subset=["Beban Kognitif"])  # merah=tinggi, hijau=rendah
            .apply(make_gradient_styler(reverse=False), subset=["Engagement"])      # hijau=tinggi, merah=rendah
            .apply(make_gradient_styler(reverse=False), subset=["Tugas (%)"]),      # hijau=tinggi, merah=rendah
        use_container_width=True, hide_index=True
    )


# ════════════════════════════════════════════════════════════
# H A L A M A N  4 : KUALITAS GURU  (diperbaiki + input nama)
# ════════════════════════════════════════════════════════════
elif halaman == "👩‍🏫  Kualitas Guru":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>👩‍🏫 Modul 3: Indeks Kualitas Kepemimpinan Guru</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 16px;'>Mengukur dukungan emosional relasional yang mempengaruhi 58,7% variance motivasi siswa.</p>", unsafe_allow_html=True)

    tab_guru1, tab_guru2, tab_guru3 = st.tabs(["📊 Radar Indeks", "🃏 Kartu Guru", "➕ Input / Tambah Guru"])

    # ── TAB 1: Radar ──────────────────────────────────────────
    with tab_guru1:
        df_t = st.session_state.df_teacher
        if len(df_t) == 0:
            st.info("Belum ada data guru. Tambahkan guru lewat tab '➕ Input / Tambah Guru'.")
        else:
            categories = ["Kecepatan Respons", "Umpan Balik", "Konsistensi", "Frekuensi Konseling", "Indeks Total"]
            palette    = ["#1E2761", "#F5A623", "#2EC47F", "#E55353",
                          "#9B59B6", "#00B4D8", "#E67E22", "#27AE60"]

            fig_radar = go.Figure()
            for i, (_, t) in enumerate(df_t.iterrows()):
                respons_norm  = max(0, 100 - safe_int(t["Respons_jam"]))
                konseling_norm = min(100, safe_int(t["Konseling"]) * 7)
                vals = [respons_norm, safe_int(t["Umpan_balik"]), safe_int(t["Konsistensi"]), konseling_norm, safe_int(t["Indeks"])]
                col  = palette[i % len(palette)]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=categories + [categories[0]],
                    fill="toself", name=str(t["Nama"]),
                    line_color=col, fillcolor=hex_to_rgba(col, 0.16),
                ))

            fig_radar.update_layout(
                polar=dict(
                    bgcolor="#F8F9FE",
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#E8ECF4",
                                    tickfont=dict(color="#6B7694")),
                    angularaxis=dict(gridcolor="#E8ECF4", tickfont=dict(color="#1E2761")),
                ),
                paper_bgcolor="#FFFFFF", font={"color": "#1E2761"},
                height=400, margin=dict(t=30, b=20, l=20, r=20),
                legend=dict(bgcolor="#F0F3FA", bordercolor="#E8ECF4"),
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    # ── TAB 2: Kartu Guru ─────────────────────────────────────
    with tab_guru2:
        df_t = st.session_state.df_teacher
        if len(df_t) == 0:
            st.info("Belum ada data guru. Tambahkan guru lewat tab '➕ Input / Tambah Guru'.")
        else:
            cols_card = st.columns(2)
            for idx, (_, t) in enumerate(df_t.iterrows()):
                nama_guru    = str(t["Nama"])
                mapel_guru   = str(t["Mapel"])
                indeks_val   = safe_int(t["Indeks"])
                respons_val  = safe_int(t["Respons_jam"])
                konseling_val = safe_int(t["Konseling"])
                umpan_val    = safe_int(t["Umpan_balik"])
                konsisten_val = safe_int(t["Konsistensi"])

                if indeks_val > 80:
                    ind_color = "#2EC47F"
                elif indeks_val > 60:
                    ind_color = "#1E2761"
                elif indeks_val > 45:
                    ind_color = "#F5A623"
                else:
                    ind_color = "#E55353"

                respons_ok    = respons_val < 30
                respons_color = "#2EC47F" if respons_ok else "#F5A623"
                respons_icon  = "✓" if respons_ok else "⚠️"
                konseling_color = "#E55353" if konseling_val <= 3 else "#2EC47F"

                umpan_bar    = bar_h(umpan_val,     color="#1E2761")
                konsisten_bar = bar_h(konsisten_val, color="#2EC47F")

                with cols_card[idx % 2]:
                    st.markdown(f"""
                    <div class='kpi-card'>
                      <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;'>
                        <div>
                          <div style='color:#1E2761;font-weight:800;font-size:17px;'>{nama_guru}</div>
                          <div style='color:#6B7694;font-size:12px;'>{mapel_guru}</div>
                        </div>
                        <div style='text-align:center;'>
                          <div style='font-size:34px;font-weight:900;color:{ind_color};line-height:1;'>{indeks_val}</div>
                          <div style='font-size:10px;color:#6B7694;'>Indeks Kualitas</div>
                        </div>
                      </div>
                      <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;'>
                        <div>
                          <div style='font-size:11px;color:#6B7694;'>⏱ Kecepatan Respons</div>
                          <div style='font-weight:700;color:{respons_color};'>{respons_val} jam {respons_icon}</div>
                        </div>
                        <div>
                          <div style='font-size:11px;color:#6B7694;'>💬 Sesi Konseling</div>
                          <div style='font-weight:700;color:{konseling_color};'>{konseling_val} sesi/bulan</div>
                        </div>
                      </div>
                      <div style='font-size:11px;color:#6B7694;margin-bottom:4px;'>Bobot Umpan Balik</div>
                      {umpan_bar}
                      <div style='font-size:11px;color:#6B7694;margin-bottom:4px;margin-top:8px;'>Konsistensi Penilaian</div>
                      {konsisten_bar}
                    </div>""", unsafe_allow_html=True)

    # ── TAB 3: Input Guru Baru ────────────────────────────────
    with tab_guru3:
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:4px;'>➕ Tambah / Perbarui Data Guru</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6B7694;font-size:13px;margin-bottom:16px;'>Isi formulir di bawah ini untuk menambahkan guru baru ke dalam sistem.</p>", unsafe_allow_html=True)

        with st.form("form_guru"):
            fg1, fg2 = st.columns(2)
            with fg1:
                inp_nama   = st.text_input("Nama Lengkap Guru *", placeholder="contoh: Bu Ratna", key="inp_nama_guru")
                inp_mapel  = st.text_input("Mata Pelajaran *",     placeholder="contoh: Matematika", key="inp_mapel_guru")
                inp_respons = st.number_input("Kecepatan Respons (jam)", min_value=1, max_value=168, value=24,
                                              help="Rata-rata waktu membalas pesan/tugas dalam jam", key="inp_respons_guru")
            with fg2:
                inp_umpan     = st.slider("Bobot Umpan Balik (0–100)",  0, 100, 70, key="inp_umpan_guru")
                inp_konsisten = st.slider("Konsistensi Penilaian (0–100)", 0, 100, 75, key="inp_konsisten_guru")
                inp_konseling = st.number_input("Sesi Konseling per Bulan", min_value=0, max_value=30, value=4, key="inp_konseling_guru")

            # Hitung indeks otomatis
            respons_norm_inp  = max(0, 100 - inp_respons)
            konseling_norm_inp = min(100, inp_konseling * 7)
            indeks_hitung = int(respons_norm_inp * 0.25 + inp_umpan * 0.35 + inp_konsisten * 0.25 + konseling_norm_inp * 0.15)

            st.markdown(f"""
            <div style='background:#F0F3FA;border-radius:10px;padding:12px 16px;margin:12px 0;'>
                <span style='color:#6B7694;font-size:13px;'>Indeks Kualitas yang Akan Dihitung: </span>
                <span style='color:#1E2761;font-size:20px;font-weight:900;'>{indeks_hitung}</span>
                <span style='color:#6B7694;font-size:12px;'> / 100</span>
            </div>""", unsafe_allow_html=True)

            submitted_guru = st.form_submit_button("💾 Simpan Data Guru")

        if submitted_guru:
            if not inp_nama.strip() or not inp_mapel.strip():
                st.warning("⚠️ Nama dan Mata Pelajaran wajib diisi.")
            else:
                guru_baru = {
                    "Nama": inp_nama.strip(),
                    "Mapel": inp_mapel.strip(),
                    "Respons_jam": inp_respons,
                    "Umpan_balik": inp_umpan,
                    "Konsistensi": inp_konsisten,
                    "Konseling": inp_konseling,
                    "Indeks": indeks_hitung,
                }
                # Cek apakah nama sudah ada → update, belum ada → tambah
                nama_list = st.session_state.df_teacher["Nama"].str.lower().tolist()
                if inp_nama.strip().lower() in nama_list:
                    idx_update = st.session_state.df_teacher[
                        st.session_state.df_teacher["Nama"].str.lower() == inp_nama.strip().lower()
                    ].index[0]
                    for k, v in guru_baru.items():
                        st.session_state.df_teacher.at[idx_update, k] = v
                    st.success(f"✅ Data **{inp_nama}** berhasil diperbarui!")
                else:
                    new_row = pd.DataFrame([guru_baru])
                    st.session_state.df_teacher = pd.concat(
                        [st.session_state.df_teacher, new_row], ignore_index=True
                    )
                    st.success(f"✅ Guru **{inp_nama}** berhasil ditambahkan ke sistem!")
                safe_rerun()

        # Tabel data guru saat ini
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:14px;margin:20px 0 8px;'>📋 Daftar Guru Saat Ini</div>", unsafe_allow_html=True)
        st.dataframe(st.session_state.df_teacher, use_container_width=True, hide_index=True)

        # Tombol hapus
        st.markdown("<div style='color:#6B7694;font-size:13px;margin-top:12px;margin-bottom:6px;'>🗑️ Hapus data guru:</div>", unsafe_allow_html=True)
        if len(st.session_state.df_teacher) == 0:
            st.caption("Tidak ada data guru untuk dihapus.")
        else:
            nama_hapus = st.selectbox("Pilih guru yang akan dihapus",
                                      ["— pilih —"] + st.session_state.df_teacher["Nama"].tolist(),
                                      key="hapus_guru")
            if st.button("Hapus Guru Terpilih", key="btn_hapus_guru") and nama_hapus != "— pilih —":
                st.session_state.df_teacher = st.session_state.df_teacher[
                    st.session_state.df_teacher["Nama"] != nama_hapus
                ].reset_index(drop=True)
                st.success(f"🗑️ Data **{nama_hapus}** telah dihapus.")
                safe_rerun()


# ════════════════════════════════════════════════════════════
# H A L A M A N  5 : FAIRNESS PERCEPTION
# ════════════════════════════════════════════════════════════
elif halaman == "⚖️  Fairness Perception":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>⚖️ Modul 4: Fairness Perception Meter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Mencegah penarikan diri akibat diskriminasi sistemik dan participation gap.</p>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:8px;'>📊 Data Struktural Otomatis (Dapodik)</div>", unsafe_allow_html=True)
        fairness_metrics = {
            "Pemerataan Kesempatan Presentasi": 73,
            "Distribusi Perhatian Guru":        58,
            "Konsistensi Aturan Diterapkan":    82,
            "Akses Fasilitas Belajar":          69,
            "Representasi dalam Kegiatan":      61,
        }
        for label, val in fairness_metrics.items():
            c = "#2EC47F" if val >= 75 else "#F5A623" if val >= 55 else "#E55353"
            st.markdown(f"""
            <div style='margin-bottom:14px;'>
              <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                <span style='color:#2D3748;font-size:13px;'>{label}</span>
                <span style='color:{c};font-weight:700;'>{val}%</span>
              </div>
              {bar_h(val, color=c)}
            </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:8px;'>📋 Participation Gap per Siswa</div>", unsafe_allow_html=True)
        if len(df_filtered):
            fig_gap = px.scatter(df_filtered, x="Fairness", y="Engagement",
                                 color="Risiko", hover_name="Nama",
                                 color_discrete_map=COLORS, text="Nama")
            fig_gap.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                              line=dict(color="#CADCFC", dash="dot"))
            fig_gap.update_traces(textposition="top center", textfont_size=9, textfont_color="#1E2761")
            fig_gap.update_layout(**PLOT_LAYOUT, height=320,
                                  xaxis=dict(gridcolor="#EEF1F8", title="Fairness Score"),
                                  yaxis=dict(gridcolor="#EEF1F8", title="Engagement Score"))
            st.plotly_chart(fig_gap, use_container_width=True, config={"displayModeBar": False})
            st.caption("Titik di bawah garis = gap fairness → engagement yang perlu ditangani.")
        else:
            st.info("Tidak ada data untuk filter yang dipilih.")

    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin:12px 0 8px;'>📋 Detail Participation Gap</div>", unsafe_allow_html=True)
    if len(df_filtered):
        gap_df = df_filtered[["Nama", "Kelas", "Fairness", "Engagement"]].copy()
        gap_df["Gap"] = gap_df["Fairness"] - gap_df["Engagement"]
        gap_df["Status Gap"] = gap_df["Gap"].apply(
            lambda g: "⚠️ Perlu Perhatian" if g > 20 else "🔴 Berbahaya" if g < -10 else "✓ Normal")
        st.dataframe(
            gap_df.style.apply(make_gradient_styler(reverse=False), subset=["Gap"]),
            use_container_width=True, hide_index=True
        )


# ════════════════════════════════════════════════════════════
# H A L A M A N  6 : EARLY WARNING AI
# ════════════════════════════════════════════════════════════
elif halaman == "🤖  Early Warning AI":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>🤖 Mesin Prediksi: Early Warning System (EWS) Berbasis AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Output sistem ini adalah <em>actionable care</em>, bukan sekadar pelaporan statistik. Algoritma: AI + SMOTE Engine.</p>", unsafe_allow_html=True)

    levels = [
        {"level": "LEVEL MERAH",  "color": "#E55353", "risiko_key": "KRITIS",
         "action": "Intervensi segera. Koordinasi guru BK, wali kelas, kepala sekolah. Laporan ke Dapodik dalam 24 jam.", "icon": "🔴"},
        {"level": "LEVEL ORANYE", "color": "#F5A623", "risiko_key": "TINGGI",
         "action": "Konseling terjadwal 2×/minggu. Hubungi wali murid. Pertimbangkan diferensiasi tugas.", "icon": "🟠"},
        {"level": "LEVEL KUNING", "color": "#F5C842", "risiko_key": "SEDANG",
         "action": "Guru memberikan perhatian ekstra dan check-in mingguan. Variasikan metode pembelajaran.", "icon": "🟡"},
    ]

    for lvl in levels:
        siswa_list = df[df["Risiko"] == lvl["risiko_key"]]["Nama"].tolist()
        if not siswa_list:
            continue
        with st.expander(f"{lvl['icon']} {lvl['level']} — {len(siswa_list)} siswa", expanded=(lvl["risiko_key"] == "KRITIS")):
            names_str = " · ".join(siswa_list)
            st.markdown(f"""
            <div style='background:{lvl["color"]}10;border:1px solid {lvl["color"]}40;
                        border-radius:10px;padding:14px 18px;margin-bottom:12px;'>
              <div style='color:{lvl["color"]};font-weight:700;margin-bottom:6px;'>Siswa teridentifikasi:</div>
              <div style='color:#2D3748;font-size:14px;margin-bottom:12px;'>{names_str}</div>
              <div style='background:#FFFFFF;border-radius:8px;padding:12px 14px;color:#2D3748;font-size:14px;'>
                💡 <strong style='color:{lvl["color"]};'>Tindakan:</strong> {lvl["action"]}
              </div>
            </div>""", unsafe_allow_html=True)
            detail = df[df["Risiko"] == lvl["risiko_key"]][["Nama", "Kelas", "Burnout", "Kognitif", "Fairness", "Engagement", "Status"]]
            st.dataframe(detail, use_container_width=True, hide_index=True)

    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin:20px 0 10px;'>⚙️ Cara Kerja Mesin Prediksi</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (icon, title, desc) in zip([c1, c2, c3], [
        ("📊", "Input Multi-Layer",    "Data perilaku (LMS), administratif (Dapodik), dan sosial-ekonomi (DTKS) digabung setiap minggu."),
        ("🤖", "AI + SMOTE Engine",    "Algoritma menimbang pola 4 modul dan mengkompensasi ketidakseimbangan data dengan SMOTE."),
        ("🎯", "Actionable Output",    "Setiap prediksi menghasilkan skor risiko, profil psikologis, dan rekomendasi tindakan spesifik."),
    ]):
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='text-align:center;'>
              <div style='font-size:32px;margin-bottom:8px;'>{icon}</div>
              <div style='color:#1E2761;font-weight:700;font-size:15px;margin-bottom:8px;'>{title}</div>
              <div style='color:#6B7694;font-size:13px;line-height:1.7;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    # Heatmap engagement
    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:15px;margin:16px 0 8px;'>🗺️ Engagement Score Map</div>", unsafe_allow_html=True)
    pivot = df.pivot_table(index="Status", columns="Kelas", values="Engagement", aggfunc="mean").round(1)
    fig_heat = px.imshow(pivot, text_auto=True,
                         color_continuous_scale=["#E55353", "#F5A623", "#2EC47F"], aspect="auto")
    fig_heat.update_layout(**PLOT_LAYOUT, height=280, coloraxis_colorbar=dict(tickfont=dict(color="#1E2761")))
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})


# ════════════════════════════════════════════════════════════
# H A L A M A N  7 : PULSE SURVEY
# ════════════════════════════════════════════════════════════
elif halaman == "📋  Pulse Survey":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>📋 Pulse Survey Mingguan</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Hanya 5 menit. Respons direkam dan langsung dianalisis sistem setiap Jumat.</p>", unsafe_allow_html=True)

    st.markdown("<div style='color:#1E2761;font-weight:700;font-size:13px;margin-bottom:12px;'>📅 Minggu ke-6 · 27 Juni 2026</div>", unsafe_allow_html=True)

    with st.form("pulse_survey"):
        ps1, ps2 = st.columns(2)
        with ps1:
            nama  = st.text_input("Nama Siswa *", placeholder="Tulis nama lengkap kamu")
        with ps2:
            kelas = st.selectbox("Kelas *", ["VIII-A", "VIII-B", "VIII-C"])

        st.markdown("<hr style='border-color:#E8ECF4;margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown("**🔥 Dimensi Burnout**")
        q1 = st.slider("Seberapa lelah kamu secara emosional menghadapi sekolah minggu ini?", 1, 5, 3,
                        help="1 = Sangat segar, 5 = Sangat kelelahan")
        q2 = st.slider("Seberapa besar kamu merasa 'tidak peduli lagi' terhadap nilai atau prestasi?", 1, 5, 2)

        st.markdown("<hr style='border-color:#E8ECF4;margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown("**🧠 Dimensi Beban Kognitif**")
        q3 = st.slider("Seberapa berat beban tugas yang kamu rasakan minggu ini?", 1, 5, 3)
        q4 = st.slider("Apakah kamu kesulitan fokus saat belajar atau mengerjakan tugas?", 1, 5, 2)

        st.markdown("<hr style='border-color:#E8ECF4;margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown("**⚖️ Dimensi Keadilan**")
        q5 = st.radio("Apakah kamu merasa diperlakukan adil oleh guru dan sekolah?",
                       ["Ya, sangat adil", "Cukup adil", "Kurang adil", "Tidak adil sama sekali"])
        q6 = st.text_area("Ada yang ingin kamu ceritakan atau sampaikan ke sekolah?",
                           placeholder="Opsional — semua jawaban bersifat rahasia", max_chars=300)

        submitted = st.form_submit_button("✅ Kirim Survei Minggu Ini")

    if submitted:
        if not nama.strip():
            st.warning("⚠️ Harap isi nama kamu sebelum mengirim survei.")
        else:
            burnout_c  = int(((q1 + q2) / 10) * 100)
            kognitif_c = int(((q3 + q4) / 10) * 100)
            fair_map   = {"Ya, sangat adil": 90, "Cukup adil": 65, "Kurang adil": 40, "Tidak adil sama sekali": 15}
            fairness_c = fair_map.get(q5, 50)
            engage_c   = max(0, 100 - int(burnout_c * 0.5 + kognitif_c * 0.3 + (100 - fairness_c) * 0.2))

            if engage_c < 30 or burnout_c > 75:
                risiko_c = "KRITIS"
            elif engage_c < 50 or burnout_c > 60:
                risiko_c = "TINGGI"
            elif engage_c < 65:
                risiko_c = "SEDANG"
            else:
                risiko_c = "RENDAH"

            color = risk_color(risiko_c)
            with st.spinner("Menganalisis respons kamu..."):
                time.sleep(1.0)

            st.success("✅ Survei berhasil direkam! Terima kasih sudah meluangkan waktu.")
            if risiko_c in ["KRITIS", "TINGGI"]:
                catatan = "Data ini akan diteruskan ke wali kelas dan guru BK untuk tindak lanjut segera."
            else:
                catatan = "Terus semangat! Sistem akan terus memantau kesejahteraanmu."

            st.markdown(f"""
            <div style='background:#FFFFFF;border:1.5px solid {color}44;border-left:4px solid {color};
                        border-radius:12px;padding:20px 24px;margin-top:16px;
                        box-shadow:0 2px 10px rgba(30,39,97,0.08);'>
              <div style='color:{color};font-weight:800;font-size:17px;margin-bottom:14px;'>
                Profil Engagement — Hasil Analisis Sistem
              </div>
              <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;margin-bottom:14px;'>
                <div style='text-align:center;'>
                  <div style='font-size:30px;font-weight:900;color:#E55353;'>{burnout_c}</div>
                  <div style='color:#6B7694;font-size:11px;'>Skor Burnout</div>
                </div>
                <div style='text-align:center;'>
                  <div style='font-size:30px;font-weight:900;color:#F5A623;'>{kognitif_c}</div>
                  <div style='color:#6B7694;font-size:11px;'>Beban Kognitif</div>
                </div>
                <div style='text-align:center;'>
                  <div style='font-size:30px;font-weight:900;color:#1E2761;'>{fairness_c}</div>
                  <div style='color:#6B7694;font-size:11px;'>Fairness Score</div>
                </div>
                <div style='text-align:center;'>
                  <div style='font-size:30px;font-weight:900;color:{color};'>{engage_c}</div>
                  <div style='color:#6B7694;font-size:11px;'>Engagement Akhir</div>
                </div>
              </div>
              <div style='background:#F8F9FE;border-radius:8px;padding:12px 16px;'>
                <span style='color:{color};font-weight:700;'>Level Risiko: {risiko_c}</span>
                <span style='color:#2D3748;font-size:13px;'>  —  {catatan}</span>
              </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# H A L A M A N  8 : LAPORAN & EKSPOR
# ════════════════════════════════════════════════════════════
elif halaman == "📊  Laporan & Ekspor":
    st.markdown("<h1 style='color:#1E2761;font-size:22px;font-weight:900;margin:0 0 4px;'>📊 Laporan & Ekspor Data</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6B7694;font-size:14px;margin:0 0 20px;'>Unduh data engagement untuk laporan PTK, koordinasi guru BK, dan pelaporan ke Dapodik.</p>", unsafe_allow_html=True)

    tab_r1, tab_r2, tab_r3 = st.tabs(["📋 Ringkasan Eksekutif", "📥 Ekspor Data", "📅 Jadwal Intervensi"])

    with tab_r1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='kpi-card'>
              <div style='color:#F5A623;font-weight:700;margin-bottom:12px;'>📌 Temuan Utama Minggu Ini</div>
              <ul style='color:#2D3748;font-size:13px;line-height:2.1;margin:0;padding-left:18px;'>
                <li>2 siswa dalam status KRITIS — perlu intervensi dalam 24 jam</li>
                <li>Tren burnout meningkat 76% dalam 6 minggu terakhir</li>
                <li>VIII-B memiliki rata-rata burnout tertinggi (67)</li>
                <li>Rata-rata login harian hanya 14 menit (ideal: 40 menit)</li>
                <li>Fairness score VIII-C paling rendah di antara 3 kelas</li>
              </ul>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='kpi-card'>
              <div style='color:#1E2761;font-weight:700;margin-bottom:12px;'>✅ Rekomendasi Sistem</div>
              <ul style='color:#2D3748;font-size:13px;line-height:2.1;margin:0;padding-left:18px;'>
                <li>Aktivasi protokol konseling darurat untuk siswa KRITIS</li>
                <li>Review beban tugas VIII-B — pertimbangkan diferensiasi</li>
                <li>Pelatihan emotional intelligence untuk guru indeks terendah</li>
                <li>Tingkatkan frekuensi pulse survey menjadi 2×/minggu</li>
                <li>Integrasikan data DTKS Kemensos untuk konteks sosial-ekonomi</li>
              </ul>
            </div>""", unsafe_allow_html=True)

        fig_sum = make_subplots(rows=1, cols=2,
            subplot_titles=["Distribusi Engagement per Kelas", "Korelasi Burnout vs Engagement"])
        for kls, c in [("VIII-A", "#1E2761"), ("VIII-B", "#F5A623"), ("VIII-C", "#2EC47F")]:
            fig_sum.add_trace(go.Box(y=df[df["Kelas"] == kls]["Engagement"], name=kls,
                                     marker_color=c, showlegend=False), row=1, col=1)
        fig_sum.add_trace(go.Scatter(
            x=df["Burnout"], y=df["Engagement"],
            mode="markers+text", text=df["Nama"].apply(lambda n: n.split()[0]),
            textposition="top center", textfont=dict(size=9, color="#1E2761"),
            marker=dict(color=[risk_color(r) for r in df["Risiko"]], size=12),
            showlegend=False,
        ), row=1, col=2)
        fig_sum.update_layout(**PLOT_LAYOUT, height=320)
        for i in [1, 2]:
            fig_sum.update_xaxes(gridcolor="#EEF1F8", row=1, col=i)
            fig_sum.update_yaxes(gridcolor="#EEF1F8", row=1, col=i)
        st.plotly_chart(fig_sum, use_container_width=True, config={"displayModeBar": False})

    with tab_r2:
        st.markdown("<p style='color:#6B7694;font-size:13px;margin-bottom:12px;'>Pilih data yang ingin diekspor:</p>", unsafe_allow_html=True)
        ce1, ce2 = st.columns(2)
        with ce1:
            export_cols = st.multiselect("Kolom data siswa", df.columns.tolist(),
                default=["Nama", "Kelas", "Burnout", "Kognitif", "Fairness", "Engagement", "Risiko", "Status"])
        with ce2:
            export_filter = st.multiselect("Filter risiko", ["KRITIS", "TINGGI", "SEDANG", "RENDAH"],
                default=["KRITIS", "TINGGI"])

        export_df = df[df["Risiko"].isin(export_filter)][export_cols] if export_cols else df[df["Risiko"].isin(export_filter)]
        st.dataframe(export_df, use_container_width=True, hide_index=True)
        csv = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Unduh CSV", data=csv,
                           file_name=f"engagement_audit_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")

    with tab_r3:
        jadwal_df = pd.DataFrame([
            {"Hari": "Senin, 30 Juni",   "Waktu": "08.00", "Kegiatan": "Konseling darurat — Deni Raharjo & Hendra Wijaya",   "PIC": "Guru BK + Wali Kelas",       "Prioritas": "🔴 KRITIS"},
            {"Hari": "Selasa, 1 Juli",   "Waktu": "10.00", "Kegiatan": "Check-in langsung — Andi Pratama & Fajar Nugroho",   "PIC": "Wali Kelas VIII-A & VIII-C", "Prioritas": "🟠 TINGGI"},
            {"Hari": "Rabu, 2 Juli",     "Waktu": "13.00", "Kegiatan": "Rapat koordinasi guru — review beban tugas VIII-B",  "PIC": "Kepala Sekolah",             "Prioritas": "⚠️ Sistemik"},
            {"Hari": "Jumat, 4 Juli",    "Waktu": "09.00", "Kegiatan": "Pulse Survey Minggu ke-7 dibuka",                    "PIC": "Admin LMS",                  "Prioritas": "📋 Rutin"},
        ])
        st.dataframe(jadwal_df, use_container_width=True, hide_index=True)


# ── Footer global ──────────────────────────────────────────────────────────────
st.markdown("<hr style='border-color:#E8ECF4;margin-top:40px;'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;padding:16px 0 8px;'>
    <div style='color:#1E2761;font-weight:800;font-size:14px;letter-spacing:0.5px;'>
        🎓 Tim Universitas Pekalongan
    </div>
    <div style='color:#6B7694;font-size:12px;margin-top:4px;'>
        FKIP · Program Studi Pendidikan Matematika · 2024/2025
    </div>
    <div style='color:#AABCD6;font-size:11px;margin-top:6px;'>
        LMS Engagement Audit v2.0 · Prototipe Deteksi Dini Quiet Quitting
    </div>
</div>
""", unsafe_allow_html=True)
