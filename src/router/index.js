import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserRegister from '../views/UserRegister.vue'
import UserLogin from '../views/UserLogin.vue'
import MainChat from '../views/MainChat.vue'
import ChatList from '../views/ChatList.vue'
import ChatRoom from '../views/ChatRoom.vue'
import store from '../../store'

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
    meta: {requiresAuth: true},
    children: [
      {
        path: 'chatlist',
        component: ChatList,
        meta: {requiresAuth: true}
      },
      {
        path: 'chatroom',
        component: ChatRoom,
        meta: {requiresAuth: true}
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.user !== null && Object.keys(store.state.user).length > 0;


  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/'); 
  } else {
    next();  
  }
});

export default router
