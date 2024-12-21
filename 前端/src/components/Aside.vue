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
<!--  <el-tree-->
<!--      style="max-width: 600px"-->
<!--      :data="data"-->
<!--      :props="defaultProps"-->
<!--      @node-click="handleNodeClick"-->
<!--  />-->
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
      ],
      // data: [
      //   {
      //     label: 'Level one 1',
      //     children: [
      //       {
      //         label: 'Level two 1-1',
      //         children: [
      //           {
      //             label: 'Level three 1-1-1',
      //           },
      //         ],
      //       },
      //     ],
      //   },
      //   {
      //     label: 'Level one 2',
      //     children: [
      //       {
      //         label: 'Level two 2-1',
      //         children: [
      //           {
      //             label: 'Level three 2-1-1',
      //           },
      //         ],
      //       },
      //       {
      //         label: 'Level two 2-2',
      //         children: [
      //           {
      //             label: 'Level three 2-2-1',
      //           },
      //         ],
      //       },
      //     ],
      //   },
      //   {
      //     label: 'Level one 3',
      //     children: [
      //       {
      //         label: 'Level two 3-1',
      //         children: [
      //           {
      //             label: 'Level three 3-1-1',
      //           },
      //         ],
      //       },
      //       {
      //         label: 'Level two 3-2',
      //         children: [
      //           {
      //             label: 'Level three 3-2-1',
      //           },
      //         ],
      //       },
      //     ],
      //   },
      // ],
      //
      // // 树形数据字段配置
      // defaultProps: {
      //   children: 'children',
      //   label: 'label',
      // },
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