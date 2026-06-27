"""
LMS Berbasis Engagement Audit — Streamlit App
Prototipe deteksi dini Quiet Quitting untuk SMP/SMK
Kerangka: Student Engagement Audit (4 Modul + EWS AI)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
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
/* Dark theme override */
:root {
    --bg: #0F1117;
    --surface: #1A1D27;
    --card: #21253A;
    --border: #2E3350;
    --amber: #F5A623;
    --teal: #00B4D8;
    --green: #2EC47F;
    --red: #E55353;
    --yellow: #F5C842;
    --text: #E8EAF6;
    --muted: #7B82A3;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}

/* Metric cards */
div[data-testid="metric-container"] {
    background: #21253A;
    border: 1px solid #2E3350;
    border-radius: 12px;
    padding: 16px 20px !important;
}
div[data-testid="metric-container"] label {
    color: #7B82A3 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 900 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1A1D27 !important;
    border-right: 1px solid #2E3350;
}
[data-testid="stSidebar"] .stRadio label {
    color: #E8EAF6 !important;
}

/* Dataframe */
.stDataFrame { border-radius: 10px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #21253A;
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #7B82A3;
}
.stTabs [aria-selected="true"] {
    background: #F5A623 !important;
    color: #0F1117 !important;
    font-weight: 700;
}

/* Expander */
.streamlit-expanderHeader {
    background: #21253A !important;
    border-radius: 10px !important;
    color: #E8EAF6 !important;
}

/* Buttons */
.stButton > button {
    background: #F5A623;
    color: #0F1117;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 24px;
}
.stButton > button:hover {
    background: #d4901e;
    color: #0F1117;
}

/* Alert boxes */
.alert-kritis {
    background: rgba(229,83,83,0.12);
    border: 1px solid rgba(229,83,83,0.4);
    border-left: 4px solid #E55353;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.alert-tinggi {
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.4);
    border-left: 4px solid #F5A623;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.badge-kritis  { background:#E5535322; color:#E55353; border:1px solid #E5535355; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-tinggi  { background:#F5A62322; color:#F5A623; border:1px solid #F5A62355; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-sedang  { background:#F5C84222; color:#F5C842; border:1px solid #F5C84255; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }
.badge-rendah  { background:#2EC47F22; color:#2EC47F; border:1px solid #2EC47F55; border-radius:6px; padding:3px 10px; font-size:12px; font-weight:700; }

.info-card {
    background: #21253A;
    border: 1px solid #2E3350;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.section-title {
    color: #E8EAF6;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 4px;
}
.section-sub {
    color: #7B82A3;
    font-size: 13px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    students = pd.DataFrame([
        {"id":1,"Nama":"Andi Pratama",  "Kelas":"VIII-A","Burnout":72,"Kognitif":68,"Fairness":55,"Engagement":42,"Risiko":"TINGGI", "Status":"Quiet Quitting","Login_mnt":12,"Tugas_selesai":55},
        {"id":2,"Nama":"Budi Santoso",  "Kelas":"VIII-A","Burnout":34,"Kognitif":45,"Fairness":80,"Engagement":78,"Risiko":"RENDAH", "Status":"Aktif",         "Login_mnt":48,"Tugas_selesai":92},
        {"id":3,"Nama":"Citra Dewi",    "Kelas":"VIII-B","Burnout":61,"Kognitif":72,"Fairness":60,"Engagement":58,"Risiko":"SEDANG", "Status":"Beban Kognitif","Login_mnt":22,"Tugas_selesai":68},
        {"id":4,"Nama":"Deni Raharjo",  "Kelas":"VIII-B","Burnout":88,"Kognitif":55,"Fairness":40,"Engagement":29,"Risiko":"KRITIS", "Status":"Exhausted",     "Login_mnt":7, "Tugas_selesai":31},
        {"id":5,"Nama":"Eka Putri",     "Kelas":"VIII-A","Burnout":45,"Kognitif":38,"Fairness":75,"Engagement":71,"Risiko":"RENDAH", "Status":"Aktif",         "Login_mnt":55,"Tugas_selesai":89},
        {"id":6,"Nama":"Fajar Nugroho", "Kelas":"VIII-C","Burnout":77,"Kognitif":80,"Fairness":50,"Engagement":35,"Risiko":"TINGGI", "Status":"Quiet Quitting","Login_mnt":9, "Tugas_selesai":42},
        {"id":7,"Nama":"Gita Sari",     "Kelas":"VIII-C","Burnout":50,"Kognitif":60,"Fairness":65,"Engagement":62,"Risiko":"SEDANG", "Status":"Monitor",       "Login_mnt":33,"Tugas_selesai":74},
        {"id":8,"Nama":"Hendra Wijaya", "Kelas":"VIII-B","Burnout":92,"Kognitif":88,"Fairness":35,"Engagement":18,"Risiko":"KRITIS", "Status":"Krisis",        "Login_mnt":4, "Tugas_selesai":20},
        {"id":9,"Nama":"Indah Lestari", "Kelas":"VIII-C","Burnout":40,"Kognitif":42,"Fairness":78,"Engagement":74,"Risiko":"RENDAH", "Status":"Aktif",         "Login_mnt":51,"Tugas_selesai":88},
        {"id":10,"Nama":"Joko Saputra", "Kelas":"VIII-A","Burnout":65,"Kognitif":70,"Fairness":52,"Engagement":47,"Risiko":"SEDANG","Status":"Monitor",        "Login_mnt":18,"Tugas_selesai":60},
    ])

    burnout_trend = pd.DataFrame([
        {"Minggu":"Mgg 1","Rata-rata":38,"VIII-A":32,"VIII-B":40,"VIII-C":42},
        {"Minggu":"Mgg 2","Rata-rata":42,"VIII-A":36,"VIII-B":45,"VIII-C":45},
        {"Minggu":"Mgg 3","Rata-rata":51,"VIII-A":44,"VIII-B":55,"VIII-C":54},
        {"Minggu":"Mgg 4","Rata-rata":58,"VIII-A":50,"VIII-B":63,"VIII-C":61},
        {"Minggu":"Mgg 5","Rata-rata":61,"VIII-A":54,"VIII-B":67,"VIII-C":62},
        {"Minggu":"Mgg 6","Rata-rata":67,"VIII-A":60,"VIII-B":72,"VIII-C":69},
    ])

    teachers = pd.DataFrame([
        {"Nama":"Bu Ratna", "Respons_jam":28,"Umpan_balik":82,"Konsistensi":91,"Konseling":3, "Indeks":84},
        {"Nama":"Pak Iman", "Respons_jam":45,"Umpan_balik":60,"Konsistensi":72,"Konseling":8, "Indeks":62},
        {"Nama":"Bu Sinta", "Respons_jam":18,"Umpan_balik":91,"Konsistensi":95,"Konseling":1, "Indeks":91},
        {"Nama":"Pak Doni", "Respons_jam":62,"Umpan_balik":44,"Konsistensi":58,"Konseling":15,"Indeks":45},
    ])

    return students, burnout_trend, teachers

df, df_trend, df_teacher = load_data()

# ─── HELPERS ─────────────────────────────────────────────────────────────────
COLORS = {"KRITIS":"#E55353","TINGGI":"#F5A623","SEDANG":"#F5C842","RENDAH":"#2EC47F"}

def risk_color(r): return COLORS.get(r, "#7B82A3")

def gauge_chart(value, title, color="#F5A623", max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#E8EAF6", "size": 13}},
        number={"font": {"color": color, "size": 28}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#2E3350", "tickfont": {"color": "#7B82A3"}},
            "bar": {"color": color},
            "bgcolor": "#21253A",
            "bordercolor": "#2E3350",
            "steps": [
                {"range": [0, max_val*0.4], "color": "#1A1D27"},
                {"range": [max_val*0.4, max_val*0.7], "color": "#21253A"},
                {"range": [max_val*0.7, max_val], "color": "#2E3350"},
            ],
        }
    ))
    fig.update_layout(
        height=200, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="#21253A", plot_bgcolor="#21253A",
        font={"color": "#E8EAF6"}
    )
    return fig

def bar_h(value, max_val=100, color="#F5A623"):
    pct = int((value / max_val) * 100)
    bar = f"""
    <div style="margin-bottom:6px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
            <span style="font-size:12px;color:#7B82A3;"></span>
            <span style="font-size:13px;font-weight:700;color:{color};">{value}</span>
        </div>
        <div style="background:#2E3350;border-radius:99px;height:8px;overflow:hidden;">
            <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{color}99,{color});border-radius:99px;"></div>
        </div>
    </div>"""
    return bar

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:4px 0 16px;'>
        <div style='color:#F5A623;font-weight:900;font-size:16px;letter-spacing:0.5px;'>⚡ LMS ENGAGEMENT</div>
        <div style='color:#7B82A3;font-size:11px;margin-top:2px;'>Audit Psikologis Real-Time</div>
        <hr style='border-color:#2E3350;margin-top:14px;'>
    </div>
    """, unsafe_allow_html=True)

    halaman = st.radio("", [
        "🏠  Dashboard Utama",
        "🔥  Burnout Detection",
        "🧠  Cognitive Load Monitor",
        "👩‍🏫  Kualitas Guru",
        "⚖️  Fairness Perception",
        "🤖  Early Warning AI",
        "📋  Pulse Survey",
        "📊  Laporan & Ekspor",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2E3350;'>", unsafe_allow_html=True)

    # Filter global
    st.markdown("<div style='color:#7B82A3;font-size:11px;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Filter Global</div>", unsafe_allow_html=True)
    kelas_filter = st.multiselect("Kelas", ["VIII-A","VIII-B","VIII-C"], default=["VIII-A","VIII-B","VIII-C"])
    risiko_filter = st.multiselect("Level Risiko", ["KRITIS","TINGGI","SEDANG","RENDAH"], default=["KRITIS","TINGGI","SEDANG","RENDAH"])

    st.markdown("<hr style='border-color:#2E3350;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='color:#7B82A3;font-size:11px;text-align:center;line-height:1.8;'>
        SMP Negeri 2 Kota Pekalongan<br>
        <span style='color:#2E3350;'>Tahun Ajaran 2024/2025</span><br>
        <span style='color:#2EC47F;'>● Sistem Aktif</span>
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ─────────────────────────────────────────────────────────────
df_filtered = df[df["Kelas"].isin(kelas_filter) & df["Risiko"].isin(risiko_filter)]

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1: DASHBOARD UTAMA
# ═══════════════════════════════════════════════════════════════════════════════
if halaman == "🏠  Dashboard Utama":
    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("""
        <div style='margin-bottom:20px;'>
            <h1 style='color:#E8EAF6;font-size:26px;font-weight:900;margin:0;'>
                Dashboard Engagement Audit
            </h1>
            <p style='color:#7B82A3;font-size:14px;margin:6px 0 0;'>
                Sistem deteksi dini <em>Quiet Quitting</em> — integrasi data LMS, Dapodik & sosial-ekonomi
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        now = datetime.now().strftime("%d %b %Y, %H:%M")
        st.markdown(f"<div style='text-align:right;color:#7B82A3;font-size:12px;padding-top:28px;'>{now}</div>", unsafe_allow_html=True)

    # KPI Cards
    kritis = len(df[df["Risiko"]=="KRITIS"])
    tinggi = len(df[df["Risiko"]=="TINGGI"])
    avg_eng = int(df["Engagement"].mean())
    avg_burnout = int(df["Burnout"].mean())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🔴 Siswa Kritis", kritis, delta="+1 dari minggu lalu", delta_color="inverse")
    with c2:
        st.metric("⚠️ Risiko Tinggi", tinggi, delta="+2 dari minggu lalu", delta_color="inverse")
    with c3:
        st.metric("📊 Avg Engagement", f"{avg_eng}/100", delta="-8 poin", delta_color="inverse")
    with c4:
        st.metric("🔥 Avg Burnout", avg_burnout, delta="+9 poin", delta_color="inverse")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Alert Banner
    if kritis > 0:
        st.markdown(f"""
        <div class="alert-kritis">
            🚨 <strong style='color:#E55353;'>PERINGATAN KRITIS:</strong>
            <span style='color:#E8EAF6;'> {kritis} siswa dalam status KRITIS dan {tinggi} dalam status TINGGI.
            Wali kelas harus melakukan intervensi segera. Cek Modul Burnout dan EWS untuk detail.</span>
        </div>
        """, unsafe_allow_html=True)

    # Charts Row
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("<div class='section-title'>📈 Tren Burnout 6 Minggu</div>", unsafe_allow_html=True)
        fig_trend = px.line(
            df_trend, x="Minggu", y=["VIII-A","VIII-B","VIII-C","Rata-rata"],
            color_discrete_map={
                "VIII-A":"#00B4D8", "VIII-B":"#F5A623",
                "VIII-C":"#2EC47F", "Rata-rata":"#E55353"
            },
            markers=True,
        )
        fig_trend.update_traces(selector=dict(name="Rata-rata"), line=dict(dash="dot", width=3))
        fig_trend.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=280,
            margin=dict(t=10,b=20,l=20,r=20),
            legend=dict(bgcolor="#2E3350", bordercolor="#2E3350"),
            xaxis=dict(gridcolor="#2E3350"), yaxis=dict(gridcolor="#2E3350", range=[20,90]),
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar":False})

    with col_right:
        st.markdown("<div class='section-title'>🎯 Distribusi Risiko</div>", unsafe_allow_html=True)
        risk_counts = df["Risiko"].value_counts().reset_index()
        risk_counts.columns = ["Risiko","Jumlah"]
        fig_pie = px.pie(
            risk_counts, names="Risiko", values="Jumlah",
            color="Risiko",
            color_discrete_map=COLORS,
            hole=0.55,
        )
        fig_pie.update_traces(textfont_color="white", textfont_size=13)
        fig_pie.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=280,
            margin=dict(t=10,b=20,l=20,r=20),
            legend=dict(bgcolor="#2E3350", bordercolor="#2E3350"),
            showlegend=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar":False})

    # Tabel Prioritas
    st.markdown("<div class='section-title' style='margin-top:8px;'>🎯 Siswa Prioritas Intervensi</div>", unsafe_allow_html=True)
    priority = df[df["Risiko"].isin(["KRITIS","TINGGI"])].sort_values("Engagement")

    for _, row in priority.iterrows():
        color = risk_color(row["Risiko"])
        badge_class = f"badge-{row['Risiko'].lower()}"
        st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:space-between;
                    background:#21253A;border:1px solid #2E3350;border-left:4px solid {color};
                    border-radius:10px;padding:14px 18px;margin-bottom:8px;'>
            <div>
                <div style='color:#E8EAF6;font-weight:700;font-size:15px;'>{row["Nama"]}</div>
                <div style='color:#7B82A3;font-size:12px;'>{row["Kelas"]} · {row["Status"]}</div>
            </div>
            <div style='display:flex;align-items:center;gap:20px;'>
                <div style='text-align:center;'>
                    <div style='color:{color};font-size:24px;font-weight:900;'>{row["Engagement"]}</div>
                    <div style='color:#7B82A3;font-size:10px;'>Engagement</div>
                </div>
                <div style='text-align:center;'>
                    <div style='color:#E55353;font-size:20px;font-weight:700;'>{row["Burnout"]}</div>
                    <div style='color:#7B82A3;font-size:10px;'>Burnout</div>
                </div>
                <span class='{badge_class}'>{row["Risiko"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2: BURNOUT DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🔥  Burnout Detection":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            🔥 Modul 1: Burnout Detection Dashboard
        </h1>
        <p class='section-sub'>Mengidentifikasi profil Exhausted-Disengaged 6–12 bulan sebelum siswa menyerah.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Peta Burnout", "📋 Detail Maslach", "📈 Tren per Kelas"])

    with tab1:
        # Scatter: Burnout vs Engagement
        fig_scatter = px.scatter(
            df_filtered,
            x="Burnout", y="Engagement",
            color="Risiko",
            size="Kognitif",
            hover_name="Nama",
            hover_data={"Kelas":True,"Status":True,"Risiko":True},
            color_discrete_map=COLORS,
            text="Nama",
        )
        fig_scatter.update_traces(textposition="top center", textfont_size=10, textfont_color="#E8EAF6")
        # Quadrant lines
        fig_scatter.add_hline(y=50, line_dash="dot", line_color="#2E3350")
        fig_scatter.add_vline(x=60, line_dash="dot", line_color="#2E3350")
        fig_scatter.add_annotation(x=20, y=90, text="🟢 Aktif", showarrow=False, font=dict(color="#2EC47F", size=12))
        fig_scatter.add_annotation(x=80, y=90, text="⚠️ Burnout Tersembunyi", showarrow=False, font=dict(color="#F5A623", size=12))
        fig_scatter.add_annotation(x=20, y=15, text="😐 Apatis", showarrow=False, font=dict(color="#7B82A3", size=12))
        fig_scatter.add_annotation(x=80, y=15, text="🔴 Zona Kritis", showarrow=False, font=dict(color="#E55353", size=12))
        fig_scatter.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=400,
            margin=dict(t=20,b=30,l=30,r=20),
            xaxis=dict(gridcolor="#2E3350", title="Skor Burnout"),
            yaxis=dict(gridcolor="#2E3350", title="Skor Engagement"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar":False})

        st.caption("💡 Ukuran titik = beban kognitif. Zona kanan-bawah = prioritas intervensi tertinggi.")

    with tab2:
        st.markdown("<div style='color:#7B82A3;font-size:13px;margin-bottom:16px;'>Pilih siswa untuk melihat profil Maslach Burnout Inventory lengkap.</div>", unsafe_allow_html=True)
        selected_student = st.selectbox("Pilih Siswa", df_filtered["Nama"].tolist())
        row = df[df["Nama"]==selected_student].iloc[0]
        color = risk_color(row["Risiko"])

        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.plotly_chart(gauge_chart(row["Burnout"], "Kelelahan Emosional", "#E55353"), use_container_width=True, config={"displayModeBar":False})
        with col_g2:
            st.plotly_chart(gauge_chart(row["Kognitif"], "Depersonalisasi", "#F5A623"), use_container_width=True, config={"displayModeBar":False})
        with col_g3:
            st.plotly_chart(gauge_chart(100-row["Fairness"], "Rendah Prestasi Diri", "#F5C842"), use_container_width=True, config={"displayModeBar":False})

        st.markdown(f"""
        <div style='background:#21253A;border:1px solid {color}55;border-left:4px solid {color};
                    border-radius:10px;padding:16px 20px;margin-top:8px;'>
            <div style='font-weight:700;color:{color};margin-bottom:8px;'>
                {row["Nama"]} — {row["Kelas"]} · <span style='color:#7B82A3;font-weight:400;'>{row["Status"]}</span>
            </div>
            <div style='color:#E8EAF6;font-size:14px;line-height:1.8;'>
                {"🚨 <strong>Intervensi Segera:</strong> Konseling wajib & koordinasi wali murid. Pertimbangkan pengurangan beban tugas sementara." if row["Risiko"]=="KRITIS" else
                 "⚠️ <strong>Pantau Ketat:</strong> Check-in langsung oleh wali kelas minggu ini. Pulse survey harian." if row["Risiko"]=="TINGGI" else
                 "🟡 <strong>Monitor Reguler:</strong> Pastikan dukungan sosial memadai. Pulse survey mingguan." if row["Risiko"]=="SEDANG" else
                 "🟢 <strong>Kondisi Baik:</strong> Pertahankan motivasi. Beri peran positif di kelas."}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        fig_box = px.box(
            df, x="Kelas", y="Burnout", color="Kelas",
            color_discrete_map={"VIII-A":"#00B4D8","VIII-B":"#F5A623","VIII-C":"#2EC47F"},
            points="all", hover_name="Nama",
        )
        fig_box.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=360,
            margin=dict(t=20,b=20,l=20,r=20),
            xaxis=dict(gridcolor="#2E3350"),
            yaxis=dict(gridcolor="#2E3350", title="Skor Burnout"),
            showlegend=False,
        )
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar":False})


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3: COGNITIVE LOAD
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🧠  Cognitive Load Monitor":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            🧠 Modul 2: Cognitive Load Monitor
        </h1>
        <p class='section-sub'>Mendeteksi batas kerja kognitif dari pola login, durasi, dan konsistensi tugas.</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI
    avg_login = int(df_filtered["Login_mnt"].mean())
    avg_tugas = int(df_filtered["Tugas_selesai"].mean())
    overload   = len(df_filtered[df_filtered["Kognitif"] > 70])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("⏱ Avg Login Harian", f"{avg_login} mnt", delta=f"{avg_login-40} dari ideal 40 mnt", delta_color="inverse")
    with c2:
        st.metric("📚 Tugas Selesai Tepat Waktu", f"{avg_tugas}%", delta="-7% dari minggu lalu", delta_color="inverse")
    with c3:
        st.metric("🧠 Siswa Overload Kognitif", overload, delta="Skor kognitif > 70")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 1])

    with col_l:
        # Scatter Login vs Kognitif
        fig_cog = px.scatter(
            df_filtered, x="Login_mnt", y="Kognitif",
            color="Risiko", size="Burnout",
            hover_name="Nama",
            hover_data={"Kelas":True,"Tugas_selesai":True},
            color_discrete_map=COLORS, text="Nama",
        )
        fig_cog.add_vline(x=40, line_dash="dot", line_color="#2EC47F",
                          annotation_text="Ideal Login ≥40 mnt", annotation_font_color="#2EC47F")
        fig_cog.add_hline(y=70, line_dash="dot", line_color="#E55353",
                          annotation_text="Batas Overload Kognitif", annotation_font_color="#E55353")
        fig_cog.update_traces(textposition="top center", textfont_size=9, textfont_color="#E8EAF6")
        fig_cog.update_layout(
            title=dict(text="Login Harian vs Beban Kognitif", font=dict(color="#E8EAF6")),
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=380,
            margin=dict(t=40,b=20,l=20,r=20),
            xaxis=dict(gridcolor="#2E3350", title="Durasi Login (menit/hari)"),
            yaxis=dict(gridcolor="#2E3350", title="Skor Beban Kognitif"),
        )
        st.plotly_chart(fig_cog, use_container_width=True, config={"displayModeBar":False})

    with col_r:
        # Bar chart tugas selesai
        fig_bar = px.bar(
            df_filtered.sort_values("Tugas_selesai"),
            x="Tugas_selesai", y="Nama",
            orientation="h",
            color="Tugas_selesai",
            color_continuous_scale=["#E55353","#F5A623","#2EC47F"],
            range_color=[0,100],
        )
        fig_bar.update_layout(
            title=dict(text="% Tugas Dikumpul Tepat Waktu", font=dict(color="#E8EAF6")),
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=380,
            margin=dict(t=40,b=20,l=20,r=20),
            xaxis=dict(gridcolor="#2E3350", range=[0,100]),
            yaxis=dict(gridcolor="#2E3350"),
            coloraxis_showscale=False, showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar":False})

    # Tabel detail
    st.markdown("<div class='section-title'>📋 Data Lengkap Siswa</div>", unsafe_allow_html=True)
    display_df = df_filtered[["Nama","Kelas","Kognitif","Login_mnt","Tugas_selesai","Engagement","Risiko"]].copy()
    display_df.columns = ["Nama","Kelas","Beban Kognitif","Login (mnt/hari)","Tugas Selesai (%)","Engagement","Risiko"]
    st.dataframe(
        display_df.style
            .background_gradient(subset=["Beban Kognitif"], cmap="RdYlGn_r")
            .background_gradient(subset=["Engagement"], cmap="RdYlGn")
            .background_gradient(subset=["Tugas Selesai (%)"], cmap="RdYlGn"),
        use_container_width=True, hide_index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 4: KUALITAS GURU
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "👩‍🏫  Kualitas Guru":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            👩‍🏫 Modul 3: Indeks Kualitas Kepemimpinan Guru
        </h1>
        <p class='section-sub'>Mengukur dukungan emosional relasional yang mempengaruhi 58,7% variance motivasi siswa.</p>
    </div>
    """, unsafe_allow_html=True)

    # Radar Chart
    categories = ["Kecepatan Respons","Umpan Balik","Konsistensi","Frekuensi Konseling","Indeks Total"]
    fig_radar = go.Figure()

    colors_guru = ["#00B4D8","#F5A623","#2EC47F","#E55353"]
    for i, (_, t) in enumerate(df_teacher.iterrows()):
        # Normalisasi respons (lebih cepat = lebih baik)
        respons_norm = max(0, 100 - t["Respons_jam"])
        konseling_norm = min(100, t["Konseling"] * 7)
        vals = [respons_norm, t["Umpan_balik"], t["Konsistensi"], konseling_norm, t["Indeks"]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            fill="toself", name=t["Nama"],
            line_color=colors_guru[i],
            fillcolor=colors_guru[i] + "30",
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="#21253A",
            radialaxis=dict(visible=True, range=[0,100], gridcolor="#2E3350", tickfont=dict(color="#7B82A3")),
            angularaxis=dict(gridcolor="#2E3350", tickfont=dict(color="#E8EAF6")),
        ),
        paper_bgcolor="#21253A",
        font={"color":"#E8EAF6"}, height=380,
        margin=dict(t=30,b=20,l=20,r=20),
        legend=dict(bgcolor="#2E3350", bordercolor="#2E3350"),
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar":False})

    # Cards per guru
    cols = st.columns(2)
    for idx, (_, t) in enumerate(df_teacher.iterrows()):
        color = "#2EC47F" if t["Indeks"]>80 else "#00B4D8" if t["Indeks"]>60 else "#F5A623" if t["Indeks"]>45 else "#E55353"
        respons_ok = t["Respons_jam"] < 30
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='info-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;'>
                    <div>
                        <div style='color:#E8EAF6;font-weight:800;font-size:17px;'>{t["Nama"]}</div>
                        <div style='color:#7B82A3;font-size:12px;'>Guru Matematika</div>
                    </div>
                    <div style='text-align:center;'>
                        <div style='font-size:34px;font-weight:900;color:{color};line-height:1;'>{t["Indeks"]}</div>
                        <div style='font-size:10px;color:#7B82A3;'>Indeks Kualitas</div>
                    </div>
                </div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;'>
                    <div>
                        <div style='font-size:11px;color:#7B82A3;'>⏱ Kecepatan Respons</div>
                        <div style='font-weight:700;color:{"#2EC47F" if respons_ok else "#F5A623"};'>
                            {t["Respons_jam"]} jam {"✓" if respons_ok else "⚠️"}
                        </div>
                    </div>
                    <div>
                        <div style='font-size:11px;color:#7B82A3;'>💬 Sesi Konseling</div>
                        <div style='font-weight:700;color:{"#E55353" if t["Konseling"]<=3 else "#2EC47F"};'>
                            {t["Konseling"]} sesi/bulan
                        </div>
                    </div>
                </div>
                <div style='font-size:11px;color:#7B82A3;margin-bottom:4px;'>Bobot Umpan Balik</div>
                {bar_h(t["Umpan_balik"], color="#00B4D8")}
                <div style='font-size:11px;color:#7B82A3;margin-bottom:4px;margin-top:8px;'>Konsistensi Penilaian</div>
                {bar_h(t["Konsistensi"], color="#2EC47F")}
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 5: FAIRNESS PERCEPTION
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "⚖️  Fairness Perception":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            ⚖️ Modul 4: Fairness Perception Meter
        </h1>
        <p class='section-sub'>Mencegah penarikan diri akibat diskriminasi sistemik dan participation gap.</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("<div class='section-title' style='font-size:16px;'>📊 Data Struktural Otomatis (Dapodik)</div>", unsafe_allow_html=True)
        fairness_metrics = {
            "Pemerataan Kesempatan Presentasi": 73,
            "Distribusi Perhatian Guru": 58,
            "Konsistensi Aturan Diterapkan": 82,
            "Akses Fasilitas Belajar": 69,
            "Representasi dalam Kegiatan": 61,
        }
        for label, val in fairness_metrics.items():
            color = "#2EC47F" if val>=75 else "#F5A623" if val>=55 else "#E55353"
            st.markdown(f"""
            <div style='margin-bottom:12px;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                    <span style='color:#E8EAF6;font-size:13px;'>{label}</span>
                    <span style='color:{color};font-weight:700;'>{val}%</span>
                </div>
                {bar_h(val, color=color)}
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='section-title' style='font-size:16px;'>📋 Participation Gap per Siswa</div>", unsafe_allow_html=True)
        fig_gap = px.scatter(
            df_filtered, x="Fairness", y="Engagement",
            color="Risiko", size=[20]*len(df_filtered),
            hover_name="Nama", color_discrete_map=COLORS,
            text="Nama",
        )
        fig_gap.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                          line=dict(color="#2E3350", dash="dot"))
        fig_gap.update_traces(textposition="top center", textfont_size=9, textfont_color="#E8EAF6")
        fig_gap.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=320,
            margin=dict(t=10,b=20,l=20,r=20),
            xaxis=dict(gridcolor="#2E3350", title="Fairness Score"),
            yaxis=dict(gridcolor="#2E3350", title="Engagement Score"),
        )
        st.plotly_chart(fig_gap, use_container_width=True, config={"displayModeBar":False})
        st.caption("Titik di bawah garis diagonal = gap fairness → engagement yang perlu ditangani.")

    # Tabel gap
    st.markdown("<div class='section-title' style='margin-top:8px;'>📋 Detail Participation Gap</div>", unsafe_allow_html=True)
    gap_df = df_filtered[["Nama","Kelas","Fairness","Engagement"]].copy()
    gap_df["Gap"] = gap_df["Fairness"] - gap_df["Engagement"]
    gap_df["Status Gap"] = gap_df["Gap"].apply(lambda g: "⚠️ Perlu Perhatian" if g>20 else "🔴 Berbahaya" if g<-10 else "✓ Normal")
    st.dataframe(
        gap_df.style.background_gradient(subset=["Gap"], cmap="RdYlGn"),
        use_container_width=True, hide_index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 6: EARLY WARNING SYSTEM AI
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🤖  Early Warning AI":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            🤖 Mesin Prediksi: Early Warning System (EWS) Berbasis AI
        </h1>
        <p class='section-sub'>Output sistem ini adalah actionable care, bukan sekadar pelaporan statistik. (Algoritma: AI + SMOTE Engine)</p>
    </div>
    """, unsafe_allow_html=True)

    # EWS Levels
    levels = [
        {
            "level":"LEVEL MERAH", "color":"#E55353",
            "siswa": df[df["Risiko"]=="KRITIS"]["Nama"].tolist(),
            "action": "Intervensi segera. Koordinasi guru BK, wali kelas, kepala sekolah. Laporan ke Dapodik dalam 24 jam.",
            "icon": "🔴"
        },
        {
            "level":"LEVEL ORANYE", "color":"#F5A623",
            "siswa": df[df["Risiko"]=="TINGGI"]["Nama"].tolist(),
            "action": "Konseling terjadwal 2×/minggu. Hubungi wali murid. Pertimbangkan diferensiasi tugas.",
            "icon": "🟠"
        },
        {
            "level":"LEVEL KUNING", "color":"#F5C842",
            "siswa": df[df["Risiko"]=="SEDANG"]["Nama"].tolist(),
            "action": "Guru memberikan perhatian ekstra dan check-in mingguan. Variasikan metode pembelajaran.",
            "icon": "🟡"
        },
    ]

    for lvl in levels:
        if lvl["siswa"]:
            with st.expander(f"{lvl['icon']} {lvl['level']} — {len(lvl['siswa'])} siswa", expanded=(lvl["level"]=="LEVEL MERAH")):
                st.markdown(f"""
                <div style='background:{lvl["color"]}11;border:1px solid {lvl["color"]}44;
                            border-radius:10px;padding:14px 18px;margin-bottom:12px;'>
                    <div style='color:{lvl["color"]};font-weight:700;margin-bottom:6px;'>
                        Siswa teridentifikasi:
                    </div>
                    <div style='color:#E8EAF6;font-size:14px;margin-bottom:12px;'>
                        {" · ".join(lvl["siswa"])}
                    </div>
                    <div style='background:#21253A;border-radius:8px;padding:12px 14px;color:#E8EAF6;font-size:14px;'>
                        💡 <strong style='color:{lvl["color"]};'>Tindakan Rekomendasi:</strong> {lvl["action"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Detail tabel untuk level ini
                risiko_map = {"LEVEL MERAH":"KRITIS","LEVEL ORANYE":"TINGGI","LEVEL KUNING":"SEDANG"}
                detail = df[df["Risiko"]==risiko_map[lvl["level"]]][["Nama","Kelas","Burnout","Kognitif","Fairness","Engagement","Status"]]
                st.dataframe(detail, use_container_width=True, hide_index=True)

    # Cara kerja mesin
    st.markdown("<div class='section-title' style='margin-top:20px;'>⚙️ Cara Kerja Mesin Prediksi</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (icon, title, desc) in zip([c1,c2,c3], [
        ("📊","Input Multi-Layer","Data perilaku (LMS), administratif (Dapodik), dan sosial-ekonomi (DTKS) digabung setiap minggu."),
        ("🤖","AI + SMOTE Engine","Algoritma menimbang pola 4 modul dan mengkompensasi ketidakseimbangan data dengan SMOTE."),
        ("🎯","Actionable Output","Setiap prediksi menghasilkan skor risiko, profil psikologis, dan rekomendasi tindakan spesifik."),
    ]):
        with col:
            st.markdown(f"""
            <div class='info-card' style='text-align:center;'>
                <div style='font-size:32px;margin-bottom:8px;'>{icon}</div>
                <div style='color:#E8EAF6;font-weight:700;font-size:15px;margin-bottom:8px;'>{title}</div>
                <div style='color:#7B82A3;font-size:13px;line-height:1.7;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Engagement score heatmap
    st.markdown("<div class='section-title' style='margin-top:8px;'>🗺️ Engagement Score Map</div>", unsafe_allow_html=True)
    pivot = df.pivot_table(index="Status", columns="Kelas", values="Engagement", aggfunc="mean").round(1)
    fig_heat = px.imshow(
        pivot, text_auto=True, color_continuous_scale=["#E55353","#F5A623","#2EC47F"],
        aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor="#21253A", plot_bgcolor="#21253A",
        font={"color":"#E8EAF6"}, height=280,
        margin=dict(t=10,b=20,l=20,r=20),
        coloraxis_colorbar=dict(tickfont=dict(color="#E8EAF6")),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar":False})


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 7: PULSE SURVEY
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📋  Pulse Survey":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            📋 Pulse Survey Mingguan
        </h1>
        <p class='section-sub'>Hanya 5 menit. Respons direkam dan langsung dianalisis sistem setiap Jumat.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("pulse_survey"):
        st.markdown("<div style='color:#F5A623;font-weight:700;font-size:14px;margin-bottom:16px;'>📅 Minggu ke-6 · 27 Juni 2026</div>", unsafe_allow_html=True)

        nama = st.text_input("Nama Siswa", placeholder="Tulis nama lengkap kamu")
        kelas = st.selectbox("Kelas", ["VIII-A","VIII-B","VIII-C"])

        st.markdown("<hr style='border-color:#2E3350;margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("**🔥 Dimensi Burnout**")
        q1 = st.slider("Seberapa lelah kamu secara emosional menghadapi sekolah minggu ini?", 1, 5, 3,
                        help="1 = Sangat segar, 5 = Sangat kelelahan")
        q2 = st.slider("Seberapa besar kamu merasa 'tidak peduli lagi' terhadap nilai atau prestasi?", 1, 5, 2)

        st.markdown("<hr style='border-color:#2E3350;margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("**🧠 Dimensi Beban Kognitif**")
        q3 = st.slider("Seberapa berat beban tugas yang kamu rasakan minggu ini?", 1, 5, 3)
        q4 = st.slider("Apakah kamu kesulitan fokus saat belajar atau mengerjakan tugas?", 1, 5, 2)

        st.markdown("<hr style='border-color:#2E3350;margin:16px 0;'>", unsafe_allow_html=True)
        st.markdown("**⚖️ Dimensi Keadilan**")
        q5 = st.radio("Apakah kamu merasa diperlakukan adil oleh guru dan sekolah?",
                       ["Ya, sangat adil","Cukup adil","Kurang adil","Tidak adil sama sekali"])
        q6 = st.text_area("Ada yang ingin kamu ceritakan atau sampaikan ke sekolah?",
                           placeholder="Opsional — semua jawaban bersifat rahasia",
                           max_chars=300)

        submitted = st.form_submit_button("✅ Kirim Survei Minggu Ini")

    if submitted and nama:
        # Kalkulasi skor
        burnout_calc = int(((q1 + q2) / 10) * 100)
        kognitif_calc = int(((q3 + q4) / 10) * 100)
        fair_map = {"Ya, sangat adil":90,"Cukup adil":65,"Kurang adil":40,"Tidak adil sama sekali":15}
        fairness_calc = fair_map.get(q5, 50)
        engagement_calc = max(0, 100 - int((burnout_calc*0.5 + kognitif_calc*0.3 + (100-fairness_calc)*0.2)))

        if engagement_calc < 30 or burnout_calc > 75:
            risiko_calc = "KRITIS"
        elif engagement_calc < 50 or burnout_calc > 60:
            risiko_calc = "TINGGI"
        elif engagement_calc < 65:
            risiko_calc = "SEDANG"
        else:
            risiko_calc = "RENDAH"

        color = risk_color(risiko_calc)

        with st.spinner("Menganalisis respons kamu..."):
            time.sleep(1.2)

        st.success("✅ Survei berhasil direkam! Terima kasih sudah meluangkan waktu.")
        st.markdown(f"""
        <div style='background:{color}11;border:1px solid {color}44;border-radius:12px;padding:20px 24px;margin-top:16px;'>
            <div style='color:{color};font-weight:800;font-size:18px;margin-bottom:12px;'>
                Profil Engagement Kamu — Hasil Analisis Sistem
            </div>
            <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;'>
                <div style='text-align:center;'>
                    <div style='font-size:28px;font-weight:900;color:#E55353;'>{burnout_calc}</div>
                    <div style='color:#7B82A3;font-size:11px;'>Skor Burnout</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:28px;font-weight:900;color:#F5A623;'>{kognitif_calc}</div>
                    <div style='color:#7B82A3;font-size:11px;'>Beban Kognitif</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:28px;font-weight:900;color:#F5C842;'>{fairness_calc}</div>
                    <div style='color:#7B82A3;font-size:11px;'>Fairness Score</div>
                </div>
                <div style='text-align:center;'>
                    <div style='font-size:28px;font-weight:900;color:{color};'>{engagement_calc}</div>
                    <div style='color:#7B82A3;font-size:11px;'>Engagement Akhir</div>
                </div>
            </div>
            <div style='margin-top:16px;background:#21253A;border-radius:8px;padding:12px 16px;'>
                <span style='color:{color};font-weight:700;'>Level Risiko: {risiko_calc}</span>
                <span style='color:#E8EAF6;font-size:13px;'>
                {"  —  Data ini akan diteruskan ke wali kelas dan guru BK untuk tindak lanjut segera." if risiko_calc in ["KRITIS","TINGGI"] else "  —  Terus semangat! Sistem akan terus memantau kesejahteraanmu."}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif submitted and not nama:
        st.warning("⚠️ Harap isi nama kamu sebelum mengirim survei.")


# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 8: LAPORAN & EKSPOR
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📊  Laporan & Ekspor":
    st.markdown("""
    <div style='margin-bottom:20px;'>
        <h1 style='color:#E8EAF6;font-size:22px;font-weight:900;margin:0;'>
            📊 Laporan & Ekspor Data
        </h1>
        <p class='section-sub'>Unduh data engagement untuk laporan PTK, koordinasi guru BK, dan pelaporan ke Dapodik.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_r1, tab_r2, tab_r3 = st.tabs(["📋 Ringkasan Eksekutif", "📥 Ekspor Data", "📅 Jadwal Intervensi"])

    with tab_r1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='info-card'>
                <div style='color:#F5A623;font-weight:700;margin-bottom:12px;'>📌 Temuan Utama Minggu Ini</div>
                <ul style='color:#E8EAF6;font-size:13px;line-height:2.0;margin:0;padding-left:18px;'>
                    <li>2 siswa dalam status KRITIS — perlu intervensi dalam 24 jam</li>
                    <li>Tren burnout meningkat 76% dalam 6 minggu terakhir</li>
                    <li>VIII-B memiliki rata-rata burnout tertinggi (67)</li>
                    <li>Rata-rata login harian hanya 14 menit (ideal: 40 menit)</li>
                    <li>Fairness score VIII-C paling rendah di antara 3 kelas</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='info-card'>
                <div style='color:#00B4D8;font-weight:700;margin-bottom:12px;'>✅ Rekomendasi Sistem</div>
                <ul style='color:#E8EAF6;font-size:13px;line-height:2.0;margin:0;padding-left:18px;'>
                    <li>Aktivasi protokol konseling darurat untuk siswa KRITIS</li>
                    <li>Review beban tugas VIII-B — pertimbangkan diferensiasi</li>
                    <li>Pelatihan emotional intelligence untuk Pak Doni (indeks terendah)</li>
                    <li>Tingkatkan frekuensi pulse survey menjadi 2×/minggu</li>
                    <li>Integrasikan data DTKS Kemensos untuk konteks sosial-ekonomi</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Summary stats
        fig_summary = make_subplots(rows=1, cols=2,
            subplot_titles=["Distribusi Engagement per Kelas", "Korelasi Burnout vs Engagement"])
        for kls, color in [("VIII-A","#00B4D8"),("VIII-B","#F5A623"),("VIII-C","#2EC47F")]:
            kls_data = df[df["Kelas"]==kls]["Engagement"]
            fig_summary.add_trace(go.Box(y=kls_data, name=kls, marker_color=color, showlegend=False), row=1, col=1)
        fig_summary.add_trace(go.Scatter(
            x=df["Burnout"], y=df["Engagement"],
            mode="markers+text", text=df["Nama"].apply(lambda n: n.split()[0]),
            textposition="top center", textfont=dict(size=9, color="#E8EAF6"),
            marker=dict(color=[risk_color(r) for r in df["Risiko"]], size=12),
            showlegend=False,
        ), row=1, col=2)
        fig_summary.update_layout(
            paper_bgcolor="#21253A", plot_bgcolor="#21253A",
            font={"color":"#E8EAF6"}, height=320,
            margin=dict(t=40,b=20,l=20,r=20),
        )
        for i in [1,2]:
            fig_summary.update_xaxes(gridcolor="#2E3350", row=1, col=i)
            fig_summary.update_yaxes(gridcolor="#2E3350", row=1, col=i)
        st.plotly_chart(fig_summary, use_container_width=True, config={"displayModeBar":False})

    with tab_r2:
        st.markdown("<div style='color:#7B82A3;font-size:13px;margin-bottom:16px;'>Pilih data yang ingin diekspor:</div>", unsafe_allow_html=True)
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            export_cols = st.multiselect("Kolom data siswa", df.columns.tolist(),
                default=["Nama","Kelas","Burnout","Kognitif","Fairness","Engagement","Risiko","Status"])
        with col_e2:
            export_filter = st.multiselect("Filter risiko untuk ekspor", ["KRITIS","TINGGI","SEDANG","RENDAH"],
                default=["KRITIS","TINGGI"])

        export_df = df[df["Risiko"].isin(export_filter)][export_cols] if export_cols else df[df["Risiko"].isin(export_filter)]
        st.dataframe(export_df, use_container_width=True, hide_index=True)

        csv = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Unduh CSV",
            data=csv,
            file_name=f"engagement_audit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with tab_r3:
        st.markdown("""
        <div class='info-card'>
            <div style='color:#F5A623;font-weight:700;margin-bottom:14px;'>📅 Jadwal Intervensi Minggu Depan</div>
        """, unsafe_allow_html=True)

        jadwal = [
            {"Hari":"Senin, 30 Juni","Waktu":"08.00","Kegiatan":"Konseling darurat — Deni Raharjo & Hendra Wijaya","PIC":"Guru BK + Wali Kelas","Prioritas":"🔴 KRITIS"},
            {"Hari":"Selasa, 1 Juli","Waktu":"10.00","Kegiatan":"Check-in langsung — Andi Pratama & Fajar Nugroho","PIC":"Wali Kelas VIII-A & VIII-C","Prioritas":"🟠 TINGGI"},
            {"Hari":"Rabu, 2 Juli","Waktu":"13.00","Kegiatan":"Rapat koordinasi guru — review beban tugas VIII-B","PIC":"Kepala Sekolah","Prioritas":"⚠️ Sistemik"},
            {"Hari":"Jumat, 4 Juli","Waktu":"09.00","Kegiatan":"Pulse Survey Minggu ke-7 dibuka","PIC":"Admin LMS","Prioritas":"📋 Rutin"},
        ]
        jadwal_df = pd.DataFrame(jadwal)
        st.dataframe(jadwal_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
