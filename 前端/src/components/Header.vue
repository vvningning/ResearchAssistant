<template>
  <div class="head">
    <!--   logo   -->
    <div style="display: flex; min-width: 200px; width: 15%; height:100%;justify-content: center;align-items: center;">
      <img style="height:80%" src="../assets/images/logo.png" alt="logo">
    </div>
    <div style="border: 1px solid #c8c9cc;border-right: 10px">
    </div>
    <!--   Name   -->
    <div style="display: flex; height:100%; min-width: 180px; width: 40%; margin: auto 1rem;line-height: 60px" @click="toHome()">
      <div style="color: #c60c23; font-weight: bolder; font-family: 华文行楷; font-size: 32px">科研小助手</div>
    </div>
    <!--   右侧按钮   -->
    <div style="height:100%; min-width: 280px; width:45%; margin:auto auto; line-height: 60px; color: #73767a; text-align: right">
      <el-button style="margin: auto 1rem;" circle>
        <div class="el-icon-bell"></div>
      </el-button>
      <span>{{username}}</span>
      <!--退出-->
      <el-button style="margin: auto 1.5rem" circle @click="exit">
        <div class="el-icon-switch-button"></div>
      </el-button>
    </div>
  </div>
</template>

<script>
import {SwitchButton, Edit} from "@element-plus/icons";

export default {
name: "Header",
  computed: {
    SwitchButton() {
      return SwitchButton
    }
  },
  data(){
    return{
      username: '普通用户',
    }
  },
  created(){
    this.username = JSON.parse(sessionStorage.getItem("username"));
  },
  methods:{
    exit(){
      window.sessionStorage.clear();
      this.$router.push('/')
    }
  }

}
</script>

<style scoped>
.head{
  overflow: hidden;
  display:flex;
  height: 60px;
  width:100%;
  margin-bottom: 1rem;
  background-color: #fff;
  box-shadow: 0 1px 3px 0 rgba(204, 204, 204, 0.5);
}
</style>