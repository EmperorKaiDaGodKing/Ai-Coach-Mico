# Private Adult Mode — Design Document

Purpose:
- Provide an isolated, opt-in "Private Adult Mode" for handling mature or sensitive interactions.
- Ensure work/development mode remains free of unsolicited mature content and distractions.

Key points:
- Activation requires explicit owner confirmation and a two-step opt-in:
  1. Enable flag in config (owner-only action).
  2. Per-session confirmation with displayed disclaimer and consent.
- The system logs all activations (timestamp, user id, session id) to an encrypted audit log.
- The system applies configurable content filters and a moderation webhook; flagged content is blocked or quarantined.
- Age verification note: the repository can collect opt-in attestations but cannot guarantee age; include legal disclaimers.
- Provide an "escape" command to immediately end Private Adult Mode and purge non-essential session history.

Security & compliance:
- Access controls: owner-only config changes; logging; minimal retention policy.
- Moderation: configurable classifiers + external moderation endpoint.
- Documentation: contributor rules, legal disclaimers, and testing checklist.

Next actions:
- Add nsfw_config.yaml, gating module, tests, and README section.
