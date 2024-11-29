<template>
<div class="asidePos">
  <el-menu style="min-height: calc(100vh - 76px); height: calc(100% - 45px)"
           class="el-menu-vertical-demo" :default-active="activeIndex" router
           @open="handleOpen()" @close="handleClose()" unique-opened
           @select="handleSelect()">
	  <el-menu-item index="/home/systemInput">
		  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		  <el-icon class="pos-icon" size="medium"><Box/></el-icon>
		  <span style="font-size: 16px">文件A</span>
	  </el-menu-item>
    <el-menu-item index="/home/requirementInfo">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-icon class="pos-icon" size="medium"><Box/></el-icon>
      <span style="font-size: 16px">文件B</span>
    </el-menu-item>

    <el-menu-item index="4">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-icon class="pos-icon" size="medium"><Loading/></el-icon>
      <span style="font-size: 16px">更多功能(待定)</span>
    </el-menu-item>

  </el-menu>
</div>
</template>

<script>
import {defineComponent, ref} from "vue";
import {
	Bicycle,
	Box,
	Connection,
	DataAnalysis,
	Document,
	Edit,
	Folder,
	Goods,
	Grid,
	House,
	Loading,
	MostlyCloudy,
	Operation,
	Paperclip,
	Place,
	Star,
	UploadFilled,
	User
} from '@element-plus/icons'

export default defineComponent({
  name: "Aside",
  components:{
    Grid, House, Paperclip, Edit, UploadFilled, Document,
    Star, Folder, Operation, Connection, DataAnalysis, MostlyCloudy,
    Goods,Bicycle, Box, Place, Loading, User
  },
  setup() {
    const activeIndex = ref('/home/content')
    const handleOpen = (key, keyPath) => {
      console.log(key, keyPath)
    }
    const handleClose = (key, keyPath) => {
      console.log(key, keyPath)
    }
    const sceneSelect = ref('')
    return {
      activeIndex,
      handleOpen,
      handleClose,
      sceneSelect
    }
  },
  data(){
    return{
      sceneOptions:[
        {value: '1', label: '云制造',},
        {value: '2', label: '智慧城市',},
        {value: '3', label: '滴滴',},
        {value: '4', label: '数据服务市场',},
      ]
    }
  },
  mounted() {
    this.activeIndex = this.$route.path
  },
	watch: {
		$route(to, from) {
			this.updateSidebarContent();
		},
	},
  methods:{
    handleSelect(keyPath){
      window.sessionStorage.setItem('keyPath', keyPath);
    },
	  updateSidebarContent(){
		  this.activeIndex = this.$route.path
	  },
    sceneChange(value){
      if(value===null) console.log("qaa")
      console.log(value)
      sessionStorage.setItem("sceneNum",value);
    },
  }
})
</script>

<style scoped>
.asidePos{
  min-width:200px;
  width: 15%;
  margin-right: 1rem;
  display: inline;
}
.pos-icon{
  margin-right: 5%;
}
/deep/ .el-select .el-input__inner {
  text-align: center;
  font-size: 20px;
  font-family: 黑体;
  font-weight: bold;
  --el-input-font-color: #114f8c;
}
/deep/ .el-select {
  --el-select-input-focus-border-color: #e4e7ed;
  display: inline;
}
</style>