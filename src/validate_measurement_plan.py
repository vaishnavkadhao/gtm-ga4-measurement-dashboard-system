from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "sample-data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_SOURCES = {"google", "meta", "facebook", "instagram", "linkedin", "email"}
ALLOWED_MEDIUMS = {"cpc", "paid_social", "email", "organic", "referral"}
REQUIRED_UTM_FIELDS = ["utm_source", "utm_medium", "utm_campaign", "utm_content"]


def has_bad_naming(value: str) -> bool:
    if pd.isna(value) or not str(value).strip():
        return True
    value = str(value).strip()
    return bool(re.search(r"\s", value)) or value != value.lower()


def validate_campaign_urls(campaigns: pd.DataFrame) -> pd.DataFrame:
    issues = []
    for _, row in campaigns.iterrows():
        campaign_id = row.get("campaign_id", "unknown")
        platform = row.get("platform", "unknown")
        campaign_name = row.get("campaign_name", "unknown")

        for field in REQUIRED_UTM_FIELDS:
            value = str(row.get(field, "")).strip()
            if not value or value.lower() == "nan":
                issues.append({
                    "section": "UTM Governance",
                    "severity": "High",
                    "campaign_id": campaign_id,
                    "platform": platform,
                    "campaign_name": campaign_name,
                    "issue": f"Missing required field: {field}",
                    "recommended_fix": f"Add a clean {field} value before launching the campaign.",
                })

        source = str(row.get("utm_source", "")).strip().lower()
        medium = str(row.get("utm_medium", "")).strip().lower()
        if source and source not in ALLOWED_SOURCES:
            issues.append({
                "section": "UTM Governance",
                "severity": "Medium",
                "campaign_id": campaign_id,
                "platform": platform,
                "campaign_name": campaign_name,
                "issue": f"Non-standard utm_source: {source}",
                "recommended_fix": "Use approved source names such as google, meta, linkedin, or email.",
            })
        if medium and medium not in ALLOWED_MEDIUMS:
            issues.append({
                "section": "UTM Governance",
                "severity": "Medium",
                "campaign_id": campaign_id,
                "platform": platform,
                "campaign_name": campaign_name,
                "issue": f"Non-standard utm_medium: {medium}",
                "recommended_fix": "Use approved medium names such as cpc, paid_social, email, organic, or referral.",
            })

        for field in ["utm_campaign", "utm_content", "utm_term"]:
            value = str(row.get(field, "")).strip()
            if value and value.lower() != "nan" and has_bad_naming(value):
                issues.append({
                    "section": "UTM Governance",
                    "severity": "Low",
                    "campaign_id": campaign_id,
                    "platform": platform,
                    "campaign_name": campaign_name,
                    "issue": f"Naming format issue in {field}: {value}",
                    "recommended_fix": "Use lowercase snake_case naming without spaces for clean reporting.",
                })
    return pd.DataFrame(issues)


def validate_event_taxonomy(events: pd.DataFrame) -> pd.DataFrame:
    issues = []
    duplicate_events = events[events.duplicated("event_name", keep=False)]
    for _, row in duplicate_events.iterrows():
        issues.append({
            "section": "GA4 Event Taxonomy",
            "severity": "High",
            "campaign_id": "N/A",
            "platform": "GA4",
            "campaign_name": row["event_name"],
            "issue": "Duplicate GA4 event name",
            "recommended_fix": "Keep event names unique and clearly mapped to a single business action.",
        })

    for _, row in events.iterrows():
        required_params = str(row.get("required_parameters", "")).strip()
        if not required_params or required_params.lower() == "nan":
            issues.append({
                "section": "GA4 Event Taxonomy",
                "severity": "Medium",
                "campaign_id": "N/A",
                "platform": "GA4",
                "campaign_name": row.get("event_name", "unknown"),
                "issue": "Missing required parameter list",
                "recommended_fix": "Define required parameters so reports can be segmented correctly.",
            })
    return pd.DataFrame(issues)


def validate_gtm_plan(gtm: pd.DataFrame) -> pd.DataFrame:
    issues = []
    for _, row in gtm.iterrows():
        qa_status = str(row.get("qa_status", "")).strip().lower()
        priority = str(row.get("priority", "")).strip()
        if qa_status in {"needs qa", "planned"}:
            issues.append({
                "section": "GTM Trigger Plan",
                "severity": "High" if priority == "High" else "Medium",
                "campaign_id": "N/A",
                "platform": "GTM",
                "campaign_name": row.get("tag_name", "unknown"),
                "issue": f"Tag not fully QA-ready: {row.get('qa_status')}",
                "recommended_fix": "Test this tag in GTM Preview Mode and confirm event appears in GA4 DebugView before launch.",
            })
    return pd.DataFrame(issues)


def main() -> None:
    campaigns = pd.read_csv(DATA_DIR / "campaign_urls.csv")
    events = pd.read_csv(DATA_DIR / "ga4_event_taxonomy.csv")
    gtm = pd.read_csv(DATA_DIR / "gtm_trigger_plan.csv")

    issues = pd.concat([
        validate_campaign_urls(campaigns),
        validate_event_taxonomy(events),
        validate_gtm_plan(gtm),
    ], ignore_index=True)

    readiness_score = max(0, 100 - (len(issues[issues["severity"] == "High"]) * 8) - (len(issues[issues["severity"] == "Medium"]) * 4) - (len(issues[issues["severity"] == "Low"]) * 2))

    summary = pd.DataFrame([
        {"metric": "Campaign URLs Reviewed", "value": len(campaigns)},
        {"metric": "GA4 Events Planned", "value": len(events)},
        {"metric": "Key Events Planned", "value": len(events[events["is_key_event"].str.lower() == "yes"])},
        {"metric": "GTM Tags Planned", "value": len(gtm)},
        {"metric": "QA Issues Found", "value": len(issues)},
        {"metric": "Measurement Readiness Score", "value": readiness_score},
    ])

    issues.to_csv(OUTPUT_DIR / "measurement_qa_issues.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "measurement_readiness_summary.csv", index=False)

    print("Measurement validation completed successfully.")
    print(f"QA issues: {len(issues)}")
    print(f"Readiness score: {readiness_score}/100")
    print(f"Outputs saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
