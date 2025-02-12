import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from '../store.js'
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

// ✅ 소켓 가져오기
import socket from './utils/socket';

const app = createApp(App);
app.config.globalProperties.$socket = socket; // Vue 전역에서 사용 가능하도록 설정

app.use(store).use(router).mount('#app');
