import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// https://vitepress.dev/reference/site-config
export default withMermaid(defineConfig({
  title: "STEP Standards Explained",
  description: "A practical guide to the STEP standard (ISO 10303)",
  srcDir: '.',
  cleanUrls: true,
  ignoreDeadLinks: true,
  appearance: 'dark',
  
  // Mermaid support is handled by withMermaid
  markdown: {
    math: true,
  },

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/docs/getting-started' },
      { text: 'FAQ', link: '/docs/faq' }
    ],

    sidebar: [
      {
        text: 'Learning Path',
        items: [
          {
            text: '1. Foundational Knowledge',
            items: [
              { text: 'Glossary', link: '/docs/glossary' },
              { text: 'Getting Started', link: '/docs/getting-started' },
              { text: 'FAQ', link: '/docs/faq' }
            ]
          },
          {
            text: '2. Select the Right AP',
            items: [
              { text: 'Which AP should I use?', link: '/decision-guides/which-ap-should-i-use' },
              { text: 'Capability Matrix', link: '/comparison/capability-matrix' }
            ]
          },
          {
            text: '3. Data Structures',
            items: [
              { text: 'STEP File Walkthrough', link: '/examples/step-file-walkthrough' },
              { text: 'Data Model Map', link: '/format/data-model-map' },
              { text: 'EXPRESS Language Basics', link: '/format/express-overview' }
            ]
          },
          {
            text: '4. Implementation',
            items: [
              { text: 'Common Pitfalls', link: '/implementation/common-pitfalls' },
              { text: 'Validation and CAx-IF', link: '/implementation/validation-and-caxif' }
            ]
          }
        ]
      },
      {
        text: 'Reference',
        items: [
          {
            text: 'AP Versions',
            collapsed: true,
            items: [
              { text: 'AP203', link: '/versions/ap203' },
              { text: 'AP214', link: '/versions/ap214' },
              { text: 'AP242 ed1', link: '/versions/ap242-ed1' },
              { text: 'AP242 ed2', link: '/versions/ap242-ed2' },
              { text: 'AP242 ed3', link: '/versions/ap242-ed3' }
            ]
          },
          {
            text: 'Format Details',
            collapsed: true,
            items: [
              { text: 'Anatomy of Product', link: '/format/anatomy-of-product' },
              { text: 'STEP File Basics', link: '/format/step-file-basics' }
            ]
          },
          {
            text: 'Comparison',
            collapsed: true,
            items: [
              { text: 'Assembly Support', link: '/comparison/assembly-support' },
              { text: 'CAD Support Matrix', link: '/comparison/cad-support-matrix' },
              { text: 'Part 21 vs Part 28', link: '/comparison/part21-vs-part28' },
              { text: 'PMI Support', link: '/comparison/pmi-support' }
            ]
          }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/takuto-NA/step-standards-explained' }
    ],

    footer: {
      message: 'Released under the CC-BY-4.0 License.',
      copyright: 'Copyright © 2025-present'
    }
  }
}))

