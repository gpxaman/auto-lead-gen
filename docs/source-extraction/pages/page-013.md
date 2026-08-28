---
page: 13
document: "Autonomous Freelance Agent Factory Architecture.pdf"
pdf_footer: "8/25/26, 5:26 PM — Autonomous Freelance Agent Factory Architecture — https://gemini.google.com/app/f8dc46d6099d59ae?hl=en-IN — 13/29"
---

## User prompt

make the prompt much more advacnced and what this does is that it also if one agent on top the chain updates one thing all the agents below will spin up another unit like 24/7 complete autonoumous system and also for each of the chain there is one agent which sole task is to prevent hallunitations and report what model ai halunicated and after a ceratin threshold it will pin that ai in the admin panel and cease its operation transfer its context and everything into replacement ai and then another ai which adds new metrics and infos that needs to be collected and it has a feature if ceratian specs like accuracy of all the date and adding any more info or metrics is useless means it will put it as notice and remains ideal

NOTE (USER_REQUIREMENT — significant, multi-part): This turn adds four new explicit requirements on top of the Layer 1-4 architecture from Page 11-12:
1. **Cascading update propagation:** if an upstream agent updates something, all downstream agents must spin up a new unit — described as a "24/7 complete autonomous system."
2. **Hallucination-prevention agent per chain:** sole task is to detect hallucination, report which model AI hallucinated, and after a threshold, pin that AI in the admin panel and cease its operation.
3. **Context transfer on replacement:** transfer the ceased agent's context and everything into a replacement AI.
4. **Metric-discovery agent:** a separate AI whose job is to add new metrics/info that need to be collected, with a self-limiting feature — if certain specs (e.g. "accuracy of all the data") and adding more info/metrics becomes "useless," it marks this as a notice and goes idle ("remains ideal" — sic, intended "idle").

## Response

Here is the advanced, production-grade master system prompt. It incorporates event-driven cascade updates, isolated hallucination watchdog agents with automated hot-swap failovers, an exploratory telemetry optimizer, and saturation throttles to keep the system running 24/7 without infinite loops or data bloat.

[Response continues into the code block beginning on Page 14: "# SYSTEM PROMPT: Autonomous Self-Healing Multi-Agent Lead & Intelligence Infrastructure"]
