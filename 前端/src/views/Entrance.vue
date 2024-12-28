<template>
  <div class="background" style="text-align: center">
    <div class="content">
      <el-card style="width: 30%; margin: auto auto; min-width: 500px">
        <div style="display: inline">
          <div style="line-height: 40px; margin: 5px 0">
            <el-input
                v-model="username"
                placeholder="请输入用户名"
                style="width: 80%; margin: auto auto; font-size: 16px; padding: 10px"
            />
          </div>

          <div style="line-height: 40px; margin: 5px 0">
            <el-input
                v-model="password"
                placeholder="请输入密码"
                type="password"
                style="width: 80%; margin: auto auto; font-size: 16px; padding: 10px"
            />
          </div>

          <div style="line-height: 40px; margin: 5px 0">
            <el-button style="font-size: 24px; padding: 16px 50px; width: 80%" type="primary" @click="sendUser">
              登录
            </el-button>
          </div>

          <div style="line-height: 40px; margin: 5px 0">
            <el-button style="font-size: 24px; padding: 16px 50px; width: 80%" @click="register">
              注册
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {
  sendUser
} from '../api/login'
import axios from "axios";

export default {
  name: "login",
  data() {
    return{
      username: '',
      loginSuccess: null,
    }
  },
  created() {

  },
  methods: {
    sendUser() {
      sendUser(this.username, this.password).then(response => {
        // 获取后端返回的数据
        const data = response.data;
        console.log('用户名:', response.username);
        // 判断登录是否成功
        if (response.username !== undefined && response.res !== undefined) {
          this.username = response.username;  // 更新前端的用户名
          this.loginSuccess = response.res;   // 获取登录结果（成功/失败）

          this.$router.push({path:'/home/content',query: {username:this.username}})
        } else {
          console.error('后端返回的数据格式不正确');
        }
      })
    },

    register() {
      this.$router.push({path:'/register'})
    }
  }
}
</script>

<style scoped>
/* 背景渐变样式 */
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at top right, rgba(255, 188, 143, 0.8), rgba(250, 112, 154, 0.6), rgba(63, 94, 251, 0.5));
  background-size: 300% 300%;
  animation: smoothGradient 10s infinite linear;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* 内容居中对齐 */
.content {
  z-index: 1;
}

/* 平滑渐变动画 */
@keyframes smoothGradient {
  0% {
    background-position: top right;
  }
  50% {
    background-position: bottom left;
  }
  100% {
    background-position: top right;
  }
}
</style>
