<template>
  <div class="register-container">
    <h2>注册</h2>

    <!-- 注册表单 -->
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名：</label>
        <input type="text" v-model="username" id="username" placeholder="请输入用户名" required />
      </div>

      <div class="form-group">
        <label for="password">密码：</label>
        <input type="password" v-model="password" id="password" placeholder="请输入密码" required />
      </div>

      <div class="form-group">
        <label for="email">邮箱：</label>
        <input type="email" v-model="email" id="email" placeholder="请输入邮箱" required />
      </div>

      <!-- 发送验证码按钮 -->
      <div class="form-group">
        <button type="button" @click="sendVerificationCode" :disabled="isVerifying">
          {{ isVerifying ? '发送中...' : '发送验证码' }}
        </button>
      </div>

      <!-- 注册提交按钮 -->
      <div class="form-group">
        <button type="submit">注册</button>
      </div>
    </form>

    <!-- 显示验证码发送状态 -->
    <div v-if="verificationStatus" class="status-message">
      {{ verificationStatus }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      verificationStatus: '', // 显示验证码发送状态
      isVerifying: false,      // 是否正在发送验证码
    };
  },
  methods: {
    // 处理注册表单提交
    handleSubmit() {
      // 在此可以添加密码和验证码的验证逻辑

      console.log('注册信息：', {
        username: this.username,
        password: this.password,
        email: this.email,
      });

      // 提交注册请求（可以根据需要替换为实际的注册 API）
      alert('注册成功！');
    },

    // 发送验证码
    async sendVerificationCode() {
      if (!this.email) {
        alert('请输入邮箱地址');
        return;
      }

      // 开始发送验证码请求
      this.isVerifying = true;
      this.verificationStatus = '正在发送验证码...';

      try {
        const response = await axios.post('http://localhost:3000/send-verification', {
          email: this.email,
        });

        if (response.data.success) {
          this.verificationStatus = '验证码已发送，请检查您的邮箱！';
        } else {
          this.verificationStatus = '发送验证码失败，请稍后再试。';
        }
      } catch (error) {
        this.verificationStatus = '发送验证码失败，请稍后再试。';
        console.error('验证码发送失败:', error);
      } finally {
        this.isVerifying = false;
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.form-group button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.form-group button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.form-group button:hover {
  background-color: #45a049;
}

.status-message {
  margin-top: 20px;
  color: green;
  font-size: 14px;
  text-align: center;
}
</style>
