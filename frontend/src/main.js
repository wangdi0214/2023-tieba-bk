import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { applyReactInVue } from 'veaury'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/index.scss'

// 创建Vue应用
const app = createApp(App)

// 使用状态管理
const pinia = createPinia()
app.use(pinia)

// 使用路由
app.use(router)

// 使用Element Plus
app.use(ElementPlus)

// 注册全局组件
// 这里可以注册一些全局的React组件，通过veaury在Vue中使用

app.mount('#app')