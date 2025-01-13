import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import VueWechatTitle from 'vue-wechat-title'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'
import 'animate.css'
import './fonts/fonts.css'

//引入css
import '@/assets/css/global.css'
import VueSession from 'vue-session'

createApp(App)
.use(ElementPlus, {
    locale: zhCn,
})
.use(VueWechatTitle)
.use(store).use(router).mount('#app')
