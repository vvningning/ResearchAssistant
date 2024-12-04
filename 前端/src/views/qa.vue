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
          论文内容
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
          <el-input style="margin-right: 10px" v-model="userInput" type="text" placeholder="请输入问题" />
          <el-button type="primary" @click="sendQuestion">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "qa"
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