from pathlib import Path
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sample-data"
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(page_title="GTM + GA4 Measurement Dashboard", page_icon="📡", layout="wide")

# ---------- Shared styling (matches the Lead Scoring dashboard) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap');
.stApp { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Poppins', sans-serif !important; letter-spacing:-.5px; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; }
div[data-testid="stMetric"] {
    background:#111827; border:1px solid #2b3553; border-radius:14px;
    padding:16px 18px; box-shadow:0 4px 18px rgba(0,0,0,.35);
}
div[data-testid="stMetricValue"] { font-size:26px; }
</style>
""", unsafe_allow_html=True)

# One palette used everywhere = cohesive look
SEVERITY_COLORS = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#3b82f6"}
ACCENT = ["#60a5fa", "#34d399", "#f59e0b", "#a78bfa", "#f472b6"]

def style_chart(fig, height=400):
    """Make every chart share one clean dark look."""
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", color="#e6e6e6", size=13),
                      margin=dict(l=10, r=10, t=50, b=10), height=height)
    return fig


def run_validation_if_needed() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    issues_file = OUTPUT_DIR / "measurement_qa_issues.csv"
    summary_file = OUTPUT_DIR / "measurement_readiness_summary.csv"
    if issues_file.exists() and summary_file.exists():
        return
    try:
        subprocess.run([sys.executable, str(BASE_DIR / "src" / "validate_measurement_plan.py")], check=True)
    except Exception as exc:
        st.warning(f"Validation output could not be generated automatically: {exc}")


def load_data():
    run_validation_if_needed()
    campaigns = pd.read_csv(DATA_DIR / "campaign_urls.csv")
    events = pd.read_csv(DATA_DIR / "ga4_event_taxonomy.csv")
    gtm = pd.read_csv(DATA_DIR / "gtm_trigger_plan.csv")
    issues = pd.read_csv(OUTPUT_DIR / "measurement_qa_issues.csv") if (OUTPUT_DIR / "measurement_qa_issues.csv").exists() else pd.DataFrame()
    summary = pd.read_csv(OUTPUT_DIR / "measurement_readiness_summary.csv") if (OUTPUT_DIR / "measurement_readiness_summary.csv").exists() else pd.DataFrame()
    return campaigns, events, gtm, issues, summary


campaigns, events, gtm, issues, summary = load_data()
summary_map = dict(zip(summary.get("metric", []), summary.get("value", [])))

# ---------- Hero ----------
st.markdown("""
<div style="background:linear-gradient(135deg,#0f172a 0%,#15213b 55%,#1e2a4a 100%);
            border:1px solid #2b3553;border-radius:18px;padding:26px 32px;margin-bottom:18px;">
  <span style="background:rgba(96,165,250,.15);color:#9db4ff;padding:4px 12px;border-radius:999px;
               font-size:12px;font-weight:600;letter-spacing:.06em;">📡 MEASUREMENT READINESS, BEFORE YOU SPEND</span>
  <h1 style="margin:14px 0 4px 0;font-size:38px;line-height:1.1;color:#fff;">
     GTM + GA4 <span style="color:#60a5fa;">Measurement Dashboard System</span></h1>
  <p style="color:#b9c0d8;font-size:15px;margin:0;max-width:980px;">
     UTM governance, GA4 event taxonomy, GTM trigger mapping, and conversion-tracking QA — so campaign data is trustworthy before the budget goes live.</p>
</div>
""", unsafe_allow_html=True)

# ---------- KPI cards ----------
metric_cols = st.columns(6)
metric_cols[0].metric("Readiness Score", f"{summary_map.get('Measurement Readiness Score', 0)}/100")
metric_cols[1].metric("Campaign URLs", int(summary_map.get("Campaign URLs Reviewed", 0)))
metric_cols[2].metric("GA4 Events", int(summary_map.get("GA4 Events Planned", 0)))
metric_cols[3].metric("Key Events", int(summary_map.get("Key Events Planned", 0)))
metric_cols[4].metric("GTM Tags", int(summary_map.get("GTM Tags Planned", 0)))
metric_cols[5].metric("QA Issues", int(summary_map.get("QA Issues Found", 0)))

st.divider()

tab_dashboard, tab_utm, tab_events, tab_gtm, tab_qa, tab_portfolio = st.tabs([
    "📊 Command Center", "🔗 UTM Governance", "📈 GA4 Event Taxonomy",
    "🏷️ GTM Trigger Plan", "✅ QA Output", "💼 Portfolio Summary",
])

with tab_dashboard:
    st.subheader("Measurement Command Center")
    c1, c2 = st.columns(2)
    with c1:
        issue_counts = issues.groupby(["severity"]).size().reset_index(name="count") if not issues.empty else pd.DataFrame({"severity": [], "count": []})
        fig = px.bar(issue_counts, x="severity", y="count", title="QA Issues by Severity", text="count",
                     color="severity", color_discrete_map=SEVERITY_COLORS)
        st.plotly_chart(style_chart(fig), use_container_width=True, config={"displayModeBar": False})
    with c2:
        event_counts = events.groupby(["funnel_stage", "is_key_event"]).size().reset_index(name="count")
        fig = px.bar(event_counts, x="funnel_stage", y="count", color="is_key_event", title="GA4 Events by Funnel Stage",
                     text="count", color_discrete_sequence=ACCENT)
        fig.update_layout(xaxis_title="Funnel Stage")
        st.plotly_chart(style_chart(fig), use_container_width=True, config={"displayModeBar": False})

    c3, c4 = st.columns(2)
    with c3:
        platform_counts = campaigns.groupby("platform").size().reset_index(name="campaign_urls")
        fig = px.pie(platform_counts, names="platform", values="campaign_urls", title="Campaign URLs by Platform",
                     hole=0.58, color_discrete_sequence=ACCENT)
        st.plotly_chart(style_chart(fig), use_container_width=True, config={"displayModeBar": False})
    with c4:
        qa_counts = gtm.groupby("qa_status").size().reset_index(name="tags")
        fig = px.pie(qa_counts, names="qa_status", values="tags", title="GTM QA Status",
                     hole=0.58, color_discrete_sequence=ACCENT)
        st.plotly_chart(style_chart(fig), use_container_width=True, config={"displayModeBar": False})

    st.info("**Operational meaning:** this confirms campaign URLs, website events, conversion events, and reporting fields are ready *before* money is spent on campaigns.")

with tab_utm:
    st.subheader("UTM Governance Review")
    st.write("Checks whether campaign URLs are clean enough for reporting in GA4, Looker Studio, CRM reports, and campaign dashboards.")
    st.dataframe(campaigns, use_container_width=True, hide_index=True)
    st.markdown("##### UTM Issues")
    utm_issues = issues[issues["section"] == "UTM Governance"] if not issues.empty else pd.DataFrame()
    st.dataframe(utm_issues, use_container_width=True, hide_index=True)

with tab_events:
    st.subheader("GA4 Event Taxonomy")
    st.write("Defines which website and CRM actions are tracked as GA4 events, and which become key events / conversions.")
    st.dataframe(events, use_container_width=True, hide_index=True)
    key_events = events[events["is_key_event"].str.lower() == "yes"]
    st.markdown("##### Planned Key Events / Conversions")
    st.dataframe(key_events[["event_name", "funnel_stage", "required_parameters", "business_question"]], use_container_width=True, hide_index=True)

with tab_gtm:
    st.subheader("GTM Trigger + Tag Plan")
    st.write("Maps business actions to GTM tags, triggers, trigger conditions, and GA4 event names.")
    st.dataframe(gtm, use_container_width=True, hide_index=True)
    st.markdown("##### Trigger QA Focus")
    st.dataframe(gtm[gtm["qa_status"].isin(["Needs QA", "Planned"])], use_container_width=True, hide_index=True)

with tab_qa:
    st.subheader("Measurement QA Output")
    st.write("The issues to fix before launching or scaling campaigns.")
    st.dataframe(issues, use_container_width=True, hide_index=True)
    if not issues.empty:
        st.download_button("Download QA Issues CSV", issues.to_csv(index=False),
                           file_name="measurement_qa_issues.csv", mime="text/csv")

with tab_portfolio:
    st.subheader("Portfolio / Interview Summary")
    st.markdown("""
**Project positioning:** a GTM + GA4 measurement-planning dashboard for lead-generation campaigns.

**What it demonstrates:**
- How campaign URLs are standardized using UTMs
- How GTM tags and triggers are planned before launch
- How GA4 events and key events map to business actions
- How QA checks catch missing UTMs, inconsistent naming, and untested conversion events
- How teams improve reporting reliability before campaign spend increases

**Resume bullet:** Built a Python + Streamlit GTM/GA4 measurement-planning dashboard to validate UTM governance, map GA4 event taxonomy, plan GTM triggers, detect tracking-QA gaps, and score campaign reporting readiness.
    """)
