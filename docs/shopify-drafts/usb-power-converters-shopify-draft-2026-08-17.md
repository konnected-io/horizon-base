# USB power converters Shopify draft

Status: Shopify CMS page published
Owner: Josh
Date: 2026-08-17

## Shopify draft

- Source review Doc: https://docs.google.com/document/d/1Nj0l2iJrEnC6OrcyOxTG2WbihI57288IYAYdiKaE9Vw/edit?usp=sharing
- Local source markdown: `content-engine/content/shopify-drafts/usb-c-pd-vs-12v-to-5v-usb-power-converter-shopify-page-draft-2026-08-12.md`
- Shopify page ID: `gid://shopify/Page/157383328059`
- Draft handle: `usb-c-pd-vs-12v-to-5v-usb-power-converter`
- Intended URL after publish: `/pages/usb-c-pd-vs-12v-to-5v-usb-power-converter`
- Live URL: https://konnected.io/pages/usb-c-pd-vs-12v-to-5v-usb-power-converter
- Published state: `isPublished: true`, `publishedAt: 2026-08-17T13:37:55Z`
- Template suffix: generic page template

## CMS vs theme decision

This is CMS body content, not a theme runtime change. The article body, comparison table, figures, FAQ content, and product CTAs live in the published Shopify page body. No one-off article copy, page-specific FAQ content, or page-specific schema was added to Liquid, JSON templates, sections, snippets, or theme assets.

## Nate comment fixes reconciled before Shopify Admin

- Clarified that most USB-C devices can run or charge from standard 5V USB, while USB-C PD usually charges compatible devices faster.
- Added the caveat that charging speed may matter less for permanently mounted devices that stay plugged in.
- Broadened the vehicle section beyond hardwired tablets to include fast USB-C charging from a vehicle's 12V system.
- Removed the comparison-table row that framed fixed 5V as a buyer mistake for USB-C devices.
- Added a physical-size comparison row: PD converter is the larger body; 12V-to-5V converter is the smaller body.
- Double-checked the fixed 5V converter input spec against the live product page and kept it as `12V DC`.

## Shopify Admin and live-page verification

Verified through Shopify Admin GraphQL on 2026-08-17:

- `id`: `gid://shopify/Page/157383328059`
- `title`: `USB-C PD vs 12V-to-5V USB power converters: which one do you need?`
- `handle`: `usb-c-pd-vs-12v-to-5v-usb-power-converter`
- `isPublished`: `true`
- `publishedAt`: `2026-08-17T13:37:55Z`
- `bodySummary` begins with the expected low-voltage DC-to-USB intro.
- Body HTML contains the expected comparison table, two product figures, product CTAs, FAQ section, and Nate-driven USB-C/5V charging-speed language.
- Public URL returned HTTP 200.
- Public HTML contains the expected title, Nate-driven USB-C/5V charging-speed language, physical-size comparison row, vehicle fast-charging section, and both product CTAs.

Shopify Admin GraphQL `PageCreateInput` and `PageUpdateInput` in API version `2026-04` do not expose an SEO title or description field. SEO metadata should be checked or set through the supported Shopify Admin surface before publish approval.

## Remaining follow-up gates

- Confirm or set the SEO title and meta description in the supported Admin surface.
- Decide whether any follow-up work should recreate this as a blog article instead of keeping the published evergreen page URL.
- Confirm final product/spec language for USB-C PD output behavior, fixed 5V input/output, Raspberry Pi caveat, Alarm Panel Pro AUX/PoE caveat, vehicle wiring safety, and solar/off-grid language.
- Add internal routing only after the live page URL is accepted as the canonical target.

## Post-publish plan

- Add the published URL to Published Monitor after it is live.
- Baseline GSC performance for the new URL and both converter product pages before publish or immediately after indexing.
- Recheck GSC, GA4 product referral behavior, and ChatGPT/OpenAI referral landing pages at 2, 4, and 8 weeks.
- Run AI visibility checks for PD-vs-5V, wall-tablet, vehicle/fleet, solar/off-grid, and Raspberry Pi prompts.
- Add one contextual support-article link from the high-impression USB cable article after publish approval.
- Track whether AI citations move from scattered support/product pages toward the canonical guide.

## CTA tracking added in this PR

`assets/custom.js` now auto-tags product links on `/pages/usb-c-pd-vs-12v-to-5v-usb-power-converter` for `content_cta_click` reporting:

- USB-C PD product destination: `/products/usb-pd-type-c-dc-fast-charge-power-converter`
- 12V-to-5V USB product destination: `/products/12v-to-5v-usb-power-converter`
- `content_slug`: `usb-c-pd-vs-12v-to-5v-usb-power-converter`
- `content_cluster`: `power_accessories`
- `destination_type`: `product`
- `cta_location`: `comparison_table` for links inside the comparison table, `inline_answer` for other matching product links.
