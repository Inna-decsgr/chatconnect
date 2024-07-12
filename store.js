import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state: {
    user: {},
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
    logout({ commit }) {
      commit('CLEAR_AUTH_DATA');
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

export default store;


if (store.state.token) {
  store.dispatch('fetchUserData');
}