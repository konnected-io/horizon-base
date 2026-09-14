# SmartThings automation ideas published Shopify page

Status: Shopify CMS page published
Owner: Josh
Date: 2026-09-14

## Shopify page

- Source review Doc: https://docs.google.com/document/d/1qmvXF7UMtIPkrkpBXhKlXULIBX4ePwZIK4IwAKVmOU4/edit
- Local source Markdown: `content-engine/content/shopify-drafts/smartthings-automation-ideas-konnected-shopify-page-draft-2026-08-20.md`
- Shopify page ID: `gid://shopify/Page/157659627835`
- Handle: `smartthings-automation-ideas-konnected`
- Live URL: https://konnected.io/pages/smartthings-automation-ideas-konnected
- Published state: `isPublished: true`, `publishedAt: 2026-09-14T18:20:10Z`
- Template suffix: generic page template

## CMS vs theme decision

The article body, figures, FAQ copy, and FAQPage JSON-LD live in Shopify CMS. No one-off article copy or page-specific schema is duplicated in theme code.

This PR only adds CTA measurement for the article's owned footer routes and records the post-publish discovery plan.

## Nate feedback reconciliation

The canonical content job records seven Nate comments as reviewed and reconciled before publication. The resulting Markdown and Shopify page preserve the approved boundaries for Konnected Cloud, GDO product compatibility, Security+ 3.0, hub requirements, professional monitoring, life-safety use, and Standalone Alarm System scope.

## Publication verification

- Shopify Admin returned the expected ID, title, handle, generic template, `isPublished: true`, and publication timestamp.
- The public URL returned HTTP 200 after publication.
- Public HTML contains the approved page title, Security+ 3.0 caveat, and FAQPage JSON-LD.
- The live Shopify body matches the reconciled canonical Markdown in substance.

## Post-publish plan

1. Track the live page in Published Monitor without overwriting existing CTA or revenue fields.
2. Baseline page-level GSC and GA4 after indexing, then review at 2, 4, and 8 weeks.
3. Measure article-footer clicks to the SmartThings integration page, Smart Garage Door Openers collection, and Smart Alarm Panels collection using `content_cta_click`.
4. Run AI visibility checks for wired SmartThings sensors, SmartThings Home Monitor, Konnected garage-door routines, SmartThings hub requirements, and local-vs-cloud questions.
5. After Nate approves the direction, run the internal-linking pass and prioritize one contextual link from `/pages/smartthings`; consider collection or product placements only where the existing module supports useful buyer routing.
6. Verify sitemap/canonical/indexability and inspect whether AI citations and organic traffic consolidate on this guide rather than less-specific pages.

## CTA tracking in this PR

`assets/custom.js` tags the three owned footer links on `/pages/smartthings-automation-ideas-konnected`:

- `content_slug`: `smartthings-automation-ideas-konnected`
- `content_cluster`: `platform_integrations`
- `cta_location`: `article_footer`
- Destination types: `integration_page` and `collection`

The external Konnected Cloud setup link remains untagged because the current route-level implementation is scoped to owned-site buyer journeys.
