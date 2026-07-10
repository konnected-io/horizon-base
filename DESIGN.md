# Konnected Storefront Design Language — "Bright Signal"

**Status:** shipped to branch `visual-refresh-2026` (2026-07-09), verified on `shopify theme dev`, theme check clean. Not yet merged or pushed to the live theme.
**Scope of the refresh:** homepage, `/collections/smart-alarm-panels`, `/collections/smart-garage-door-openers`. Global styles propagate elsewhere by design.
**Companion:** the [Konnected Design System](https://claude.ai/design/p/8f9bfe39-2982-413d-803d-68aaf3d2e15d) on claude.ai/design — its `readme.md`, `tokens/colors.css`, and the two *Storefront* guideline cards were reconciled with this document on 2026-07-09. Where the two disagree, whatever is **shipping on the storefront** wins for marketing surfaces, and this file is the arbiter.

---

## 1. Direction

**"Bright Signal" (Direction B).** Light, airy, trust-first surfaces with tech-forward depth from brand-geometry texture, not darkness. Chosen over a dark "Midnight Circuit" hero direction because light reads more trustworthy for this audience.

Design dials (from the tasteskill framework):

| Dial | Value | Meaning here |
|---|---|---|
| DESIGN_VARIANCE | 5–6 | Left-aligned headlines, asymmetric header (headline + proof column), equal-card duos. No perfect centering everywhere, no chaos. |
| MOTION_INTENSITY | 3–4 | Fluid CSS transitions, one rotator, reveal-on-scroll. No scroll hijacks, parallax, or loops. |
| VISUAL_DENSITY | 4 | Fewer boxes, more whitespace; cards only where elevation means something. |

**Theme lock: light.** Marketing pages never flip to dark sections. Bold moments use texture, midnight ink, or full-bleed blue — not black panels.

---

## 2. Tokens

Single source of truth: the theme editor's **color palette** (`config/settings_data.json` → `color_palette`), surfaced as CSS custom properties by `snippets/custom-palette-vars.liquid`. Never hardcode a hex in `custom.css` when a palette var exists.

### 2.1 Color roles (marketing surfaces)

| Token | Hex | Var | Role |
|---|---|---|---|
| Konnected Blue | `#3f75ff` | `--color-primary` | The single accent: primary CTAs, links, fit labels, stat rules, the one headline emphasis phrase |
| Midnight Blue | `#203074` | `--color-midnight` | Stat numerals, compare-table headers, card-shadow tint |
| Electric Cyan | `#22beff` | `--color-electric-cyan` | Ring texture only. Never text, never UI |
| Circuit Green | `#47f5a3` | `--color-circuit-green` | **Reserved: the header "Shop Now" pill and nothing else.** Ink text on it (contrast ≈ 10:1) |
| Brand Tint | `#eef4f9` | `--color-brand-tint` | Hero gradient floor, tint panels |
| Foreground | `#121212` | `--color-foreground` | Ink. Secondary text via `rgb(var(--color-foreground-rgb) / .6–.75)` |
| Border | `#e5e7eb` | `--color-border` | Hairlines |
| Stars | `#f5b423` | (literal) | Review stars only |
| Slate ✗ | `#9aa4b8` | (literal) | Compare-table "no" marks. **Never red** — red reads as alarm and is reserved for genuine danger states |

### 2.2 Type

- **Headings:** `basic-sans` 600 (Adobe Typekit kit `hzh6fgx`, forced in `custom.css`), tight tracking (−0.015em on display sizes).
- **Body:** Inter 400, 16px base, relaxed line-height (1.55–1.6).
- **Emphasis rules:** one blue emphasis phrase per page (`em` styled solid blue, not italic); keyword bolds in subtext (same family, weight 600, ink color). Never mixed-family emphasis, never italics-as-decoration.
- Hero display size: `clamp(2rem, 1.15rem + 2.3vw, 2.85rem)`; collection h1s share it.

### 2.3 Shape

- **Buttons:** full pill (theme setting, 30px radius) — unchanged brand mechanic.
- **Chooser cards (`k-line-card`):** 20px radius, 1px `--color-border` hairline.
- **Stock Horizon cards elsewhere:** 4px (theme setting) — pre-existing, untouched.
- Documented rule: pills = interactive, 20px = hero/chooser cards, 4px = stock product cards. This is a context split, not drift.

### 2.4 Elevation

- Card resting: `0 20px 44px rgb(var(--color-midnight-rgb) / .07)`
- Card hover: `translateY(-4px)` + `0 30px 60px rgb(... / .12)`
- Product cutout images: `filter: drop-shadow(0 14px 22px rgb(... / .14))`
- Shadows are always midnight-tinted. No pure-black shadows, no glows.

### 2.5 The ring texture (signature backdrop)

Ring arcs echoing the circuit-chip "O" logo + cyan/blue radial washes over a white→tint gradient. Pure CSS, zero image assets, shipped as section-scoped `custom_css` on `.section-background`:

```css
background:
  radial-gradient(circle 240px at 91% -70px, transparent 58%, rgba(34,190,255,.26) 60%, rgba(63,117,255,.15) 74%, transparent 76%),
  radial-gradient(circle 260px at 3% 108%, transparent 60%, rgba(63,117,255,.18) 62%, rgba(34,190,255,.09) 76%, transparent 78%),
  radial-gradient(640px 420px at 88% -10%, rgba(34,190,255,.12), transparent 65%),
  linear-gradient(180deg, #ffffff 0%, #eef4f9 100%);
```

Use on hero/heading sections only. Body sections stay clean. Derived from the brand's blog/email banner art (rings + gradient swooshes).

---

## 3. Component language (`k-*` in `assets/custom.css`)

All custom markup lives in **template-JSON `custom-liquid` sections** (precedent: the alarm retrofit chooser). No upstream Liquid was modified.

### 3.1 `k-hero` — the hero pattern
- **Homepage:** left column = headline + subtext; right column = boxless social proof separated by a hairline (stars → quote rotator → official works-with badges); below = the dual-line duo.
- **Collections (`k-hero--collection`):** breadcrumbs → h1 (SEO heading preserved verbatim) → subtext → two-kit duo.
- Hero must fit the desktop fold with CTAs visible.

### 3.2 `k-line-card` — chooser cards
Content order: clickable product image (`k-line-card__media-link`, `tabindex="-1"` + `aria-hidden` to avoid duplicate tab stops) → blue **fit label** ("Best for…") → title → one-liner → row of pill CTA + **decision note**.
- **Dual-line parity rule:** when both product lines share a surface, cards are equal — same size, same CTA weight. Never primary-vs-ghost between product lines.
- **Decision notes carry the tradeoff** ("Keypads retire, the app takes over" / "Keypads and monitoring stay" / "The myQ alternative" / "The universal option").
- **CTA discipline:** labels are distinct and destination-specific; button text never wraps.
- Image size caps: 185px desktop (165px for the alarm board, ~10% smaller for visual parity), 150/135px mobile.

### 3.3 `k-quote-rotator` — social proof
Real, named customer quotes only (sourced from the existing testimonial carousel / Okendo). 5s interval, crossfade + rise, 0.35s entry delay so quotes never overlap; static first quote under `prefers-reduced-motion`. Boxless: sits directly on the hero texture behind a hairline.

### 3.4 `k-stats` — stat strip
Border-top 3px blue, midnight numeral (basic-sans 600), muted label. Replaces outline stat cards. Numbers must be real (currently: 9 integrations, $780, +25k, 60+, ~1hr).

### 3.5 `k-crumbs` — breadcrumbs
`Home › {Collection}` in quiet gray, blue hover, `nav[aria-label="Breadcrumb"]` + `aria-current="page"`, plus `BreadcrumbList` JSON-LD. Horizon has no native breadcrumb component; this is ours.

### 3.6 Header Shop Now
Circuit green pill via the existing `_header-button` block settings (`#47f5a3` bg / `#121212` text). The block's class-concatenation bug that hid this styling was fixed in `b3f151b`. Green appears nowhere else.

### 3.7 `k-intro` — homepage intro pair (what / who / why per product line)
Replaced the "Two upgrades, one app" chip panels (`k-duo-detail`/`k-chip`, retired 2026-07-10). Two mirrored sections, one per product line, each an x-ray split: media on one side, h2 + what-it-does lede + three who-is-this-for rows on the other. Rows are boxless with midnight hairline tops; each is a blue fit *question* (h3, body family 600) + plain answer. No CTA by design (hero above and quiz below carry the clicks).
- **`custom_what_lines`** — alarm/sensors angle ("There's a smart home hiding in your walls."): house-cutaway art (`02166205cdfec617ba45c6979d68e164.png`, 1200×1010, Shopify Files) left, text right. Illustrated cutouts stay boxless.
- **`custom_intro_gdo`** — garage angle ("The biggest door in your house shouldn't be the dumbest."): `k-intro--flip` mirrors the grid (text left, media right, desktop-only via `min-width: 900px`); media is `Rectangle_585_2.jpg` (device pinched in a hand) with the `k-intro__img--photo` chip treatment (20px radius, hairline, midnight shadow) — photographs get the chip, illustrations don't.
Grid areas `media/head/fits` collapse to `head → media → fits` under 900px. Fit rows stagger 0.1s/0.2s via `k-reveal`, gated on reduced motion. Adjacent padding between the pair is 32/32.

### 3.8 Compare tables
Stock AI-gen table block restyled **via its own settings** (template JSON): midnight header, white text, blue ✓, slate ✗.

---

## 4. Motion principles

1. **Motivated only** — hierarchy, feedback, or storytelling; nothing decorative-for-its-own-sake.
2. `transform` + `opacity` only. Easing `cubic-bezier(0.16, 1, 0.3, 1)`.
3. Reveal-on-scroll: IntersectionObserver in `custom.js`, applied only to elements starting below the fold (no flash, no CLS), fires once, 700ms fade + 14px rise.
4. Hover: card lift −4px / 250ms; button press scale 0.98.
5. **Everything beyond hover is disabled under `prefers-reduced-motion`.**
6. No `window scroll` listeners in new code, no scroll hijack, no parallax, no infinite loops, no autoplay carousels for static content.

---

## 5. Copy rules

- Voice unchanged: confident, plain-spoken, second person, platform- and product-named. ("Breathe new life into the wiring your home already has.")
- **Zero em-dashes** in marketing copy (one legacy em-dash survives inside the GDO safety warning; safety copy is frozen without explicit approval).
- Fit labels answer "who is this for"; decision notes answer "what's the tradeoff".
- No eyebrows/kickers on light surfaces; the headline carries the section.
- Quotes are verbatim excerpts from real named customers, ≤3 lines.

---

## 6. Implementation map (the Shopify way)

| Concern | Where it lives |
|---|---|
| Hero/stats/chooser markup | `templates/index.json` (`custom_hero_duo`, `custom_stats`), `templates/collection.*.json` (`custom_hero_collection`) as `custom-liquid` sections |
| `k-*` styles | end of `assets/custom.css` (banner-commented block) |
| Rotator + reveal JS | end of `assets/custom.js` (module, loads `fetchpriority=low`) |
| Palette custom properties | `snippets/custom-palette-vars.liquid` (single source: theme color palette) |
| Ring texture | per-section `custom_css` arrays in template JSON |
| Compare table colors | block settings in template JSON |
| Header CTA | `sections/header-group.json` settings + `blocks/_header-button.liquid` (Konnected-owned block) |

**Constraints honored:** no upstream (Shopify/horizon) files modified; no new CSS frameworks; no `!important` in new CSS; theme check must exit 0; URLs, nav labels, form fields, logo, legal/safety copy unchanged.

**Images** are referenced with `{{ 'file.png' | file_img_url: '900x' }}` from Shopify Files — new imagery must be uploaded to Files (admin), not the theme.

---

## 7. Gaps, weaknesses, honest notes

1. **Dark-blue split.** Brand guide says Deep Navy `#00263D`; the storefront palette ships Midnight `#203074`. Both are "the dark blue" in their own context. Needs a brand decision, then a palette/DS update. *(Flagged in the design system's Caveats too.)*
2. **Two Typekit kits.** The DS imports kit `zoq0xkd`; the theme links `hzh6fgx`. Both serve basic-sans. Consolidate to one Adobe Fonts project to avoid divergent weights/licensing.
3. **Quiz sections still use the stock "woman with phone" composite** (homepage + both collections). The hero refresh removed the worst offenders, but this banner art needs a real replacement (product-collage on tint + rings would fit the language). Blocked on new art.
4. **Logo strip is incomplete.** HomeSeer and josh.ai have no logo assets on the CDN; they were dropped from the implementation (mockup used text wordmarks). Needs official SVGs uploaded to Files, then two image blocks added to the logo grid sections.
5. **Legacy sections not yet in the language:** homepage testimonial card carousel (now redundant with the hero rotator — candidate for removal or restyle), "What They Do" / feature grid sections, YouTube embeds section, "Buy with confidence" 4-up cards, icon-card feature carousels on collections (still carousels), footer (still flat `#3f75ff`; consider midnight or tint treatment).
6. **Product pages untouched.** The two GDO and two alarm product templates still carry the old visual language (plus they got only the typo fix). Same for `/pages/*` platform pages, cart, about.
7. **Collection split-card inner boxes.** The old split-showcase text blocks kept subtle white background chips inside the new hero cards on collections... actually those sections were fully replaced; but the *product grid* cards and mid-page sections still show the stock 4px card look next to 20px k-cards. Acceptable, but worth a pass.
8. **No `og:image`** on collection pages (admin task: set social share images).
9. **Homepage `h1` is still "Konnected"** (from the header logo on index). The hero headline is an `h2` to avoid double-h1. Fixing properly means an upstream-ish header change or accepting it. Low SEO priority but noted.
10. **CWV not measured.** The hero images now load with explicit sizes + `fetchpriority`, and reveal avoids CLS, but no Lighthouse run has been done on the branch. Do one before merge.
11. **Cookie banner / widget pile-up** (black bar, clipped yellow button, "Ask me anything" pill, back-to-top all stacked bottom-right) is untouched — third-party apps, needs its own pass.
12. **DS marketing ui_kit/template are stale.** `ui_kits/marketing` and `templates/marketing-site` in the claude.ai design system still recreate the *old* homepage. The Storefront guideline cards are authoritative until those are rebuilt.
13. **`k-*` patterns exist only as Liquid/CSS.** The DS component library (JSX) has no `KitChooserCard`, `QuoteRotator`, `StatStrip`, or `Breadcrumbs` equivalents yet.

---

## 8. TODO / next steps (prioritized)

**Before merge**
- [ ] Lighthouse run on the three pages (LCP < 2.5s, CLS < 0.1); fix anything red.
- [ ] Cross-browser spot check (Safari especially, for `radial-gradient` ring rendering and `:has()` usages already in custom.css).
- [ ] Real-device mobile pass (rotator timing, tap targets, card image sizes).
- [ ] Open PR against `konnected-io/horizon-base` `main` (never bare `gh pr create` — the upstream remote points at Shopify/horizon). Flag "visually verified on dev; theme check clean" in the description.

**Content/asset asks (Nate)**
- [ ] Upload HomeSeer + josh.ai official logos to Shopify Files → extend logo strips.
- [ ] New quiz-banner art (or approve a CSS/product-collage replacement).
- [ ] Set `og:image` for both collections in admin.
- [ ] Decide: Deep Navy vs Midnight as *the* dark blue.
- [ ] Consolidate Typekit kits (`zoq0xkd` vs `hzh6fgx`).

**Next design passes**
- [ ] Retire/restyle the homepage testimonial carousel (redundant with hero rotator).
- [ ] Convert collection icon-card carousels to static grids in the k-language.
- [ ] Footer treatment pass (midnight or tint; current flat blue predates the refresh).
- [ ] Product-page templates in the new language (hero, spec presentation, compare modules).
- [ ] Platform pages (`/pages/home-assistant` etc.) — logo walls + ring texture would carry over naturally.

**Design-system upkeep**
- [ ] Rebuild `ui_kits/marketing` + `templates/marketing-site` in the claude.ai DS to match Bright Signal.
- [ ] Author `KitChooserCard`, `QuoteRotator`, `StatStrip`, `Breadcrumbs` as DS components (JSX + prompt.md + cards).
- [ ] Add a motion guideline card to the DS (timings/easings above).
- [ ] Once quiz art and logos land, sync `assets/imagery/` in the DS with the new art.

---

*Maintained alongside the code: update this file whenever the language changes, and re-sync the claude.ai design system (readme + Storefront cards) in the same change.*
