<template>
  <div class="asidePos" @click="OptionCardClose" @contextmenu.prevent="OptionCardClose">
    <div class="background">
      <el-tree
        ref="treeRef"
        class="tree"
        :data="tree_data"
        :props="defaultProps"
        @node-click="handleNodeClick"
        @node-contextmenu="handleNodeContextMenu"
      >
        <template #default="{ node }">
          <el-icon v-if="icon_isfolder(node.label)"><Document /></el-icon>
          <el-icon v-else><Folder /></el-icon>
          <span :class="{ 'active-node': isActiveNode(node) }" style="margin-left: 3px">{{ node.label }}</span>
        </template>
      </el-tree>
      
      <div @contextmenu.prevent v-if="showMenu" :style="{ top: menuY + 'px', left: menuX + 'px' }" class="context-menu">
        <div class="menu-item" @click="addFolder">新建文件夹</div>
        <div class="menu-item" @click="addPDF">新建PDF</div>
        <div class="menu-item" @click="deleteNode">删除节点</div>
      </div>

      <el-dialog title="新增文件夹" v-model="addFolderDialogVisible" width="400px">
        <el-input v-model="newFolderName" placeholder="请输入文件夹名称"></el-input>
        <span slot="footer" class="dialog-footer">
          <el-button @click="confirmAddFolder" type="primary">确定</el-button>
          <el-button @click="addFolderDialogVisible = false">取消</el-button>
        </span>
      </el-dialog>

      <el-dialog title="确认删除" v-model="deleteDialogVisible" width="400px">
        <p>确认删除节点 "{{ deleteNodeLabel }}" 及其所有子节点吗？</p>
        <span slot="footer" class="dialog-footer">
          <el-button @click="confirmDeleteNode" type="danger">确认</el-button>
          <el-button @click="deleteDialogVisible = false">取消</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>
  
  
