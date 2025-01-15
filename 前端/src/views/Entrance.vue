<template>
  <div class="background" style="text-align: center">
    <!-- 背景视频 -->
    <video class="background-video" autoplay muted loop>
      <source src="@/assets/bg.mp4" type="video/mp4" />
      您的浏览器不支持视频播放。
    </video>
    <div class="readpaper" style="display:flex; font-family: cambria; font-size: 30px; position:absolute; left: 5%; top: 5%">
      <img src="../assets/images/paper.png" width="45">
      &nbsp;&nbsp;ReadPaper
    </div>
    <div class="content" style="font-family: coca_cola; font-size: 50px; margin: 20px;">
      <div class="text">
        极简科研工具，高效阅读论文
      </div>
      <div class="card" style="background-color: transparent; border-color: transparent; width: 25%; margin: auto auto; min-width: 500px">
        <div style="display: inline">
          <div class="username" style="line-height: 40px; margin: 10px 0">
            <input
                v-model="username"
                placeholder="请输入用户名"
                style="padding-left:12px; padding-right: 12px; height:45px; width: 80%; border: #5856D5 3px solid; border-radius: 7px; margin: auto auto; font-size: 16px"

            />
          </div>

          <div class="password" style="line-height: 40px; margin: 5px 0">
            <input
                v-model="password"
                placeholder="请输入密码"
                type="password"
                style="padding-left:12px; padding-right: 12px; height:45px; width: 80%; border: #5856D5 3px solid; border-radius: 7px; margin: auto auto; font-size: 16px"
            />
          </div>

          <div class="login" style="line-height: 40px; margin: 10px 0">
            <el-button style="font-family:'华康俪金黑W8'; font-size: 20px; padding: 12px; width: 75%" type="primary" @click="sendUser">
              登&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;录
            </el-button>
          </div>

          <div style="line-height: 40px; margin: 10px 0">
            <el-button style="font-family:'华康俪金黑W8'; font-size: 20px; padding: 12px; padding: 10px; width: 75%" @click="register">
              注&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;册
            </el-button>
          </div>
        </div>
      </div>
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
      password: '',
      loginSuccess: null,
    }
  },
  created() {

  },
  methods: {
    sendUser() {
      sendUser(this.username, this.password).then(response => {
        // 判断登录是否成功
        if (response.username !== undefined && response.res) {
          this.username = response.username;  // 更新前端的用户名
          this.loginSuccess = response.res;   // 获取登录结果（成功/失败）
          alert('登录成功！')
          sessionStorage.setItem("username", JSON.stringify(this.username));
          this.$router.push({path:'/home/searchPage',query: {username:this.username}})
        } else if (!response.res) {
          alert('用户名或密码输入错误！')
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
/* 背景视频样式 */
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1; /* 确保视频不覆盖其他内容 */
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

/* 内容居中对齐 */
.content {
  z-index: 1;
  padding-top: 6%;
}

.text {
  padding: 20px;
  margin-bottom: 50px; /* 控制两个div之间的空隙 */
}

.login {
  margin-top: 50px;
}

.username {
  margin-top: 20px;
}

.username:focus {
  border-color: white;
}

.icon-search {
  background: url(../assets/images/paper.png) no-repeat;
  width: 20px;
  height: 20px;
  position: absolute;
  top: 0;
  left: 0;
}

.password {
  margin-bottom: 50px;
}

/* 视频的平滑过渡动画可以不需要，背景视频通常不需要动感 */
</style>
