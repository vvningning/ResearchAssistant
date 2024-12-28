<template>
	<div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline;">
	    <el-card style="width: 100%;height: 98%">
		    <div style="display: flex; width: 100%;height: 100%">
          <iframe
              :src="fileUrl"
              id="iframeBox"
              ref="iframeRef"
              style="width: 100%; height: 800px"
          ></iframe>

        </div>
	    </el-card>
    </div>
	</div>
</template>

<script>
import pdf from "vue-pdf"
export default {
  name: "content",
  data() {
    return {
      fileUrl: "../pdf/test.pdf", //文件路径
    };
  },
  components:{
    pdf
  }
}
</script>

<style scoped>

</style>