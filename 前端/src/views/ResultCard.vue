<template>
  <div>
    <el-card class="main-card">
      <template #header>
        <div class="header" style="height: 20px; text-align: left; font-weight: bold">
          <el-link v-html="data.name" @click="jump()"></el-link>
        </div>
      </template>
      <p v-html="data.content"></p>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "ResultCard",
  props: ['data'],
  methods: {
    jump() {
      this.$router.push({path: '/home/qa', query: {eid:this.data.eid}})
    }
  }
}
</script>

<style scoped>
.main-card /deep/ .el-card__body {
  padding: 10px 40px;
}

.main-card /deep/ .el-card__header {
  background: #F8F8F8;
  padding: 15px 40px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
}

.el-link--default {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.el-link--default:hover {

  color: #409eff;
}

</style>
