import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserRegister from '../views/UserRegister.vue'
import UserLogin from '../views/UserLogin.vue'
import MainChat from '../views/MainChat.vue'
import ChatList from '../views/ChatList.vue'
import ChatRoom from '../views/ChatRoom.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/mainchat',
    name: 'MainChat',
    component: MainChat,
    children: [
      {
        path: 'chatlist',
        component: ChatList
      },
      {
        path: 'chatroom',
        component: ChatRoom
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router
