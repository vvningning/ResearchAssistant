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
        <div v-if="leftResultList.length !== 0">
          <el-divider content-position="left">传统检索结果</el-divider>
          <result-card v-for="(result, index) in leftResultList"
                       :data="result"
                       :key="index"
                       class="result-card">
          </result-card>

        </div>
      </el-col>
      <el-col :span="12">
        <div v-if="rightResultList.length !== 0">
          <el-divider content-position="left">大模型检索结果</el-divider>
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
import ResultCard from "@/views/ResultCard.vue";

export default {
  name: "SearchPage",
  components: {
    ResultCard
  },
  data() {
    return {
      keyword: '',
      size: 0,
      leftResultList: [],
      rightResultList: []
    }
  },
  methods: {
    searchKeyword() {
      this.leftResultList = [
        {
          title:'基于监督<font color="red">机器学习</font>的配电网电力智能运维检修研究_邵芳.pdf',
          text:'提出一种基于监督<font color="red">机器学习</font>的配电网配电变压器风' +
              '险筛选策略。首先介绍实物资产风险管理的行业要求，' +
              '然后采用案例研究和行动研究相结合的方法，将资产风' +
              '险管理方法和有监督的<font color="red">机器学习</font>算法有机结合'
        },
        {
          title:'基于CT平扫影像组学特征机...囊性肾占位性病变的诊断效能_尚晓静.pdf',
          text:'因此，本研究通过基于 CT平扫的影像组学特征建立 CRM 诊断<font color="red">机器学习</font>算法模' +
              '型，并进行内外部数据验证，以及与放射科医师的手动诊断效能进行比较，从而进一步验证' +
              '<font color="red">机器学习</font>算法模型对CRM诊断的效能。'
        },
        {
          title:'基于对抗神经网络的力学试验机故障诊断系统设计_国雪.pdf',
          text:'关于<font color="red">机器学习</font>在故障诊断' +
              '中的适用性，近年来众多专家学者也进行了大量' +
              '研究，研究的关键点主要集中在传统<font color="red">机器学习</font>算' +
              '法建立[1－5]方面。 基于<font color="red">机器学习</font>的'
        },
        {
          title:'基于多输入高斯过程回归的震级快速估算方法_赵庆旭.pdf',
          text:'相较人为定义的经验' +
              '公式，<font color="red">机器学习</font>的优势在于可以自动地建立更为复杂的输入与输出关系，实现更为精准的预' +
              '测。<font color="red">机器学习</font>的震级估算方法'
        },
      ]
      this.rightResultList = [
        {
          title:'基于多输入高斯过程回归的震级快速估算方法_赵庆旭.pdf',
          text:'本文基于<font color="red">机器学习</font>领域的高斯过程回归（Gaussian processes regression，缩写为 GPR）提出' +
              '了一种多输入的震级估算方法。'
        },
        {
          title:'基于CT平扫影像组学特征机...囊性肾占位性病变的诊断效能_尚晓静.pdf',
          text:'以构建朴素贝叶斯、梯度提升算法（GBM）及主' +
              '成分分析（PCA）的监督与非监督影像组学算法模型，进行验证集验证，在珠海分院 45 例（外部测试集）中完成外部' +
              '测试。使用 ROC 曲线评估<font color="red">机器学习</font>算法模型诊断效能',
        },
        {
          title:'基于对抗神经网络的力学试验机故障诊断系统设计_国雪.pdf',
          text:'欲设计力学试验机故障诊断的<font color="red">机器学习</font>' +
              '算法，首先应建立<font color="red">机器学习</font>所需的知识库。 本课' +
              '题选择已标定的无故障电子万能试验机'
        },
        {
          title:'基于迁移学习的煤矸图像识别方法_张释如.pdf',
          text:'逻辑回归等<font color="red">机器学习</font>算法结合构建煤矸识别模型，其' +
              '模型结构如图 2 所示。' +
              '图 2 VGG16 卷积基与<font color="red">机器学习</font>算法结合'
        },
        {
          title:'基于交互式多头注意力的机械故障诊断方法_冯肖亮.pdf',
          text:'dddd'
        },
      ]
    },
  }
}
</script>

<style scoped>
.main-div {
  position: relative;
  margin-top: 20px;
  width: 99%;
  left: auto;
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
</style>
