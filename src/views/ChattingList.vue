<template>
  <div>
    <div class="pt-3 pb-2 w-[100%]">
      <div class="flex justify-between items-center">
        <p class="text-lg font-bold pl-5 pb-3">채팅 <i class="fa-solid fa-caret-down"></i></p>
        <button @click="showSearch">
          <i class="fa-solid fa-magnifying-glass text-lg pr-5 pb-2"></i>
        </button>
      </div>
      <div v-if="showSearchBar" class="flex items-center pl-4 pb-3">
        <input 
          type="text"
          v-model="searchkeyword"
          class="py-2 px-3 rounded-2xl bg-[#efefef] text-sm w-[90%] "
          placeholder="채팅방, 참여자 검색"
          @keyup.enter="getSearchResult"
        >
        <button class="w-[10%] pr-3" @click="close">
          <i class="fa-solid fa-x text-sm text-gray-500 pl-3 cursor-pointer"></i>
        </button>
      </div>
      <div>
        <ChatCard :messages="groupedMessages"/>
      </div>
    </div>
  </div>
</template>

<script>
import ChatCard from '../components/ChatCard'
import axios from 'axios';


export default {
  data() {
    return {
      groupedMessages: [],
      showSearchBar: false,
      searchkeyword: null,
      searhuserid: null,
      searchresult: []
    }
  },
  components: {
    ChatCard
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  mounted() {
    this.getLastMessage();
  },
  methods: {
    async getLastMessage() {
      try {
        const response = await axios.get(`http://localhost:5000/lastmessage/${this.user.userid}`);
        
        this.groupedMessages = Object.values(
          response.data.reduce((acc, message) => {
            const chatId = message.chat_id;

            if (!acc[chatId] || new Date(message.created_at) > new Date(acc[chatId].created_at)) {
              // 상대방 정보를 display_user로 설정
              acc[chatId] = {
                ...message,
                display_user: {
                    id: message.receiver_id,
                    name: message.receiver_name,
                    profile_image: message.profile_image
                  } // 내가 보낸 경우, receiver 정보를 저장
              };
            }
            return acc;
          }, {})
        );
        console.log('채팅방별 최신 메시지:', this.groupedMessages);
      } catch (error) {
        console.error('메세지 가져오기 실패', error.response?.data || error.message);
      }
    },
    showSearch() {
      this.showSearchBar = true;
      console.log(this.showSearchBar);
    },
    close() {
      this.showSearchBar = false
    },
    async getSearchResult() {
      console.log('검색 키워드', this.searchkeyword);
      const response = await axios.get(`http://localhost:5000/searchuser/${this.searchkeyword}`);
      console.log('검색 키워드를 포함하는 모든 사용자들', response.data);
      // 검색 결과가 없는 경우 빈 배열 처리
      if (response.data.length === 0) {
        console.log("검색 결과 없음");
        this.groupedMessages = [];
        return;
      }

      this.searchresult = response.data.map((user) =>
        axios.get(`http://localhost:5000/lastmessage/${this.user.userid}`, {
          params: {id: user.id}
        }).then(res => res.data)
      )

      if (this.searchresult) {
        // 모든 요청의 결과를 Promise.all로 처리
        Promise.all(this.searchresult).then((response) => {
          // 각 Promise 결과의 [0]을 가져와 display_user를 설정
          this.groupedMessages = response.map((message) => {
            const lastmessage = message[0];  // 각 Promise의 첫 번째 메세지 저장

            return {
              ...lastmessage,
              display_user: {
                id: lastmessage.receiver_id,
                name: lastmessage.receiver_name,
                profile_image: lastmessage.profile_image
              }
            }
          });

          console.log('최종 검색 결과', this.groupedMessages);
        });
      } else {
        this.groupedMessages = []
      }
    }
  }
}
</script>


<style>
input {
  border: 1px solid #efefef;
}

input:focus {
  background-color: white;
  outline: none;
  border: 1px solid rgb(187, 185, 185);
}

input:focus::placeholder {
  color: transparent;
}
</style>