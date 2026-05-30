# GTM + GA4 Measurement Blueprint

## Purpose

This document explains how campaign traffic, landing page actions, GTM triggers, GA4 events, and dashboard reporting connect together.

## Step 1: Campaign URL Planning

Every paid or owned campaign URL should include clean UTM parameters:

- `utm_source` — traffic source such as google, meta, linkedin, email
- `utm_medium` — traffic medium such as cpc, paid_social, email
- `utm_campaign` — campaign name in lowercase snake_case
- `utm_content` — creative/ad variation
- `utm_term` — keyword, audience, or targeting group

## Step 2: Landing Page Actions

The website should track actions that show user intent:

- Page view
- Scroll depth
- CTA click
- Call click
- WhatsApp click
- Form start
- Form submit
- Thank-you page view

## Step 3: GTM Planning

GTM is used to fire tags when a specific trigger condition is met.

Example:

- Trigger: Click URL contains `tel:`
- Tag: GA4 Event - Call Click
- GA4 Event Name: `call_click`

## Step 4: GA4 Event Taxonomy

Each event should have:

- Event name
- Funnel stage
- Required parameters
- Whether it is a key event
- Business question it answers

## Step 5: Key Event Planning

Events that represent business outcomes should be marked as key events/conversions:

- call_click
- whatsapp_click
- form_submit
- thank_you_view
- qualified_lead
- booking_confirmed

## Step 6: QA Before Launch

Before launching campaigns, confirm:

- UTMs are present
- Event names are consistent
- GTM triggers fire correctly
- GA4 DebugView receives events
- Key events are configured
- Reports show source, medium, campaign, content, and term

## Step 7: Dashboard Reporting

Dashboard should show:

- Campaign traffic by source and medium
- Event volume by funnel stage
- Key events/conversions
- Tracking issues
- Landing page performance
- Campaign readiness score

## Summary

This process helps prevent wasted campaign spend caused by broken tracking, poor naming, missing conversions, and weak reporting visibility.
