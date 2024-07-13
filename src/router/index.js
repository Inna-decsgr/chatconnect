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


// 인증되지 않은 사용자가 해당 경로에 접근하려고하면 막기
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.user !== null && Object.keys(store.state.user).length > 0;
  // 현재 로그인한 사용자가 null이 아니거나(사용자가 있거나) 사용자의 길이가 0보다 클다면 isAuthenticated는 true. 사용자가 없다면 false

  // 인증이 필요한 라우트에 접근할 때 사용자 인증이 되지 않았다면
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // meta.requiresAuth가 true(인증이 필요한 경로인데)인데 (&&) 인증된 사용자가 없다면 => 사용자가 없다면 isAuthenticated가 false인데 !한번 더 붙었으니까 true. true&&true라서 next('/')가 실행
    next('/');  // 홈으로 리다이렉트
  } else {
    next();  // 인증이 된 상태라면 다음으로 진행
  }
});

export default router
