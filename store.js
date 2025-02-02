import { createStore } from 'vuex';
import axios from 'axios';
import createPersistedState from 'vuex-persistedstate';

const store = createStore({
  state: {
    me: {},
    user: {},   
    users: [],  
    token: localStorage.getItem('access_token') || null,
    favorite_users: []
  },
  mutations: {
    SET_USER(state, user) {
      console.log('SET_USER 호출됨:', state.user);
      // ... 스프레드 연산자 사용하면 객체를 병합하면서 중복된 키는 새로운 객체의 값으로 덮어씌움
      state.user = {
        ...state.user, // 기존 데이터를 유지
        ...user,       // 새로운 데이터로 덮어쓰기
      };
      state.me = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('access_token', token);
    },
    CLEAR_AUTH_DATA(state) {
      state.user = null;
      state.token = null;
      localStorage.removeItem('access_token');
    },
    SET_FRIENDS(state, users) {
      state.users = users
    },
    setProfileMessage(state, message) {
      state.user.profile_message = message;
    },
    SET_FAVORITE(state, users) {
      state.favorite_users = users;
    },
    CLEAR_FAVORITE(state) {
      state.favorite_users = null;
    },
    addFavoriteUser(state, user) {
      state.favorite_users.push(user);
    },
    removeFavoriteUser(state, friendid) {
      state.favorite_users = state.favorite_users.filter(user => user.user_id !== friendid);
    }
  },
  actions: {
    async fetchUserData({ commit, state }) {
      if (!state.token) {
        return;
      }
      try {
        const response = await axios.get('http://localhost:5000/get_profile', {
          headers: {
            Authorization: `Bearer ${state.token}`
          }
        });
        commit('SET_USER', response.data);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        commit('CLEAR_AUTH_DATA');
      }
    },
    async login({ commit, dispatch }, userdata) {
      try {        
        const response = await axios.post('http://localhost:5000/login', {
          id: userdata.id,
          password: userdata.password,
        });

        console.log('로그인 응답 정보', response.data.user);
        commit('SET_USER', response.data.user);
        commit('SET_FAVORITE', response.data.user.favorite_users);

        const accessToken = response.data.access_token || response.data.token;
        if (!accessToken) {
          throw new Error('No access token found in login response');
        }
        commit('SET_TOKEN', accessToken);

        await dispatch('fetchUserData');
        
        return response.data;
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    logout({ commit }) {
      commit('CLEAR_AUTH_DATA');
      commit('CLEAR_FAVORITE')
    },
    async getFriends({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/users');
        commit('SET_FRIENDS', response.data);
        console.log('친구들', response.data);
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    }
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    getUser(state) {
      return state.user;
    },
    getMe(state) {
      return state.me;
    },
    getFavoriteUsers(state) {
      return state.favorite_users;
    }
  },
  plugins: [  
    createPersistedState({
      key: 'myApp', 
      paths: ['user', 'favorite_users'], 
    })
  ],
});

if (store.state.token) {  
  store.dispatch('fetchUserData');
}


export default store;