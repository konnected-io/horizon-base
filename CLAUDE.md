# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Shopify theme for the Konnected.io store, built on **Horizon** — Shopify's first-party flagship theme that uses Liquid theme blocks. There is **no build step and no test suite**: the theme is server-rendered Liquid, JavaScript ships as native ES modules, and CSS ships as-is. Development happens against a live Shopify store through the Shopify CLI.

`origin` is `konnected-io/horizon-base`. Commits titled "Update from Shopify for theme horizon-base/main" come from Shopify's GitHub integration syncing edits made in the Shopify theme editor — expect machine-generated changes to `config/settings_data.json` and template JSON. To pull upstream Horizon updates, see the `upstream` workflow in README.md (`git pull upstream main` from `https://github.com/Shopify/horizon.git`).

## Commands

```bash
shopify theme dev        # local dev server with hot reload against the connected store
shopify theme check      # lint/validate Liquid (also runs in CI on every commit)
shopify theme push       # upload local theme to the store (use --unpublished for a draft)
shopify theme pull       # download store state (settings_data.json, template edits made in editor)
```

There are no unit tests. Validation = `shopify theme check` + visual verification in the dev server / theme editor.

### `shopify theme check` must be clean before committing

Theme check is configured by [`.theme-check.yml`](.theme-check.yml) and gates on **errors** (warnings don't fail the exit code). A clean run — `0 errors, exit 0` — is the pre-commit/CI signal, so **any new error is a real regression you introduced.** Don't reintroduce noise by working around the config.

Run it locally when you can. **But running it locally is not a hard gate** — if you're in a sandboxed environment without the Shopify CLI (or can't otherwise run `shopify theme check`), do not block on it. The same check runs in CI on every PR via [`.github/workflows/theme-check.yml`](.github/workflows/theme-check.yml) (using the same `.theme-check.yml`), so it's safe to open a PR and rely on the GitHub Action to report any errors. Say so explicitly in the PR ("theme check not run locally — relying on CI") so the run is reviewed before merge.

The config disables four checks that produce structural false positives for *this* theme (each is commented in the file with its rationale):
- **`MatchingTranslations`** — English-only store; custom keys added to `en.default.json` don't need backfilling into the 30 stock locale files (which Shopify's GitHub sync overwrites anyway).
- **`JSONMissingBlock`** — app blocks (`shopify://apps/okendo/…`, `…/collabs/…`) resolve at runtime; theme-check can't see them.
- **`ValidScopedCSSClass`** — Horizon defines CSS in shared stylesheets, not per-block scoped CSS.
- **`RemoteAsset`** — the Adobe Typekit font `<link>` in `layout/theme.liquid` is intentional.

`OrphanedSnippet` is intentionally **kept on** as an advisory warning (flags dead snippets worth cleaning up). For a genuine one-off false positive, prefer a scoped inline `{%- # theme-check-disable <Check> -%}` … `{%- # theme-check-enable <Check> -%}` with a comment (see `blocks/_header-button.liquid`) over disabling a check globally.

### Opening a pull request

This repo is a fork: `origin` is `konnected-io/horizon-base` and `upstream` is `Shopify/horizon`. Because of the `upstream` remote, a bare `gh pr create` defaults to opening the PR against **Shopify/horizon** — which is wrong. Always target this repo explicitly:

```bash
gh pr create --repo konnected-io/horizon-base --base main --head <branch> --title "..." --body "..."
```

## Architecture

### Liquid rendering model
- **Server-rendered first.** Business logic, money formatting, and translations live in Liquid, not JS. Async/on-demand rendering exists but is used sparingly as progressive enhancement.
- **Directory roles:** `sections/` (top-level page regions with `{% schema %}`), `blocks/` (composable units placed inside sections), `snippets/` (reusable Liquid partials rendered with `{% render %}`), `templates/` (JSON page definitions that wire sections+blocks together), `layout/theme.liquid` (document shell).
- **Block naming convention:** blocks prefixed with `_` (e.g. `_card.liquid`, `_cart-summary.liquid`) are private/nested — meant to be rendered by other blocks/sections, not exposed as standalone theme-editor blocks. Unprefixed blocks are user-selectable.
- **Sections accept `{"type": "@theme"}` and `{"type": "@app"}`** in their schema to allow theme blocks and app blocks. See `.cursor/rules/sections.mdc` for the required section skeleton (schema, CSS scoping via section class, translation keys for all text).

### JavaScript: web components
- JS is **progressive enhancement via custom elements**, not a framework. The base class is `Component` in [assets/component.js](assets/component.js) (extends `DeclarativeShadowElement`). It auto-wires child elements marked with a `ref` attribute into `this.refs`, supports declarative event listeners, and hydrates declarative shadow DOM.
- **Module resolution uses an import map**, not a bundler. `@theme/*` specifiers map to asset files in [snippets/scripts.liquid](snippets/scripts.liquid) (e.g. `@theme/events` → `events.js`). When adding a new shared module, register it there and add a `modulepreload` if it's critical. Import with `import { ThemeEvents } from '@theme/events'`.
- Cross-component communication goes through events defined in `assets/events.js` (`ThemeEvents`).
- Type checking is via JSDoc + `assets/global.d.ts` (declares `Shopify`, `Theme` globals). No TypeScript compilation step.

### Konnected-specific customizations
These are the local additions on top of stock Horizon — preserve them when merging upstream:
- **`assets/custom.js`, `assets/custom.css`** — site-specific JS (hash-scroll with sticky-header offset, header group height calc) and styles.
- **`assets/accordion-custom.js`, `assets/product-custom-property.js`** — bespoke components.
- **Custom templates** (named JSON templates assigned to specific products/collections/pages in the editor): `page.platforms.json`, `page.control4.json`, `page.smartthings.json`, `page.hubitat.json`, `page.homeassistant.json`, `page.konnected-partners.json`, `page.partners-index.json`, `page.collabs.json`, `collection.alarm-panel-pro-kits.json`, `collection.gdo-collection.json`, `collection.partners-and-resellers.json`, `product.gdo-blaq-v2.json`, `product.garage-door-opener.json`, `product.pro-conversion-kit.json`, `product.pro-interface-kit.json`.

## Conventions enforced by Cursor rules (`.cursor/rules/`)

- **Accessibility is non-negotiable.** Per-component WAI-ARIA rules exist for accordions, tabs, headings, tooltips, comboboxes, modals, flip cards, product cards, and sale prices. When building or editing any interactive component, match the required ARIA attributes, keyboard handlers (Enter/Space/Escape/arrows), and focus management described in the relevant `.mdc` file.
- **All user-facing text must be a translation key.** Use `{{ 'group.key' | t }}`; add the key to `locales/en.default.json` (the required source of truth) under a hierarchical, snake_case path (max 3 levels deep). `*.schema.json` locale files hold theme-editor setting labels (`t:` references in schemas). See `.cursor/rules/locales.mdc`.
