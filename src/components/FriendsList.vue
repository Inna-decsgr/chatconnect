<template>
  <div>
    <p v-if="filteredUsers" class="text-xs text-gray-500 font-bold py-3 px-4">친구 {{ filteredUsers.length }}</p>
    <ul class="d-flex flex-column">
      <li v-for="(user, index) in filteredUsers" :key="index" class="w-100 hover:bg-gray-100" @dblclick="startchat(user)">
        <UserCard :friends="user" :favorites="favorites" />
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import UserCard from '../components/UserCard.vue'
import { v4 as uuidv4 } from 'uuid';
import socket from "../utils/socket";


export default {
  components: {
    UserCard
  },
  computed: {
    ...mapState(['users', 'user']),   
    filteredUsers() {
      return this.users.filter(user => user.id !== this.user.id);
    }
  },
  props: {
    favorites: {
      type: Object,
      default: null
    }
  },
  mounted() {
    this.$store.dispatch('getFriends')
  },
  methods: {
    startchat(user) {
      const chatid = this.getChatId({ myid: this.user.userid, friendid: user.user_id });
      this.$router.push({
        path: '/mainchat/chatroom',
        query: {id: user.user_id, username: user.username, image:user.profile_image}
      })
      socket.emit("joinRoom", { roomid: chatid, userid: this.user.userid });
    },
    getChatId(data) {
      const ids = [data.myid, data.friendid].sort();
      const chatKey = `chatId_${ids.join('_')}`;  
      let chatId = localStorage.getItem(chatKey); 

      if (!chatId) {  
        chatId = uuidv4();   
        localStorage.setItem(chatKey, chatId); 
      }
      return chatId;
    },
  }
}
</script>