<template>
  <div class="container">
    <div class="left-panel">
      <el-card style="width: 100%; height: 20%">
        <div style="display: flex; width: 100%;height: 100%">
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
        <el-card style="width: 100%; height: 100%">
          <div v-for="(message, index) in chatMessages" :key="index">
            <strong>{{ message.sender }}:</strong> {{ message.text }}
          </div>
        </el-card>
        <div style="display: flex; margin-top: 10px">
          <el-input style="margin-right: 10px" v-model="question" type="text" placeholder="请输入问题" />
          <el-button type="primary" @click="sendQuestion">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  sendQuestion
} from '../api/chat'
import pdf from "vue-pdf"

export default {
  name: "qa",
  data() {
    return {
      question: '',
      ans: '',
      fileUrl: "../pdf/test.pdf",
      chatMessages: []
    }
  },
  created() {

  },
  methods: {
    sendQuestion() {
      sendQuestion(this.question).then(response => {
        this.ans = response.ans;
        this.chatMessages.push({sender: this.question, text: this.ans})
        console.log('发送的问题:', this.chatMessages);
      })
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
</style>