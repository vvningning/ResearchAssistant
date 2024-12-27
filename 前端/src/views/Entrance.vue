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
            <el-button style="font-size: 24px; padding: 16px 50px; width: 80%" type="primary" @click="enter">
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
