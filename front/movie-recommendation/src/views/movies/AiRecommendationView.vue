<template>
  <div class="container mt-4">
    <div class="chat-box p-3">
      <div v-for="(message, index) in messages" :key="index" class="mb-3 d-flex align-items-start">
        <img v-if="message.role === 'Bot'" src="@/assets/logo.png" alt="Bot" class="bot-icon me-2" />
        <div :class="message.role === 'User' ? 'user-message ms-auto' : 'bot-message'">
          <p class="mb-0">{{ message.content }}</p>
        </div>
      </div>
      <div class="input-group mt-3">
        <input
          v-model="userInput"
          placeholder="메시지를 입력하세요."
          class="form-control input-transparent"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage" class="btn ms-2" id="sendbtn">보내기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userInput = ref('');
const messages = ref([]);
const typingMessage = ref(null);

const sendMessage = () => {
  if (userInput.value.trim() === '') return;

  const userMessage = {
    role: 'User',
    content: userInput.value,
  };
  messages.value.push(userMessage);

  axios.post('http://127.0.0.1:8000/api/v1/movies/recommend/', {
    input: userInput.value
  })
  .then(response => {
    const fullMessage = response.data.recommendation;
    typingMessage.value = {
      role: 'Bot',
      content: '',
    };
    messages.value.push(typingMessage.value);
    typeMessage(fullMessage);
  })
  .catch(error => {
    console.error('Error getting recommendation:', error);
  });

  userInput.value = '';
};

const typeMessage = async (message) => {
  for (let i = 0; i < message.length; i++) {
    typingMessage.value.content += message[i];
    await new Promise(resolve => setTimeout(resolve, 50)); // 50ms 간격으로 타이핑
  }
  typingMessage.value = null;
  scrollToBottom();
};

const scrollToBottom = () => {
  const chatBox = document.querySelector('.chat-box');
  chatBox.scrollTop = chatBox.scrollHeight;
};

onMounted(() => {
  const initialBotMessage = {
    role: 'Bot',
    content: '안녕하세요! 무슨 영화를 추천해 드릴까요?',
  };
  messages.value.push(initialBotMessage);
  scrollToBottom();
});
</script>

<style scoped>
#sendbtn{
  background-color: #519857;
}
.container {
  background-color: rgba(26, 26, 26, 0.9); /* 반투명 배경색 */
  color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 1400px;
  position: relative;
  height: 76vh;
  display: flex;
  flex-direction: column;
}

.chat-box {
  flex: 1;
  max-height: 70vh;
  overflow-y: auto;
  border-radius: 8px;
  background-color: #2a2a2a;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end; /* 채팅 메시지를 아래로 정렬 */
}

.user-message {
  background-color: #444;
  color: white;
  padding: 10px;
  border-radius: 8px;
  text-align: left;
  max-width: 70%;
}

.bot-message {
  background-color: transparent;
  color: white;
  padding: 10px;
  border-radius: 8px;
  text-align: left;
  max-width: 70%;
}

.bot-icon {
  width: 40px;
  height: 40px;
}

.input-group {
  display: flex;
  align-items: center;
  background-color: #2a2a2a;
  padding: 10px;
  border-radius: 8px;
  margin-top: auto; /* 채팅창의 맨 아래에 위치 */
}

.input-transparent {
  background-color: transparent;
  color: white;
  border: 1px solid #444;
}

.input-transparent::placeholder {
  color: #aaaaaa;
}

.input-transparent:focus {
  background-color: transparent;
  color: white;
  border: 1px solid #888;
  box-shadow: none; /* 포커스 시 흰색 배경 제거 */
}
</style>
  