<script>
  import {defineComponent, ref} from "vue";
  import {
      Document,
      Edit,
      Folder,
      Loading,
  } from '@element-plus/icons'
  import {
    get_nodes_list,
    post_selected_node,
    post_new_folder,
    post_new_document,
    post_deleted_node,
  } from '../api/tree'

  export default {
    name: "tree",
    components:{
      Document,
      Folder,
    },
    data(){
      return {
        tree_data : [
          {
            label: 'root',
            id: 1,
          },
        ],
        nodes_list : [
          {
            name: "",
            type: "",
            path: "",
          },
          // 可以添加更多节点
        ],

        defaultProps : {
          children: 'children',
          label: 'label',
        },

        username : "",
        activeNode: null, // 用于存储当前选中的节点

        showMenu: false,
        menuX: 0,
        menuY: 0,
        selectedNode: null, // 用于保存右键点击的节点

        addFolderDialogVisible: false, // 控制对话框的显示与隐藏
        newFolderName: '', // 存储输入框的值

        sendNode: null, // 用于传递值给对话框

        deleteDialogVisible: false,
        deleteNodeLabel: '',

        clickTimer: null,
        clickDelay: 500, //500ms
      }
    },

    mounted() {

    },

    created() {
      // 页面加载时自动获取数据
      this.get_nodes_list();
    },

    methods: {
      //处理节点点击事件
      handleNodeClick(node){
        this.activeNode = node; // 更新选中的节点
        //返回当前选中节点path
        const active_node = this.nodes_list.find(item => item.name === node.label);

        if (this.clickTimer) {
          // 如果 Timer 存在，说明是双击
          clearTimeout(this.clickTimer);
          this.clickTimer = null;
          if (active_node.type == "document"){
            post_selected_node(active_node.path).then(response => {
              if (response.status === 'success') {
                console.log(response.message);
                sessionStorage.setItem("pdf_file_path", JSON.stringify(response.message));
                this.$router.push({path: '/home/qa', query: {eid:node.id}})
              } else {
                console.log('没拿到path');
              }
            }).catch(error => {
              this.$message.error('请求失败：' + error.message);
            });
          }
        } else {
          // 如果 Timer 不存在，设置一个 Timer
          this.clickTimer = setTimeout(() => {
            this.clickTimer = null;
          }, this.clickDelay);
        }
      },

      // 点击el-tree之外的地方，菜单就消失
      OptionCardClose(event) {
        var currentCli = this.$refs.treeRef; // 获取 el-tree 实例
        if (currentCli) {
          if (!currentCli.$el.contains(event.target)) { 
            this.showMenu = false;
          }
        }
      },
      // 处理右键点击事件
      handleNodeContextMenu(e, data, n, t) {
        this.selectedNode = n; // 保存当前点击的节点
        this.menuX = e.x; // 获取鼠标点击位置
        this.menuY = e.y;
        this.showMenu = true; // 显示上下文菜单
      },
      // 隐藏上下文菜单
      hideMenu() {
        this.showMenu = false;
      },
      // 新增节点
      addFolder() {
        this.sendNode = this.selectedNode;
        this.hideMenu();
        //弹出输入框让用户输入节点名称
        this.newFolderName = '';
        this.addFolderDialogVisible = true;
      },
      confirmAddFolder() {
        if (this.newFolderName.trim() === '') {
          this.$message.warning('请输入有效的文件夹名称');
          return;
        }
        const active_node = this.nodes_list.find(item => item.name === this.sendNode.label);
        //传给后端
        post_new_folder(active_node.path+"+"+this.newFolderName.trim()).then(response => {
          if (response.status === 'success') {
            let newFolderNode = { name: this.newFolderName.trim() , type: "folder", path: response.message };
            this.nodes_list.push(newFolderNode);
            //更新树结构
            this.list_to_tree();
            //刷新显示（有问题，将整个页面刷新显示了，但是我需要的是类似点击当前节点的效果，最好还能懒加载）

            console.log('创建成功');
          } else {
            console.log('创建失败');
          }
        }).catch(error => {
          this.$message.error('请求失败：' + error.message);
        });
        this.addFolderDialogVisible = false; 
      },
      addPDF() {
        //console.log(`新增节点至 ${this.selectedNode.label}`);
        const active_node = this.nodes_list.find(item => item.name === this.selectedNode.label);
        this.hideMenu();
        post_new_document(active_node.path).then(response => {
          if (response.status === 'success') {
            //拆分出路径和文件名（仅保留四位）
            //console.log(response.message);
            const parts = response.message.split("+");
            let newDocumentNode = { name: parts[1], type: "document", path: parts[0] };
            this.nodes_list.push(newDocumentNode);
            //更新树结构
            this.list_to_tree();
            //刷新显示（有问题，将整个页面刷新显示了，但是我需要的是类似点击当前节点的效果，最好还能懒加载）

            console.log('创建成功');
          } else {
            console.log('创建失败');
          }
        }).catch(error => {
          this.$message.error('请求失败：' + error.message);
        });

      },
      // 删除节点
      deleteNode() {
        //console.log(`删除节点 ${this.selectedNode.label}`);
        this.sendNode = this.selectedNode;
        this.deleteNodeLabel = this.selectedNode.label;
        this.hideMenu();
        this.deleteDialogVisible = true;
      },
      confirmDeleteNode() {
        const active_node = this.nodes_list.find(item => item.name === this.sendNode.label);
        
        post_deleted_node(active_node.path).then(response => {
          if (response.status === 'success') {
            console.log('拿到了path');
          } else {
            console.log('没拿到path');
          }
        }).catch(error => {
          this.$message.error('请求失败：' + error.message);
        });
        
        this.nodes_list = this.nodes_list.filter(item => {
          // 保留那些不包含 active_node.path 的节点
          return !item.path.includes(active_node.path) && item.name !== active_node.name;
        });
        console.log(this.nodes_list);
        this.list_to_tree();
        this.$message.success('删除成功');
        this.deleteDialogVisible = false;
      },

      //从后端依据username拿到树状表结构
      get_nodes_list(){
        this.username = JSON.parse(sessionStorage.getItem("username"));
        get_nodes_list(this.username).then(response => {
          if (Array.isArray(response)) {
            this.nodes_list = response.map(item => ({
              name: item.name || "",
              type: item.type || "",
              path: item.path || "",
            }));
          } else {
            console.error("Response is not a valid array.");
          }
          this.list_to_tree();
        })
      },
      //依据树状表结构映射到tree_data
      list_to_tree(){
        let tree = [];
        // 遍历 nodes_list 并构建树
        for (const node of this.nodes_list) {
          //console.log('测试:', node);
          const pathParts = node.path.split('/').filter(Boolean); // 获取路径的各个部分
          let currentLevel = tree;
          for (const part of pathParts) {
            // 在当前层级查找是否已经存在节点
            let existingNode = currentLevel.find(item => item.id === part);
            // 如果不存在需要创建节点
            if (!existingNode) {
              existingNode = { label: node.name, id: part, children: [] };
              currentLevel.push(existingNode);
            }
            // 向下深入到下一个层级
            currentLevel = existingNode.children;
          }
        }
        this.tree_data = tree;
      },
      //依据当前节点node.label找到树状表结构对应节点的类型，进而选择图标
      icon_isfolder(label){
        //console.log('测试1:', label);
        const node = this.nodes_list.find(item => item.name === label);
        if (node) {
          return node.type === "document"; // 如果是 "document" 返回 true，"folder" 返回 false
        }
        // 如果没有找到对应的项，返回false
        return false;
      },
      //当前选中节点变色
      isActiveNode(node){
        return this.activeNode && this.activeNode.label === node.label; // 确定当前节点是否为活动节点
      },
    },

    watch: {
      showMenu(value) {
        if (!value) {
          this.selectedNode = null; // 重置选中的节点
        }
      },
    },
  }

</script>
  

<style scoped>
  .asidePos{
    min-width:200px;
    width: 14.7%;
    min-height: 90vh;
    margin-right: 0.5rem;
    display: inline-block;
  }
  .background{
    height: 98.8%;
    background-color: #ffffff;
  }
  .tree{
    padding-left: 15px;
    padding-top: 15px;
  }
  .active-node {
    color: #409eff; 
  }

  .context-menu {
    position: absolute;
    background-color: white;
    border: 1px solid #ccc;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 1000; /* 确保上下文菜单在其他元素上方 */
  }
  .context-menu div {
    padding: 8px 12px;
    cursor: pointer;
  }
  .context-menu div:hover {
    background-color: #f0f0f0; /* 鼠标悬停时的背景颜色 */
  }
  .menu-item {
    display: flex;                /* 使用 Flexbox 布局 */
    justify-content: center;      /* 水平居中 */
    align-items: center;          /* 垂直居中 */
    height: 40px;                /* 控制高度，使居中效果明显 */
  }

  .dialog-footer {
    margin-top: 18px;
    display: flex;           /* 使用 Flexbox 布局 */
    justify-content: flex-end; /* 将按钮向右对齐 */
  }
</style>
