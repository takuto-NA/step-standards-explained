import { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import NURBSViewer from './components/NURBSViewer.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router, siteData }) {
    app.component('NURBSViewer', NURBSViewer)
  }
} satisfies Theme


