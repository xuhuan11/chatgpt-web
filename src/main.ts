import { createApp } from 'vue'
import { createGuard } from '@authing/guard-vue3'
import '@authing/guard-vue3/dist/esm/guard.min.css'

import App from './App.vue'
import { setupI18n } from './locales'
import { setupAssets, setupScrollbarStyle } from './plugins'
import { setupStore } from './store'
import { setupRouter } from './router'

async function bootstrap() {
  const app = createApp(App)
  app.use(
    createGuard({
      appId: '642e4e1d0767409fce8e1ab8',
    }),
  )
  setupAssets()

  setupScrollbarStyle()

  setupStore(app)

  setupI18n(app)

  await setupRouter(app)

  app.mount('#app')
}

bootstrap()
