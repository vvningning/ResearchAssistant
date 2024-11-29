import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from "@/layout/Layout.vue";

const routes = [
  {
    path: '/home',
    name: 'Layout',
    component: AdminLayout,
    meta: {
      title: "用例生成",
      icon: "shopping-basket-2-fill"
    },
    children:[
      {
        path: '/home',
        redirect:'/home/content',
      },
      {
        path: 'content',
        name: 'content',
        component: () => import("@/views/content.vue")
      }
    ]
  },
  {
    path: '/',
    name: 'Entrance',
    component: () => import("@/views/Entrance.vue"),
    meta: {
      title: "欢迎登陆",
      icon: "shopping-basket-2-fill"
    },
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to,from,next)=>{
  return next();
  // const userIdentify = window.sessionStorage.getItem("userIdentify");
  // if(to.path==='/')
  //   return next();
  // if(userIdentify === '0'){
  //   if(to.path === '/admin' || to.path === '/admin/admin_project' || to.path === '/admin/topic_distribute'
  //       || to.path === '/admin/team_distribute' || to.path === '/admin/view_total_score'
  //       || to.path === '/admin/check_firm_topic' || to.path === '/admin/View_log'
  //       || to.path === '/admin/Administrator_score' || to.path === '/admin/View_file')
  //     return next();
  //   else{
  //     return next('/');
  //   }
  // }
  // else if(userIdentify === '1'){
  //   if(to.path === '/student' || to.path === '/student/applyRecords'
  //       || to.path === '/student/team_member' || to.path === '/student/team_member_innovation'
  //       || to.path === '/student/team_leader_innovation' || to.path === '/student/team_leader'
  //       || to.path === '/student/team' || to.path === '/student/chooseTeam'
  //       || to.path === '/student/showTopic' || to.path === '/student/log'
  //       || to.path === '/student/studentScore')
  //     return next();
  //   else{
  //     return next('/');
  //   }
  // }
  // else{
  //   if(to.path === '/teacher' || to.path === '/teacher/teacher_topic' || to.path === '/teacher/teacher_create_topic'
  //       || to.path === '/teacher/teacher_topic_check' || to.path === '/teacher/teacher_score'
  //       || to.path === '/teacher/teacher_examine')
  //     return next();
  //   else{
  //     return next('/')
  //   }
  // }
})
export default router
