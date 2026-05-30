from pathlib import Path
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sample-data"
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(
    page_title="GTM + GA4 Measurement Dashboard",
    page_icon="📡",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #0b0f17; }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #111827, #0f172a);
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 18px;
        border-radius: 18px;
    }
    .hero {
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(96, 165, 250, 0.35);
        background: linear-gradient(135deg, #0f172a, #111827);
        margin-bottom: 24px;
    }
    .pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(96, 165, 250, 0.35);
        margin-right: 8px;
        margin-top: 8px;
        color: #bfdbfe;
        font-size: 13px;
    }
    .callout {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(34, 197, 94, 0.35);
        background: rgba(34, 197, 94, 0.08);
        margin: 12px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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

st.markdown(
    """
    <div class="hero">
      <h1>📡 GTM + GA4 Measurement Dashboard System</h1>
      <p style="color:#cbd5e1; font-size:17px; max-width:980px;">
      A portfolio web app for UTM governance, GA4 event taxonomy planning, GTM trigger mapping, conversion tracking QA, and campaign reporting readiness.
      </p>
      <span class="pill">GTM planning</span>
      <span class="pill">GA4 events</span>
      <span class="pill">UTM governance</span>
      <span class="pill">Conversion QA</span>
      <span class="pill">Python + Streamlit</span>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(6)
metric_cols[0].metric("Readiness Score", f"{summary_map.get('Measurement Readiness Score', 0)}/100")
metric_cols[1].metric("Campaign URLs", int(summary_map.get("Campaign URLs Reviewed", 0)))
metric_cols[2].metric("GA4 Events", int(summary_map.get("GA4 Events Planned", 0)))
metric_cols[3].metric("Key Events", int(summary_map.get("Key Events Planned", 0)))
metric_cols[4].metric("GTM Tags", int(summary_map.get("GTM Tags Planned", 0)))
metric_cols[5].metric("QA Issues", int(summary_map.get("QA Issues Found", 0)))

st.divider()

tab_dashboard, tab_utm, tab_events, tab_gtm, tab_qa, tab_portfolio = st.tabs([
    "📊 Command Center",
    "🔗 UTM Governance",
    "📈 GA4 Event Taxonomy",
    "🏷️ GTM Trigger Plan",
    "✅ QA Output",
    "💼 Portfolio Summary",
])

with tab_dashboard:
    st.subheader("Measurement Command Center")
    c1, c2 = st.columns(2)
    with c1:
        issue_counts = issues.groupby(["severity"]).size().reset_index(name="count") if not issues.empty else pd.DataFrame({"severity": [], "count": []})
        fig = px.bar(issue_counts, x="severity", y="count", title="QA Issues by Severity", text="count", color="severity")
        fig.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        event_counts = events.groupby(["funnel_stage", "is_key_event"]).size().reset_index(name="count")
        fig = px.bar(event_counts, x="funnel_stage", y="count", color="is_key_event", title="GA4 Events by Funnel Stage", text="count")
        fig.update_layout(template="plotly_dark", height=420, xaxis_title="Funnel Stage")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        platform_counts = campaigns.groupby("platform").size().reset_index(name="campaign_urls")
        fig = px.pie(platform_counts, names="platform", values="campaign_urls", title="Campaign URLs by Platform", hole=0.55)
        fig.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        qa_counts = gtm.groupby("qa_status").size().reset_index(name="tags")
        fig = px.pie(qa_counts, names="qa_status", values="tags", title="GTM QA Status", hole=0.55)
        fig.update_layout(template="plotly_dark", height=420)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="callout">
    <b>Operational meaning:</b> This dashboard helps a marketer confirm whether campaign URLs, website events, conversion events, and reporting fields are ready before spending money on campaigns.
    </div>
    """, unsafe_allow_html=True)

with tab_utm:
    st.subheader("UTM Governance Review")
    st.write("This section checks whether campaign URLs are clean enough for reporting in GA4, Looker Studio, CRM reports, and campaign dashboards.")
    st.dataframe(campaigns, use_container_width=True, hide_index=True)
    st.markdown("### UTM Issues")
    utm_issues = issues[issues["section"] == "UTM Governance"] if not issues.empty else pd.DataFrame()
    st.dataframe(utm_issues, use_container_width=True, hide_index=True)

with tab_events:
    st.subheader("GA4 Event Taxonomy")
    st.write("This section defines which website and CRM actions should be tracked as GA4 events and which should become key events/conversions.")
    st.dataframe(events, use_container_width=True, hide_index=True)
    key_events = events[events["is_key_event"].str.lower() == "yes"]
    st.markdown("### Planned Key Events / Conversions")
    st.dataframe(key_events[["event_name", "funnel_stage", "required_parameters", "business_question"]], use_container_width=True, hide_index=True)

with tab_gtm:
    st.subheader("GTM Trigger + Tag Plan")
    st.write("This section maps business actions to GTM tags, triggers, trigger conditions, and GA4 event names.")
    st.dataframe(gtm, use_container_width=True, hide_index=True)
    st.markdown("### Trigger QA Focus")
    st.dataframe(gtm[gtm["qa_status"].isin(["Needs QA", "Planned"])], use_container_width=True, hide_index=True)

with tab_qa:
    st.subheader("Measurement QA Output")
    st.write("These are the issues that should be fixed before launching or scaling campaigns.")
    st.dataframe(issues, use_container_width=True, hide_index=True)
    if not issues.empty:
        st.download_button(
            "Download QA Issues CSV",
            issues.to_csv(index=False),
            file_name="measurement_qa_issues.csv",
            mime="text/csv",
        )

with tab_portfolio:
    st.subheader("Portfolio / Interview Summary")
    st.markdown("""
    **Project positioning:** Built a GTM + GA4 measurement planning dashboard for lead-generation campaigns.

    **What the project demonstrates:**
    - How campaign URLs are standardized using UTMs
    - How GTM tags and triggers are planned before launch
    - How GA4 events and key events are mapped to business actions
    - How QA checks catch missing UTMs, inconsistent naming, and untested conversion events
    - How marketing teams can improve reporting reliability before campaign spend increases

    **Resume bullet:**
    Built a Python and Streamlit-based GTM + GA4 measurement planning dashboard to validate UTM governance, map GA4 event taxonomy, plan GTM triggers, detect tracking QA gaps, and score campaign reporting readiness for lead-generation campaigns.
    """)
