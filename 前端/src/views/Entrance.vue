<template>
  <div class="background" style="display: inline; text-align: center; width: 100%">
    <div style="height: 100%">
      <el-card style="width: 30%; margin: auto auto; margin-top: 5rem; min-width: 500px;">
        <div style="display: inline">
          <!-- 用户名输入框 -->
          <div style="line-height: 40px; margin: 5px 0">
            <el-input
                v-model="username"
                placeholder="请输入用户名"
                style="width: 80%; margin: auto auto; font-size: 16px; padding: 10px"
            />
          </div>

          <!-- 密码输入框 -->
          <div style="line-height: 40px; margin: 5px 0">
            <el-input
                v-model="password"
                placeholder="请输入密码"
                type="password"
                style="width: 80%; margin: auto auto; font-size: 16px; padding: 10px"
            />
          </div>

          <!-- 登录按钮 -->
          <div style="line-height: 40px; margin: 5px 0">
            <el-button
                style="font-size: 24px; padding: 16px 50px"
                type="primary"
                @click="enter"
            >
              登录
            </el-button>
          </div>

          <!-- 注册按钮 -->
          <div style="line-height: 40px; margin: 5px 0">
            <el-button
                style="font-size: 24px; padding: 16px 50px"
                @click="register"
            >
              注册
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <div style="width: 100%; margin-top: 1rem">
      <p style="color: #c8c9cc">
        注：此按钮仅用于测试，正式投入使用后根据用户登录身份自动判断
      </p>
    </div>

    <div style="margin-top: 38rem; color: #b1b3b8">
      Copyright © By 高级软工小组 All Rights Reserved
    </div>
  </div>
</template>

<script>
import request from "@/utils/request";
import { ref } from "vue";

export default {
  name: "Entrance",
  setup() {
    const username = ref("");
    const password = ref("");
    return {
      username,
      password,
    };
  },
  data() {
    return {
      projects: [],
    };
  },
  created() {
    // 用户登录后存在的session为用户id，用户name，用户identify
    // 根据用户id查询选课表，得到用户该学年的所有选课信息并获取其id，依次遍历每个选课id，匹配项目表中正在进行的项目
    // 匹配成功则返回projectId到前端，并展示其名称（projectId与按钮绑定）
    // this.load();
  },
  methods: {
    // 找出当前正在进行中的、且该学生选了课的项目
    load() {
      let i = 0;
      // 写死该学生的学号，其实是登录时存在session中
      // 项目实训
      request.get("/pTrainProject/getOnGoingProject", {
        params: {},
      }).then((res) => {
        if (res !== null && res.length !== 0) {
          // 有一个项目实训项目正在进行中
          // 下面到项目实训学生团队表看看该学生是否选了该课。
          request.get("/pTrainStudentTeam/getStudentTeam", {
            params: {
              stuId: sessionStorage.getItem("userId"),
            },
          }).then((res1) => {
            if (res1 !== null) {
              // 该学生选了该项目实训课
              this.projects[i++] = res.project_id;
            }
          });
        }
      });

      // 认识实习
      request.get("/pAwareProject/getOnGoingProject", {
        params: {},
      }).then((res) => {
        if (res !== null && res.length !== 0) {
          // 有一个项目实训项目正在进行中
          // 下面到项目实训学生团队表看看该学生是否选了该课。
          request.get("/pAwareStudentTeam/getStudentTeam", {
            params: {
              stuId: sessionStorage.getItem("userId"),
            },
          }).then((res1) => {
            if (res1 !== null) {
              // 该学生选了该项目实训课
              this.projects[i++] = res.project_id;
            }
          });
        }
      });

      // 校内外实习（尚未实现）
    },
    enter() {
      // 登录操作
      if (this.username && this.password) {
        this.$router.push("/home");
      } else {
        this.$message.error("用户名或密码不能为空");
      }
    },
    register() {
      // 注册操作（可以添加跳转到注册页面的代码）
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
/* 背景样式：设置一个动感渐变效果 */
.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 50%;
  background: linear-gradient(45deg, #ff6a00, #ee0979, #ffb400, #4f5f96);
  background-size: 300% 300%;
  animation: gradientBG 15s ease infinite;
  z-index: -1; /* 确保背景不会遮挡内容 */
}

/* 动态渐变动画 */
@keyframes gradientBG {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
