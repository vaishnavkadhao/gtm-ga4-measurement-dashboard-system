# GTM + GA4 Pre-Launch QA Checklist

## UTM QA

- [ ] Every campaign URL has `utm_source`
- [ ] Every campaign URL has `utm_medium`
- [ ] Every campaign URL has `utm_campaign`
- [ ] Every campaign URL has `utm_content`
- [ ] UTM values use lowercase naming
- [ ] UTM values do not contain spaces
- [ ] Source and medium values follow approved naming rules

## GTM QA

- [ ] GA4 configuration tag fires on all pages
- [ ] CTA click trigger fires only on correct buttons
- [ ] Phone click trigger fires on `tel:` links
- [ ] WhatsApp trigger fires on WhatsApp links
- [ ] Form start event fires once per form attempt
- [ ] Form submit event fires after successful submit
- [ ] Thank-you page event fires only on thank-you page

## GA4 QA

- [ ] Events appear in GA4 DebugView
- [ ] Event names match taxonomy
- [ ] Required parameters are visible in GA4
- [ ] Key events are marked correctly
- [ ] Source / medium / campaign values appear in reports
- [ ] Duplicate events are not firing

## CRM / Lead Quality QA

- [ ] Lead source is captured in CRM
- [ ] Campaign name is passed into CRM
- [ ] Lead quality status is defined
- [ ] Qualified lead feedback can be mapped back to campaign
- [ ] Meeting booked / deal won status can be connected later

## Launch Decision

Launch only when:

- No high-severity tracking issue is open
- Primary conversion events are working
- Campaign URLs are clean
- GA4 DebugView confirms events
- Dashboard can show campaign source and conversion performance
