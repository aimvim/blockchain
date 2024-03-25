<template>
  <div class="common-layout">
    <el-container>
      <el-header height="8.26vh" style="">
        <div style="display: flex;">
          <div class="title">
            <span style="margin-left: 13px; font-size: 28px">时间银行管理系统</span><br>
            <span style="font-size: 15px">Time Bank Management System</span>
          </div>
            <el-menu active-text-color="#fff" text-color="#40b9dc" :default-active="menu"
                     class="menu" mode="horizontal" @select="handleSelect1" :ellipsis="false"> <!-- 菜单激活回调 -->
              <el-menu-item index="1">任务中心</el-menu-item>
              <el-menu-item v-if="identity === '志愿者'" index="2">交易社区</el-menu-item>
              <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
            </el-menu>
          <div class="title-icon">
            <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
          </div>
          <div class="user">
            <!-- TODO: 补充个人信息界面 -->
          </div>
        </div>
      </el-header>
      <div class="h-separate"></div>
      <el-container>
        <el-aside width="20.05vw">
          <div class="option">
            <el-button class="openTask" @click="openTask = true">发布任务</el-button>
            <el-menu active-text-color="#303133" background-color="#fff" @select="handleSelect2"
                     text-color="1b1c1f" class="taskMenu" :default-active="taskMenu">
              <el-menu-item index='1'>已发布</el-menu-item>
              <el-menu-item index='2'>进行中</el-menu-item>
              <el-menu-item index='3'>已完成</el-menu-item>
            </el-menu>
          </div>
        </el-aside>
        <el-main>
          <div class="search">
            <el-input v-model="search" style="width: 240px"
                      :prefix-icon="Search" placeholder="请输入" clearable/>
          </div>
          <div style="display: flex">
            <Detail :index="curIndex"/>
            <Detail :index="curIndex"/>
          </div>
          <div style="display: flex">
            <Detail :index="curIndex"/>
            <Detail :index="curIndex"/>
          </div>
          <div style="text-align: center; display: flex">
            <span style="margin-top: 2vh; margin-left: 20vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
            <el-pagination class="pagination" :page-size="4" :pager-count="6" layout="prev, pager, next" :total="total"></el-pagination>
          </div>
          <el-dialog width="30%" v-model="openTask" title="发布任务" :close-on-click-modal="false" :onClose="reset">
           <div style="margin-left: 80px">
             <el-form :model="data.form2" label-width="100px" label-position="right" style="padding-right: 25px" ref="formRef" :rules="rules" status-icon>
               <p style="margin-left: 45px"> 原成绩：{{ data.grade !== undefined ? data.grade : '' }} </p>
               <el-row>
                 <el-col :span="12">
                   <el-form-item label="新成绩" prop="grade">
                     <el-input v-model.number="data.form2.grade" autocomplete="off" />
                   </el-form-item>
                 </el-col>
               </el-row>
             </el-form>
           </div>
           <template #footer>
             <span class="dialog-footer">
               <el-button type="danger" @click="close2">取 消</el-button>
               <el-button v-loading.fullscreen.lock="fullscreenLoading2" type="primary" @click="saveGrade">保 存</el-button>
             </span>
           </template>
         </el-dialog>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts" name="Home">
  import {reactive, ref} from "vue"
  import {Search} from "@element-plus/icons-vue";
  import Detail from "./Detail.vue"

  const menu = ref("1")
  const identity = localStorage.getItem('identity')
  const taskMenu = ref('1')
  const search = ref("")
  const total = ref(6532)
  const curIndex = ref('1')
  const openTask = ref(false)
  const formRef = ref()
  const form = reactive({
    name: "",
    location: "",
    time: "",

    description: ""
  })

  const handleSelect2 = (index: string) => {
    console.log(index)
    curIndex.value = index
  }

  // TODO：查询，任务详情，发布任务，交互信息，分页

</script>

<style scoped>
  .title {
    width: 15vw;
    margin: 10px 25px 0;
    background: linear-gradient(to right, rgb(0, 132, 208), rgb(88, 142, 212) 40%, rgb(64, 185, 220));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-family: 'siYuanHeavy';
  }

  .menu {
    background-color: #fff;
    height: 9.02vh;
    width: calc(3 * 9.32vw);
    border: 0;
  }

  .menu .el-menu-item {
    font-size: 17px;
    width: 9.32vw;
  }

  .menu .el-menu-item:hover{
    background-color: rgb(84, 205, 255);
    color: #fff;
  }

  .menu .el-menu-item.is-active {
    color: #fff;
    background: #40b9dc;
    z-index: 100;
    border-bottom-color: blue;
    box-shadow: 0 -5px 15px -12px blue inset;
  }

  .title-icon {
    margin-left: 40.52vw;
    margin-top: 1.5vh;
    width: 2.92vw;
    height: 6vh;
    background: linear-gradient(to bottom, rgb(2, 132, 208), rgb(66, 181, 219));
    border-radius: 50%;
  }

  .h-separate {
    margin-top: 5px;
    content: "";
    width: 100%;
    height: 2px;
    background-color: rgb(64, 185, 220);
    z-index: 50;
  }

  .option {
    margin-top: 4.91vh;
    margin-left: 7.42vw;
  }

  .openTask {
    width: 8.29vw;
    height: 3.98vh;
    margin-left: 0.8vw;
    background: linear-gradient(to right bottom, rgb(2, 132, 208), rgb(64, 185, 220));
    color: white;
    border-radius: 7px;
  }

  .openTask:hover {
    background: linear-gradient(to right bottom, rgba(2, 132, 208, 0.5), rgba(64, 185, 220, 0.5));
  }

  .openTask:active {
    background: linear-gradient(to right bottom, rgba(2, 132, 208, 0.3), rgba(64, 185, 220, 0.3));
  }

  .taskMenu {
    margin-top: 3.15vh;
    border-radius: 7px;
    width: 9.79vw;
    border: rgba(64, 185, 220, 0.5) solid 1px;
    font-family: '黑体';
  }

  .taskMenu .el-menu-item {
    font-size: 15px;
  }

  .taskMenu .el-menu-item.is-active {
    background-color: rgba(64, 185, 220, 0.5);
  }

  :deep(.taskMenu .el-menu-item:first-child) {
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
  }

  :deep(.taskMenu .el-menu-item:last-child) {
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }

  .search {
    margin-left: 52vw;
    margin-top: 3vh;
  }

  .pagination {
    margin-top: 2vh;
    margin-left: 1vw;
  }

</style>