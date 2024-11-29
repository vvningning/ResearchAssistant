<template>
  <div style="display: inline;text-align: center;width: 100%">
    <div style="height: 100%">
      <el-card style="width: 30%;margin: auto auto; margin-top:5rem; min-width: 500px;">
        <div style="display: inline">
          <div style="line-height: 40px;margin: 5px 0">
            <el-button style="font-size: 24px;padding:16px 50px" type="primary" @click="enter">进入系统</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <div style="width:100%;margin-top: 1rem">
      <p style="color: #c8c9cc">注：此按钮仅用于测试，正式投入使用后根据用户登录身份自动判断</p>
    </div>

    <div style="margin-top: 38rem;color: #b1b3b8">
      Copyright © By 高级软工小组 All Rights Reserved
    </div>
  </div>


</template>

<script>
import request from "@/utils/request";
import { ref } from 'vue'

export default {
  name: "Entrance",
  setup(){
    const value = ref(true)
    return{
      value,
    }
  },
  data(){
    return{
      projects:[],
    }
  },
  created() {
    // 用户登录后存在的session为用户id，用户name，用户identify
    // 根据用户id查询选课表，得到用户该学年的所有选课信息并获取其id，
    // 依次遍历每个选课id，匹配项目表中正在进行的项目
    // 匹配成功则返回projectId到前端，并展示其名称（projectId与按钮绑定）
    // this.load();
  },
  methods:{
    //找出当前正在进行中的、且该学生选了课的项目
    load(){
      let i=0;
      //写死该学生的学号，其实是登录时存在session中
      //项目实训
      request.get("/pTrainProject/getOnGoingProject",{
        params: {}
      }).then(res => {
        if (res!==null&&res.length!==0){//有一个项目实训项目正在进行中
          //下面到项目实训学生团队表看看该学生是否选了该课。
          request.get("/pTrainStudentTeam/getStudentTeam",{
            params: {
              stuId:sessionStorage.getItem("userId"),
            }
          }).then(res1 => {
            if (res1!==null){//该学生选了该项目实训课
              this.projects[i++]=res.project_id;
            }
          })
        }
      })

      //认识实习
      request.get("/pAwareProject/getOnGoingProject",{
        params: {}
      }).then(res => {
        if (res!==null&&res.length!==0){//有一个项目实训项目正在进行中
          //下面到项目实训学生团队表看看该学生是否选了该课。
          request.get("/pAwareStudentTeam/getStudentTeam",{
            params: {
              stuId:sessionStorage.getItem("userId"),
            }
          }).then(res1 => {
            if (res1!==null){//该学生选了该项目实训课
              this.projects[i++]=res.project_id;
            }
          })
        }
      })

      //校内外实习（尚未实现）
    },
    enter(){
      this.$router.push('/home')
    },
  }
}
</script>

<style >

</style>