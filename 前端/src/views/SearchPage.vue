<template>
  <div class="main-div">
    <el-backtop :right="50" :bottom="100"/>
    <el-input v-model="keyword" placeholder="请输入搜索关键词" @keyup.enter="searchKeyword">
      <template #append>
        <el-button icon="Search" @click="searchKeyword">搜索</el-button>
      </template>
    </el-input>

    <div v-if="leftResultList.length === 0 && rightResultList.length === 0">
      <div class="empty-div">
        <el-empty description=" "/>
        <el-alert title="请在上方输入框内输入关键词，点击搜索按钮或按下回车显示相关内容" type="info" :closable="false" show-icon/>
      </div>
    </div>

    <el-row :gutter="40">
      <el-col :span="12">
        <div v-if="leftResultList.length !== 0 || rightResultList.length !== 0">
          <el-divider class="res-divider" content-position="left">字符串匹配检索结果</el-divider>
          <result-card v-for="(result, index) in leftResultListShow"
                       :data="result"
                       :key="index"
                       class="result-card">
          </result-card>

        </div>
      </el-col>
      <el-col :span="12">
        <div v-if="leftResultList.length !== 0 || rightResultList.length !== 0">
          <el-divider class="res-divider" content-position="left">BM25检索结果</el-divider>
          <result-card v-for="(result, index) in rightResultListShow"
                       :data="result"
                       :key="index"
                       class="result-card">
          </result-card>
        </div>
      </el-col>
      <el-pagination v-if="leftResultList.length !== 0 || rightResultList.length !== 0"
          @current-change="pageChange"
          v-model:current-page="page"
          :page-size="pageSize"
          layout="prev, pager, next, jumper"
          :total="totalEntry"
          style="margin: 20px">
      </el-pagination>
    </el-row>
  </div>
</template>

<script>
import ResultCard from "@/views/ResultCard";
import request from "@/utils/request";


export default {
  name: "SearchPage",
  components: {
    ResultCard
  },
  data() {
    return {
      keyword: '',
      leftResultList: [],
      rightResultList: [],
      leftResultListShow: [],
      rightResultListShow: [],
      page: 1,
      pageSize: 3,
      totalEntry: 0,
    }
  },
  methods: {
    searchKeyword() {
      if (this.keyword === '' || this.keyword == null) {
        this.leftResultList = []
        this.rightResultList = []
      } else {
        request.get("/strmatch/", {
          params: {
            username: this.$route.query.username,
            keyword: this.keyword,
          }
        }).then((response) => {
          this.leftResultList = response
          this.page = 1
          this.totalEntry = Math.max(this.leftResultList.length, this.rightResultList.length)
          this.pageChange()
        }).catch(() => {
          this.$messageBox.error("服务器错误")
        })
        request.get("/bm25/", {
          params: {
            username: this.$route.query.username,
            keyword: this.keyword,
          }
        }).then((response) => {
          this.rightResultList = response
          this.page = 1
          this.totalEntry = Math.max(this.leftResultList.length, this.rightResultList.length)
          this.pageChange()
        }).catch(() => {
          this.$messageBox.error("服务器错误")
        })
      }
    },
    pageChange() {
      this.leftResultListShow = this.leftResultList.slice((this.page-1) * this.pageSize,this.page * this.pageSize)
      this.rightResultListShow = this.rightResultList.slice((this.page-1) * this.pageSize,this.page * this.pageSize)
    }
  }
}

</script>

<style scoped>
.main-div {
  position: relative;
  margin-top: 20px;
  width: 80%;
}

.result-card {
  position: relative;
  margin: 16px 0;
}

.empty-div {
  position: relative;
  width: 50%;
  left: 25%;
  margin-top: 150px;
}

.res-divider /deep/ .el-divider__text {
  background-color: rgb(242, 247, 247);
}
</style>
