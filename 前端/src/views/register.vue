<template>
  <div class="register-container">
    <video class="background-video" autoplay muted loop>
      <source src="@/assets/bg.mp4" type="video/mp4" />
      您的浏览器不支持视频播放。
    </video>

    <h2>注册</h2>

    <!-- 注册表单 -->
    <form @submit.prevent="handleSubmit" style="border: transparent">
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

      <div class="form-group">
        <label for="verification">验证码：</label>
        <input id="verification" v-model="verification" placeholder="请输入验证码" required />
      </div>

      <!-- 发送验证码按钮 -->
      <div class="form-group">
        <button type="button" @click="sendVerificationCode" :disabled="isVerifying">
          {{ isVerifying ? '发送中...' : '发送验证码' }}
        </button>
      </div>

      <!-- 注册提交按钮 -->
      <div class="form-group">
        <button type="submit" @click="register">注册</button>
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
import {register, sendVerification} from "@/api/register";

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      verification: '',
      verificationStatus: '', // 显示验证码发送状态
      isVerifying: false,      // 是否正在发送验证码
      sentVerification: ''
    };
  },
  methods: {
    // 处理注册表单提交
    register() {
      if (this.sentVerification !== this.verification)
        alert('验证码错误！')
      else
        // 在此可以添加密码和验证码的验证逻辑
        register(this.username, this.password, this.email, this.verification, this.sentVerification).then(response => {
          if (response.res === 1) {
            alert('用户名已被使用，请更换用户名！')
            this.$router.push({path:'/register'})
          }
          else {
            alert('注册成功！')
            sessionStorage.setItem("username", JSON.stringify(this.username));
            this.$router.push({path:'/home/searchPage',query: {username:this.username}})
          }
        })
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
      this.sentVerification = '-1'

      sendVerification(this.email).then(response => {
        try {
          if(response) {
            this.sentVerification = response.verification_code;
            console.log(this.sentVerification)
            this.verificationStatus = '验证码已发送，请检查您的邮箱！';
          } else {
            this.verificationStatus = '发送验证码失败，请稍后再试。';
          }
        }  catch (error) {
          this.verificationStatus = '发送验证码失败，请稍后再试。';
          console.error('验证码发送失败:', error);
        } finally {
          this.isVerifying = false;
        }
      })
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

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持视频覆盖整个背景 */
  z-index: -1; /* 确保视频在其他内容下面 */
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
