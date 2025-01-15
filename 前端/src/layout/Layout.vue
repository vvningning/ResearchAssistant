<template>
  <div class="background-color">
    <header style="position: sticky;top: 0;z-index:2000" >
      <Header/>
    </header>
    <div style="display: flex">
      <Aside/>
      <router-view style="flex:1;max-width: 1200px; margin: 0 auto;"/>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header";
import Aside from "@/components/Aside.vue";
export default {
  name: "Layout",
  components:{
    Header,
    Aside
  },
  created(){
    window.sessionStorage.setItem("projectId", "96aab941901761a58453875fe606aac2");
    window.sessionStorage.setItem("userIdentify", 0);

  }
}
</script>

<style scoped>
.background-color{
  background-color: #F2F7F7;
  width: 100%;
}
</style>