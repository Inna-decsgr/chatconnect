import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    user: {},  // 현재 사용자
    users: [],  // 모든 사용자 목록
    token: localStorage.getItem('access_token') || null,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
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
    }
  },
  actions: {
    // 로그인한 사용자 정보 가져오기
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
    // 로그인
    async login({ commit, dispatch }, credentials) {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: credentials.username,
          password: credentials.password,
        });

        console.log('로그인 응답 정보', response.data);

        const accessToken = response.data.access_token || response.data.token;
        if (!accessToken) {
          throw new Error('No access token found in login response');
        }
        
        commit('SET_USER', response.data.user);
        commit('SET_TOKEN', accessToken);

        console.log(accessToken);

        // 로그인 끝나면 fetchUserData 실행
        await dispatch('fetchUserData');
        
        return response.data;
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    // 로그아웃
    logout({ commit }) {
      commit('CLEAR_AUTH_DATA');
    },
    // 모든 사용자 목록 가져오기
    async getFriends({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/users');
        commit('SET_FRIENDS', response.data);
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    }
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    user(state) {
      return state.user;
    }
  }
});

if (store.state.token) {  // 로그인 상태 유지하려고
  store.dispatch('fetchUserData');
}


export default store;