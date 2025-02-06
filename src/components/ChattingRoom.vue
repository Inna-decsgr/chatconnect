<template>
  <div id="app">
    <div>
      <ChatTopBar />
    </div>
    <div class="chat-container p-3" ref="chatContainer">
      <div v-for="(group, groupIndex) in messages" :key="groupIndex">
        <!-- 날짜별로 표시-->
        <p class="bg-gray-800 bg-opacity-5 text-center w-[160px] mx-auto my-3 text-xs py-[6px] rounded-xl text-gray-600">
          <i class="fa-regular fa-calendar"></i>
          {{group.date}} {{ group.day }}
        </p>

        <!--날짜별로 메시지 반복-->
        <div v-for="minuteGroup in group.groupedMinutes" :key="minuteGroup.minute" class="mb-2">
        <!--쉽게 생각하면 receiver_id, 수신자가 7이고 보내는 사람이 8이라고 치자. 그럼 sender_id와 user.userid는
        8로 같을수밖에 없잖아. 현재 로그인된 사용자가 메시지를 보낼테니까. 근데 우리가 채팅방을 만들때 같은 방을 
        공유하게 만들어뒀으니까 7이 sender가 될수도 receiver가 될수도 있고 8이 sender가 될수도 receiver가 될 수도 있잖아 그치?
        데이터베이스 보면서 이해하면 더 잘될거야. receiver_id가 userid와 같은것만 따로 모아서 왼쪽 정렬하고
        receiver_id와 userid가 다른것만 모아서 오른쪽 정렬하는거야! 그냥 야매로 생각하자면 현재 로그인된
        사용자가 sender가 되어서 오른쪽에 보여야하는거잖아. 그러니까 반대로 생각해서 receiver_id와 userid
        가 같은 것만 골라서 왼쪽정렬하면 v-else했을때 반대의 경우가 다 오른쪽 정렬되니까 그런거라고 생각해.
        미래의 나야...과거의 내가 멍청해서 미안 허허허 내가 고쳤어! 현재 사용자와 sender_id가 
        같지 않으면 수신자라는 거니까 msg.receiver_id === user.userid에서 아래와 같이 바꿈!ㅎㅎ-->
          <div v-for="(msg, index) in minuteGroup.messages" :key="index" class="message-wrapper" :class="msg.sender_id === user.userid ? 'sender-wrapper' : 'receiver-wrapper'">
            <div class="message-container">
              <div class="flex">
                <img v-if="msg.sender_id !== user.userid && index === 0" :src="msg.receiver_profile_image ? `http://localhost:5000${msg.receiver_profile_image}` : '/images/사용자 프로필.png'" class="w-[40px] h-[40px] object-cover rounded-[16px]">
                <div class="pl-3">
                  <p class="text-[12px] mb-[3px]" v-if="msg.sender_id !== user.userid && index === 0">{{ msg.sender_name }}</p>
                  <div class="flex">
                    <!-- receiver일 때는 text가 먼저오도록 -->
                    <div v-if="msg.sender_id !== user.userid" class="flex">
                      <p :class="['message', msg.sender_id === user.userid ? 'sender' : 'receiver', index === 0 ? 'has-tail' : '', index !== 0 ? 'ml-[39px]' : '']">{{ msg.text }}</p>
                      <p v-if="index === minuteGroup.messages.length - 1" class="time">{{ msg.created_at }}</p>
                    </div>
                    <!-- sender일 때는 info-wrapper가 앞에 오도록 설정 -->
                    <div v-if="msg.sender_id === user.userid" class="flex">
                      <div class="info-wrapper">
                        <p v-if="msg.sender_id == user.userid && !msg.is_read" class="unread-indicator" :class="index !== minuteGroup.messages.length - 1 ? 'mt-[14px]' : 'mt-[2px]'">1</p>
                        <p v-if="index === minuteGroup.messages.length - 1" class="time">{{ msg.created_at }}</p>
                      </div>
                      <p :class="['message', msg.sender_id === user.userid ? 'sender' : 'receiver', index === 0 ? 'has-tail' : '']">{{ msg.text }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex">
      <input 
        type="text" 
        class="basis-5/6 text-xs p-3 outline-none" 
        v-model="newMessage" 
        placeholder="메시지 입력" 
        @keyup.enter="sendmessage"
        @input="newMessage = $event.target.value"
      >
      <!--@input 이벤트는 사용자가 입력 필드에 값을 입력하거나 변경할 때마다 트리거됨. 
        입력한 값을 실시간으로 감지하면서 추가로 공백 제거 작업을 처리하기 위해서 사용.
        Vue에서는 v-model과 동일한 동작으로 수행하기 때문에 데이터 간의 양방향 바인딩을 설정하는 역할을 함.
        v-model을 사용했지만 추가적인 데이터 처리(공백 제거, 유효성 검사)가 필요할 때 유용.
      -->
      <button 
        class="text-xs basis-1/6" 
        :disabled="!newMessage.trim()"
        :class="newMessage ? 'bg-[#f7e330] hover:bg-[#ffd966]' : 'bg-gray-200 text-gray-400 cursor-not-allowed'"
        @click="sendmessage">전송</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid';
import { chatformatTime } from '@/utils/chatformatTime';
import ChatTopBar from './ChatTopBar.vue';

export default {
  components: {
    ChatTopBar
  },
  data() {
    return {
      newMessage: '',
      messages: [],
      chatId: null
    }
  },
  created() {
    this.loadUserandMessages();
  },
  mounted() {
    this.loadUserandMessages();
  },
  updated() {
    this.scrollToBottom();
  },
  computed: {
    ...mapState(['user'])
  },
  props: { 
    friendId: {
      type: String,
      required: true
    },
    friendName: {
      type: String,
      required: true
    },
    friendImage: {
      type: String,
      required: false
    }
  },
  methods: {
    async loadUserandMessages() {
      await this.$store.dispatch('fetchUserData'); 

      if (this.user && this.user.userid) {
        this.chatId = this.getChatId();
        this.loadMessages();
      } else {
        console.error('User is not defined or userid is missing');
      }

      this.setIsReadTrue(this.chatId);
    },
    getChatId() {
      const ids = [this.user.userid, this.friendId].sort();
      const chatKey = `chatId_${ids.join('_')}`;  
      let chatId = localStorage.getItem(chatKey); 

      if (!chatId) {  
        chatId = uuidv4();   
        localStorage.setItem(chatKey, chatId); 
      }
      return chatId;
    },
    async loadMessages() {
      try {
        const response = await axios.get(`http://localhost:5000/messages/${this.chatId}`);
        console.log('날짜보기', response.data);

        // 날짜별로 메세지 그룹화할 객체
        const daysOfWeek = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
        const groupedMessages = {};

        response.data.forEach(msg => {
          const dateObj = new Date(msg.created_at);

          // 연, 월, 일 추출
          const year = dateObj.getFullYear();
          const month = dateObj.getMonth() + 1; // 0부터 시작하므로 +1 필요
          const day = dateObj.getDate();
          // 날짜를 2025년 2월 5일 형식으로 조합하기
          const dateKey = `${year}년 ${month}월 ${day}일`;
          const dayOfWeek = daysOfWeek[dateObj.getDay()]; // 요일 추출

          // 시간:분 키 생성
          const minuteKey = chatformatTime(msg.created_at);

          // 날짜 그룹이 없으면 새로 생성
          if (!groupedMessages[dateKey]) {  // 새로운 날짜일 경우
            groupedMessages[dateKey] = {
              day: dayOfWeek,
              groupedMinutes: {}
            };            
          }

          // minuteKey 그룹이 없으면 새로 생성
          if (!groupedMessages[dateKey].groupedMinutes[minuteKey]) {
            groupedMessages[dateKey].groupedMinutes[minuteKey] = [];
          }

          // 있으면 해당 날짜, 분 그룹에 메시지 추가
          groupedMessages[dateKey].groupedMinutes[minuteKey].push({
            ...msg,
            created_at: chatformatTime(msg.created_at)  // 새로운 날짜 키 생성
          })
        });

        // 객체를 배열로 변환해서 날짜별 메시지 리스트 생성
        this.messages = Object.keys(groupedMessages).map(date => {
          // Object.keys(groupedMessages)를 하게 되면 객체의 키(날짜)민 배열로 추출 가능. map을 사용하면 키(날짜)만 date로 가져올 수 있음. value 값은 해당 배열의 키를 사용해서 값을 다시 가져와야함.
          return {
            date,  // 날짜(년-월-일)
            day: groupedMessages[date].day,
            groupedMinutes: Object.keys(groupedMessages[date].groupedMinutes).map(minute => {
              return {
                minute,
                messages: groupedMessages[date].groupedMinutes[minute]
              }
            })
          };
        });
        console.log('그룹화', this.messages)
      } catch (error) {
        console.error('메시지 로드 실패:', error)
      }
    },
    async sendmessage() {
      if (this.newMessage.trim()) {
        const timestamp = new Date().toISOString();  
        const messages = {
          chat_id: this.chatId,
          sender_id: this.user.userid,
          sender_name: this.user.username,
          receiver_id: this.friendId,
          receiver_name: this.friendName,
          text: this.newMessage,
          timestamp
        };
        console.log('메세지 정보', messages);

        try {
          const response = await axios.post('http://localhost:5000/messages', messages);
          console.log('보낸 메시지', response.data);

          // 날짜 키와 요일 계산
          const daysOfWeek = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
          const dateObj = new Date(response.data.created_at);
          const year = dateObj.getFullYear();
          const month = dateObj.getMonth() + 1; // 월은 0부터 시작하므로 +1 필요
          const day = dateObj.getDate();
          const dateKey = `${year}년 ${month}월 ${day}일`; // "YYYY년 M월 D일" 형식
          const dayOfWeek = daysOfWeek[dateObj.getDay()]; // 요일 계산

          // 시간 + 분 키 생성
          const hour = dateObj.getHours().toString().padStart(2, "0");  // 00~23
          const minute = dateObj.getMinutes().toString().padStart(2, "0"); // 00~59
          const minuteKey = `${hour}:${minute}`; // "21:48" 형식

          // 새로운 메세지 포맷
          const formattedMessage = {  
            ...response.data,
            created_at: chatformatTime(response.data.created_at)
          };

          // 기존 그룹에서 메세지를 추가할 해당 날짜 키를 찾음
          const groupIndex = this.messages.findIndex(group => group.date === dateKey);

          if (groupIndex !== -1) {
            // 해당 날짜 그룹이 이미 있으면 그 그룹의 groupedMinutes(시간 그룹) 배열을 groupedMinutes에 저장
            const groupedMinutes = this.messages[groupIndex].groupedMinutes;

            if (!groupedMinutes[minuteKey]) {
              // 해당 날짜는 있는데 해당 시간이 없을 경우 새로 생성
              groupedMinutes[minuteKey] = [];
            }

            // 있으면
            groupedMinutes[minuteKey].push(formattedMessage);
          } else {
            // 해당 날짜 그룹이 없으면 새 그룹을 생성 후 메세지 추가
            this.messages.push({
              date: dateKey,
              day: dayOfWeek,
              groupedMinutes: {
                [minuteKey] : [formattedMessage]
              }
            });
          }
          this.newMessage = '';  // 메세지 보내고 input 비우기
          this.$nextTick(() => this.scrollToBottom());
          this.loadMessages()
        } catch (error) {
          console.error('메시지 전송 실패:', error);
          alert("메시지 전송에 실패했습니다.");
        }
      } else {
        alert('메시지를 입력하세요')
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    async setIsReadTrue(chatid) {
      try {
        // this.chatId랑 this.userid
        //  {{ this.chatId }}{{ this.user.userid }}
        const response = await axios.post(`http://localhost:5000/setisreadtrue/${chatid}`, {
          userid: this.user.userid
        });
        console.log('is_read를 true로', response.data);
      } catch (error) {
        console.error('Error setting is_read:', error.response.data);
      }
    }
  }
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 화면 전체를 채움 */
}

.chat-container {
  height: 500px;
  flex: 1;
  overflow-y: auto;
  background: #bad0e5;
  padding: 10px;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
}

.sender-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;  /* 메세지 오른쪽 정렬*/
  position: relative;
}

.receiver-wrapper {
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-container {
  display: flex;
  flex-direction: row;
  align-items: flex-end;  /* 시간이랑 말풍선 수직 정렬 */
  max-width: 70%;
  margin-bottom: 6px;
}

.sender {
  background-color: #f7e330; 
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 12px;
  position: relative;
}


.receiver {
  background-color: white;
  border-radius: 4px;
  padding: 6px 10px;
  position: relative;
  margin-right: 7px; 
  font-size: 12px;
}

.info-wrapper {
  width: 50px;
  margin-right: 2px;
}

.receiver-wrapper .time {
  color: #555555;
  font-size: 11px;
  padding-top: 14px;
}
.sender-wrapper .time {
  color: #555555;
  flex-shrink: 0;
  position: absolute;
  bottom: 5px;
  font-size: 11px;
}


/* 읽지 않은 메시지 (1)를 시간 위에 작은 크기로 표시 */
.sender-wrapper .unread-indicator {
  font-size: 11px;
  color: #f7e330;
  text-align: right;
  padding-right: 3px;
  margin-bottom: -2px;
}


.sender.has-tail::after,
.receiver.has-tail::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
}

.sender.has-tail::after {
  border-left: 13px solid #f7e330;
  border-top: 2px solid transparent;
  border-bottom: 10px solid transparent;
  right: -10px; 
  top: 8px;
}

.receiver.has-tail::after {
  border-right: 13px solid white;
  border-top: 2px solid transparent;
  border-bottom: 10px solid transparent;
  left: -10px;
  top: 8px;
}

/* 스크롤바 전체 영역 */
::-webkit-scrollbar {
  width: 10px; /* 세로 스크롤바 너비 */
  height: 10px; /* 가로 스크롤바 높이 */
}

/* 스크롤바 슬라이더 */
::-webkit-scrollbar-thumb {
  background: #a8a8a8; /* 슬라이더 색상 */
  border-radius: 10px; /* 둥근 모서리 */
}

/* 슬라이더에 마우스를 올렸을 때 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 호버 시 색상 */
}


</style>