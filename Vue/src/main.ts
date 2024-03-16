import { createApp } from 'vue' // 造花盆
// @ts-ignore
import App from './App.vue' // 根
// import router from './router' // 路由

// 1.引入 pinia
import { createPinia } from 'pinia'

const app = createApp(App)

// 2.创建 pinia
const pinia = createPinia()

// 3.安装 pinia
app.use(pinia)

// app.use(router) // 使用路由
app.mount('#app')
// 造花盆，把根放到花盆里 -> 挂载到 id 为 app 的容器（div，在 index 里）上

