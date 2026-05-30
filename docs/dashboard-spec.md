# Dashboard Specification

## Dashboard Name

GTM + GA4 Measurement Dashboard System

## User Persona

- Performance marketing executive
- Campaign analyst
- Marketing operations executive
- Digital marketing manager
- Founder or small business owner reviewing campaign tracking readiness

## Main Dashboard Sections

### 1. Measurement Command Center

Purpose: Give a quick overview of whether the measurement system is ready.

Cards:

- Readiness Score
- Campaign URLs Reviewed
- GA4 Events Planned
- Key Events Planned
- GTM Tags Planned
- QA Issues Found

### 2. UTM Governance

Purpose: Validate whether campaign URLs can be used for clean reporting.

Checks:

- Missing source
- Missing medium
- Missing campaign
- Missing content
- Non-standard source
- Non-standard medium
- Spaces or capital letters in campaign values

### 3. GA4 Event Taxonomy

Purpose: Define what events need to be tracked.

Fields:

- Event name
- Event category
- Funnel stage
- Key event status
- Required parameters
- Business question
- Success condition
- Owner

### 4. GTM Trigger Plan

Purpose: Map business actions to GTM triggers and GA4 event tags.

Fields:

- Tag name
- Tag type
- Trigger name
- Trigger type
- Trigger condition
- GA4 event name
- QA status
- Priority
- Notes

### 5. QA Output

Purpose: Show what must be fixed before campaigns go live.

Fields:

- Section
- Severity
- Platform
- Campaign / tag / event
- Issue
- Recommended fix

## Suggested Future Improvements

- Add upload option for real campaign URL sheets
- Add automated UTM builder
- Add GA4 event naming validation rules
- Add Looker Studio dashboard mockup
- Add CRM lead quality mapping
- Add PDF report export
