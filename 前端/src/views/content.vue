<template>
	<div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline;">
	    <el-card style="width: 100%;height: 98%">
		    <div style="display: flex; width: 100%;height: 100%">
          <iframe 
              id="iframe" 
              name="iframe" 
              height="100%" 
              width="100%" 
              :src="`/pdfUtils/web/viewer.html?file=${pdfPath}`"
              scrolling="auto" 
              frameborder="0">
          </iframe>
          <div v-if="selectedText" class="tooltip" :style="tooltipStyle">
            <span>{{ translatedText }}</span>
          </div>
        </div>
	    </el-card>
    </div>
	</div>
</template>


<script>
import axios from 'axios'
import md5 from 'js-md5'
export default {
  data() {
    return {
      pdfPath: '/pdf/GraphGPT.pdf',
      selectedText: '',
      translatedText: '',
      tooltipStyle: {
        top: '0px',
        left: '0px',
        display: 'none',
      }
    }
  },
  mounted() {
    // 页面加载完成后，修改框架高度
    this.changeFrameHeight();
    this.getSelectedText();

    // 窗口大小调整时重新计算框架高度
    window.onresize = () => {
      this.changeFrameHeight();
    }
  },
  methods: {
    // 获取选中的文本
    getSelectedText() {
      const iframe = document.getElementById('iframe');
      let x = '';
      let y = '';
      let _x = '';
      let _y = '';

      iframe.onload = () => {
        // 鼠标点击监听
        iframe.contentDocument.addEventListener('mousedown', (e) => {
          this.selectedText = '';
          this.translatedText = '';
          this.tooltipStyle.display = 'none';
          x = e.pageX;
          y = e.pageY;
        }, true);

        // 鼠标抬起监听
        iframe.contentDocument.addEventListener('mouseup', (e) => {
          _x = e.pageX;
          _y = e.pageY;
          if (x === _x && y === _y) return; // 如果点击和抬起位置相同，则视为没有选中

          this.tooltipStyle.display = 'block';
          this.tooltipStyle.top = `${_y + 20}px`;
          this.tooltipStyle.left = `${_x + 20}px`;

          let choose = iframe.contentWindow.getSelection().toString();
          this.selectedText = choose.replace(/[\r\n]/g, " ");
          console.log(this.selectedText);
          this.translateText(this.selectedText);
        }, true);
      };
    },

    // 改变iframe高度
    changeFrameHeight() {
      let iframe = document.getElementById("iframe");
      iframe.height = document.documentElement.clientHeight;
    },

    // 翻译文本
    translateText(text) {
      let appid = '20241230002241792';
      let secretkey = 'ly0fKph1cR04HNQJrCFP';
      let from = 'en';
      let to = 'zh';
      let salt = Date.parse(new Date()) / 1000;
      let sign = md5(appid + text + salt + secretkey);
      let url2 = '/baiduapi';

      axios({
        headers: {
          "Content-Type": 'application/x-www-form-urlencoded',
        },
        data: {
          q: text,
          from: from,
          to: to,
          appid: appid,
          salt: salt,
          sign: sign
        },
        method: 'POST',
        url: url2,
      }).then((data) => {
        console.log(data);
        this.translatedText = data.data.trans_result[0].dst;
        console.log(this.translatedText);
      }).catch((resp) => console.warn(resp));
    }
  }
}
</script>

<style scoped>
.tooltip {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 14px;
  z-index: 10;
  width: 200px;
}
</style>