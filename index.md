---
title: STEP Standards Explained
---

# Overview

A simple, open guide for understanding and implementing the STEP standard (ISO 10303).

STEP (Standard for the Exchange of Product model data) is an international standard for the computer-interpretable representation and exchange of industrial product data. While powerful, it is notoriously complex. This guide provides the procedural knowledge and context needed to work with STEP files accurately and efficiently.

## Why this guide?

Engineers and developers often don’t have the context they need to implement STEP support reliably. This project solves this by giving you access to technical knowledge and specific implementation details that you can apply immediately.

* **Expert Knowledge**: Specialized knowledge from geometry definitions to PMI (Product and Manufacturing Information).
* **Implementation Focus**: Practical tips for building parsers, exporters, and handling persistent IDs.
* **Open Standard**: Based on ISO 10303, explaining the differences between AP203, AP214, and AP242.

## What can this guide enable?

* **Domain expertise**: Understand the hierarchy of entities and the EXPRESS language used to define them.
* **Accurate Data Exchange**: Learn how to preserve colors, layers, and semantic PMI across different CAD systems.
* **Repeatable Workflows**: Turn complex STEP export/import tasks into consistent and reliable processes.

## Adoption & Compatibility

The STEP standard is supported by all major CAD and simulation tools. Understanding which version (AP) to use is critical for interoperability.

| Application Protocol | Primary Focus | Use Case |
| :--- | :--- | :--- |
| **AP203** | Configuration Controlled Design | Legacy systems, basic geometry |
| **AP214** | Automotive Mechanical Design | Mainstream CAD exchange (colors/layers) |
| **AP242** | Managed Model Based 3D Engineering | Modern MBD, PMI, and simulation |

[→ View full CAD Support Matrix](/comparison/cad-support-matrix)

## Get started

<div class="card-grid">
  <a href="./docs/getting-started" class="card">
    <div class="card-title">Getting Started</div>
    <div class="card-description">Quickly grasp the big picture of the STEP standard.</div>
  </a>
  <a href="./docs/glossary" class="card">
    <div class="card-title">Glossary</div>
    <div class="card-description">Understand STEP-specific terminology and concepts.</div>
  </a>
  <a href="./docs/faq" class="card">
    <div class="card-title">FAQ</div>
    <div class="card-description">Resolve common questions about STEP implementations.</div>
  </a>
  <a href="./examples/step-file-walkthrough" class="card">
    <div class="card-title">File Walkthrough</div>
    <div class="card-description">Understand real STEP files line by line.</div>
  </a>
</div>

