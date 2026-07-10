# Product

## Register

brand

## Users

Three audiences, in priority order:

1. **Homeowners with dormant wiring** — people who bought or own a house with an old wired alarm system (panel in a closet, sensors in every door and window) or a plain garage door opener. They are not hobbyists; they want the stuff they already own to work in the app they already use. Context: evaluating whether this is a DIY-able weekend project.
2. **Smart-home enthusiasts** — Home Assistant, SmartThings, Hubitat, Homebridge users who care about local control, open APIs, and no cloud lock-in. They arrive pre-sold on the concept and are auditing the execution (ESPHome inside, official integrations, no subscription).
3. **Pro installers and integrators** — Control4/alarm trade professionals retrofitting client homes.

The job to be done: "make the wiring and hardware my house already has show up in my smart-home platform, without a monthly fee."

## Product Purpose

Konnected sells retrofit boards that convert two things nearly every house already owns — the wired alarm system and the garage door opener — into first-class smart-home devices. Success looks like a visitor understanding within one scroll that (a) their house is already wired for this, (b) it works in *their* platform, and (c) there is no subscription, then choosing a product line.

## Brand Personality

Confident, plain-spoken, trust-first. Second person, platform- and product-named, zero hype. The emotional register is *relief and ownership* ("use what you already paid for") rather than fear ("protect your family") or novelty ("the future is here").

## Anti-references

- **Alarm-industry fear marketing** — ADT-style burglar imagery, red alerts, urgency. Red is reserved for genuine danger states only.
- **Dark "techy" aesthetics** — black panels, neon glows, hacker-terminal vibes. The storefront is light by lock (see DESIGN.md).
- **Subscription-upsell patterns** — pricing tables with "recommended" tiers, feature-gating, recurring-revenue framing. The absence of a subscription IS the pitch.
- **Generic smart-home stock art** — interchangeable "person taps tablet in beige loft" imagery without Konnected product or UI in frame.

## Design Principles

1. **The house is the hero.** The most persuasive asset is the buyer's own home: show existing wiring, sensors, and openers becoming smart, not abstract lifestyle scenes.
2. **Answer "who is this for" out loud.** Fit labels and decision notes over feature lists; every surface should let a visitor self-select in seconds.
3. **Trust is light.** Airy, bright, hairline-separated surfaces; proof (real quotes, real numbers, official works-with badges) over claims.
4. **Both product lines are equals.** Alarm panels and garage openers get parity in size, CTA weight, and placement whenever they share a surface.
5. **Nothing rented.** Copy and design must never imply a service dependency; local control and ownership are the differentiators.

## Accessibility & Inclusion

- WAI-ARIA per-component rules in `.cursor/rules/` are non-negotiable (keyboard paths, focus management, ARIA states).
- All motion beyond hover is disabled under `prefers-reduced-motion`.
- Body text contrast ≥ 4.5:1; secondary text uses foreground at ≥ 60% alpha on light surfaces.
- All user-facing strings are translation keys in theme Liquid (custom-liquid template sections are exempt: English-only store).
