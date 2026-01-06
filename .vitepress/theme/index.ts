// https://vitepress.dev/guide/custom-theme
import { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router, siteData }) {
    // ...
  }
} satisfies Theme


