---
layout: home

hero:
  name: "STEP Standards Explained"
  text: "A Practical Guide to ISO 10303"
  tagline: "Explaining versions, capabilities, and implementation methods for CAD engineers and developers."
  image:
    src: https://vitepress.dev/vitepress-logo-large.png
    alt: VitePress
  actions:
    - theme: brand
      text: Get Started
      link: /docs/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/takuto-NA/step-standards-explained

features:
  - title: Complete STEP Guide
    details: From AP203 to AP242, understand the evolution and capabilities of the standard.
  - title: Implementer Focus
    details: Practical tips, common pitfalls, and line-by-line walkthroughs of real STEP files.
  - title: Interactive Learning
    details: Visualized entity structures and clear decision guides for selecting the right AP.
---

<style>
:root {
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: -webkit-linear-gradient(120deg, #bd34fe 30%, #41d1ff);
}
</style>

## 🚀 Why this guide?

Agents and engineers often don’t have the context they need to do real work reliably with STEP files. This guide solves this by giving you access to procedural knowledge and specific context you can load on demand.

## 📚 Learning Path

::: info Step 1: Foundational Knowledge
Understand STEP-specific terminology and the big picture.
- [Glossary](/docs/glossary)
- [Persistent IDs and Face Naming](/docs/persistent-ids)
- [Getting Started](/docs/getting-started)
- [FAQ](/docs/faq)
:::

::: info Step 2: Select the Right AP
Choose the right Application Protocol for your project.
- [Which AP should I use?](/decision-guides/which-ap-should-i-use)
- [Capability Matrix](/comparison/capability-matrix)
:::

::: info Step 3: Understand Data Structures
Dive into the entity hierarchy and EXPRESS language.
- [STEP File Walkthrough](/examples/step-file-walkthrough)
- [Data Model Map](/format/data-model-map)
- [EXPRESS Language Basics](/format/express-overview)
:::

::: info Step 4: Implementation
Common pitfalls and quality assurance.
- [Common Pitfalls](/implementation/common-pitfalls)
- [Validation and CAx-IF](/implementation/validation-and-caxif)
:::

