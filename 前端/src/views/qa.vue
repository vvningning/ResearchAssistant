<template>
  <div class="container">
    <div class="left-panel">
      <el-card style="width: 100%; height: 20%">
        <div style="display: flex; width: 100%; height: 100%">
          论文关键词
          <p>{{ keywords }}</p>
        </div>
      </el-card>
      <el-card style="width: 100%; height: 80%; margin-top: 10px">
        <div style="display: flex; width: 100%;height: 100%">
          <iframe
              :src="fileUrl"
              id="iframeBox"
              ref="iframeRef"
              style="width: 100%; height: 800px"
          ></iframe>
          <p>{{ content }}</p>
        </div>
      </el-card>
    </div>
    <div class="right-panel">
      <div style="display: flex; flex-direction: column; height: 100%">
        <!-- 聊天记录部分 -->
        <el-card class="chat-card" style="position: relative;">
          <div style="position: absolute; right: 15px; top: 0">
            <el-dropdown @command="handleCommand" trigger="click" :dropdown-append-to-body="true">
              <el-button type="text">
                <img src="../assets/images/more.png" alt="更多功能" width="20"/>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu style="white-space: nowrap;">
                  <el-dropdown-item command="clear" style="display: flex; align-items: center;">
                    <img src="../assets/images/clearMsg.png" alt="清空聊天" height="20" style="margin-right: 10px" />
                    清空聊天内容
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>

          <div style="margin-bottom: 15px"></div>

          <div v-for="(message, index) in chatMessages" :key="index" class="chat-message">
            <!-- 用户消息 -->
            <div v-if="message.role === 'user'" class="message" style="justify-content: flex-end;">
              <div class="message-user">
                {{ message.text }}
              </div>
              <img src="../assets/images/user.png" width="30" style="margin-left: 5px; transform: translateY(20%);" alt="user" />
            </div>

            <!-- Bot 消息 -->
            <div v-else class="message">
              <img src="../assets/images/bot.png" width="30" style="margin-right: 5px; transform: translateY(20%);" alt="bot" />
              <div class="message-bot">
                {{ message.text }}
              </div>
            </div>
          </div>
        </el-card>
        <div style="display: flex; margin-top: 10px">
          <el-input style="margin-right: 10px" v-model="question" type="textarea" placeholder="请输入问题，按 Shift+Enter 换行" @keydown="handleKeyDown" :disabled="isInputDisabled" />
          <el-button type="primary" @click="sendQuestion" :disabled="isButtonDisabled">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  sendQuestion, showChatHistory, clearChat
} from '../api/chat'
import pdf from "vue-pdf"

export default {
  name: "qa",
  data() {
    return {
      question: '',
      fileUrl: "../pdf/test.pdf",
      chatMessages: [],
      isInputDisabled: false,
      isButtonDisabled: false,
      typingInterval: null
    }
  },
  created() {
    this.showChatHistory();
  },
  methods: {
    showChatHistory() {
      showChatHistory(this.$route.query.eid).then(response => {
        this.chatMessages = response.msg;
      })
    },

    sendQuestion() {
      if (!this.question.trim()) {
        console.warn("输入内容不得为空");
        return;
      }
      this.isInputDisabled = true;
      this.isButtonDisabled = true;
      this.chatMessages.push({role: 'user', text: this.question});
      console.log('发送的问题:', this.question);
      this.chatMessages.push({role: 'bot', text: '.'});
      this.startTypingEffect();

      sendQuestion(this.question, this.$route.query.eid).then(response => {
        this.question = '';
        this.isInputDisabled = false;
            this.stopTypingEffect();
        this.chatMessages[this.chatMessages.length - 1].text = '';
        this.displayBotMessage(response.ans);
      })
    },

    // 启动动态“...”效果
    startTypingEffect() {
      let dotCount = 1;
      this.typingInterval = setInterval(() => {
        const botMessage = this.chatMessages[this.chatMessages.length - 1];
        if (dotCount < 3) {
          botMessage.text += '.';
          dotCount++;
        } else {
          botMessage.text = '.';
          dotCount = 1;
        }
      }, 500);
    },

    // 停止动态“...”效果
    stopTypingEffect() {
      if (this.typingInterval) {
        clearInterval(this.typingInterval);
        this.typingInterval = null;
      }
    },

    // 显示 Bot 消息的打字效果
    displayBotMessage(message) {
      let index = 0;
      const fullMessage = message;
      const botMessage = this.chatMessages[this.chatMessages.length - 1];

      // 设置定时器逐个字符显示
      const typingInterval = setInterval(() => {
        botMessage.text += fullMessage.charAt(index);  // 逐个字符添加到消息中
        index++;

        if (index === fullMessage.length) {
          clearInterval(typingInterval);
          this.isButtonDisabled = false;
        }
      }, 10);
    },

    // 监听键盘事件
    handleKeyDown(event) {
      // 如果按下 Shift + Enter 就插入换行符
      if (event.key === 'Enter' && event.shiftKey) {
        return;
      }

      // 如果按下 Enter 键
      if (event.keyCode === 13 && !event.shiftKey) {
        event.cancelBubble = true;
        event.stopPropagation();
        event.preventDefault();
        if (!this.isButtonDisabled)
          this.sendQuestion();
      }
    },

    clearChat() {
      if (this.chatMessages.length === 0) return;

      this.$confirm('您确定要清空聊天记录吗?', '确认清空', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        clearChat(this.$route.query.eid).then(response => {
          if (response.status === 'success') {
            this.chatMessages = [];
          } else {
            this.$message.error('删除失败：' + response.message);
          }
        }).catch(error => {
          this.$message.error('请求失败：' + error.message);
        });
      });
    },

    handleCommand(command) {
      if (command === 'clear') {
        this.clearChat();
      }
    }
  },
  components:{
    pdf
  }
}
</script>

<style scoped>
  .container {
    display: flex;
    padding: 20px;
    height: 1000px;
  }

  .left-panel {
    width: 65%;
    padding-right: 20px;
  }

  .right-panel {
    width: 35%;
    border-left: 1px solid #ccc;
    padding-left: 20px;
  }

  .chat-card {
    width: 100%;
    height: 100%;
    overflow-y: auto;
    padding: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .chat-message {
    margin-bottom: 15px;
  }

  .message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 15px;
  }

  .message-user {
    padding: 10px;
    color: #003472;
    max-width: 80%;
    text-align: left;
    white-space: pre-line;
    word-break: break-word;
    word-wrap: break-word;
  }

  .message-bot {
    padding: 10px;
    background-color: #e9e9e9;
    border-radius: 8px;
    max-width: 80%;
    text-align: left;
    white-space: pre-line;
    word-break: break-word;
    word-wrap: break-word;
  }
</style>