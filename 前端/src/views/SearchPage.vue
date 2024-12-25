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
          <result-card v-for="(result, index) in leftResultList"
                       :data="result"
                       :key="index"
                       class="result-card">
          </result-card>

        </div>
      </el-col>
      <el-col :span="12">
        <div v-if="leftResultList.length !== 0 || rightResultList.length !== 0">
          <el-divider class="res-divider" content-position="left">BM25检索结果</el-divider>
          <result-card v-for="(result, index) in rightResultList"
                       :data="result"
                       :key="index"
                       class="result-card">
          </result-card>
        </div>
      </el-col>
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
      rightResultList: []
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
            //以后改成从sessions获取
            username: 'user1',
            keyword: this.keyword,
          }
        }).then((response) => {
          this.leftResultList = response
        }).catch(() => {
          this.$messageBox.error("服务器错误")
        })
        request.get("/bm25/", {
          params: {
            //以后改成从sessions获取
            username: 'user1',
            keyword: this.keyword,
          }
        }).then((response) => {
          this.rightResultList = response
        }).catch(() => {
          this.$messageBox.error("服务器错误")
        })
      }
    },
  }
}

</script>

<style scoped>
.main-div {
  position: relative;
  margin-top: 20px;
  width: 80%;
  //left: 10%;
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
