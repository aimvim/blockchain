<template>
  <div class="common-layout">
    <el-container>
      <el-header height="8.26vh" style="">
        <div style="display: flex;">
          <div class="title">
            <span style="margin-left: 1.3vw; font-size:1.5vw">时间银行管理系统</span><br>
            <span style="font-size: 0.9vw">Time Bank Management System</span>
          </div>
            <el-menu active-text-color="#fff" text-color="#40b9dc" :default-active="menu"
                     class="menu" mode="horizontal" @select="handleSelect2" :ellipsis="false"> <!-- 菜单激活回调 -->
              <el-menu-item index="1" v-if="identity === '用户'">任务中心</el-menu-item>
              <el-menu-item index="2" v-if="identity === '管理员'">任务审核</el-menu-item>
              <el-menu-item index="3" v-if="identity === '管理员'">账号审核</el-menu-item> <!-- TODO -->
            </el-menu>
          <el-popover popper-style="border: #40b9dc solid 1px; border-radius: 8px" offset="5" width="13vw">
            <template #reference>
              <div class="title-icon">
                <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
              </div>
            </template>
             
            <template #default>
              <div class="popover">
                <span class="pText">用户名：{{ username }}</span>
                <br>
                <span class="pText">机构：{{ institution }}</span>
              </div>
            </template>
          </el-popover> <!-- 用户icon显示信息 -->
        </div>
      </el-header>
      <div class="h-separate"></div>
      
    
    </el-container>

    <div class="content">
      <div class="contenttop" id="backbtn">
        <el-button class="backbtn" @click="goback" :icon="Back">返 回</el-button>
        <p class="taskTitle">任务详情</p>
        <div class="condition" style="color: rgb(120, 120, 120); border: rgb(120, 120, 120) solid 1px;" v-if="checked === 'not'">待审核</div>
        <div class="condition" style="color: rgb(230, 136, 100); border: rgb(230, 136, 100) solid 1px;" v-if="checked === 'yes' && status === 'not finished'">未完成</div>
        <div class="condition" style="color: rgb(102, 183, 153); border: rgb(102, 183, 153) solid 1px;" v-if="checked === 'yes' && status === 'finished'">已完成</div>
      </div>
      <div>
        <div style="display: flex">
          <span class="taskKey">发布用户</span> <span class="taskValue">&nbsp;{{ username }}</span>
          <span class="taskKey" style="margin-left: 0">机构</span> <span class="taskValue">{{ institution }}</span>
        </div>
        <div style="display: flex">
          <span class="taskKey">名称</span> <span class="taskValue">&nbsp;{{ name }}</span>
          <span class="taskKey" style="margin-left: 0">活动区域</span> <span class="taskValue">{{ area }}</span>
        </div>
        <div style="display: flex">
          <span class="taskKey">活动时长</span> <span class="taskValue">&nbsp;{{ duration }} 小时</span><br>
          <span class="taskKey" style="margin-left: 0">活动奖励</span> <span class="taskValue">{{ award }} 时间币</span><br>
        </div>
        <span class="taskKey">活动日期</span> <span class="taskValue" style="width: 25vw">{{ date }}</span><br>

        <span class="taskKey">性质</span> <span class="taskValue">{{ type }}</span><br>
        <div style="display: flex;">
          <span class="taskKey">活动内容</span>
          <div id="taskContent" style="margin-top: 1vw; padding: 10px; word-wrap: break-word">
            <el-scrollbar height="6vw">{{ details }}</el-scrollbar>
          </div>
        </div>

        <div>
          <span class="taskKey" style="vertical-align: middle">证明材料</span>
          <span v-if="index === '5' || index === '6'" class="taskValue" style="vertical-align: middle">
            <img v-if="proof !== '' && proof !== 'picture'" :src="proof" alt="">
            <img v-else src="../assets/imgs/pictureNotLoaded.png" alt="图片未加载">
          </span>
        </div>

        <!-- TODO: 图片 -->
        <div class="button" v-if="index === '3' || index === '5'">
          <el-button class="passBtn" @click="passMission" v-loading.fullscreen.lock="fullscreenLoading">通过</el-button>
          <el-button class="RefuseBtn" @click="refuse">不通过</el-button>
        </div>
      </div>
    </div>
  </div>

</template>


<script setup lang="ts" name="TaskDetail">
  import { onMounted, reactive, ref } from "vue"
  import { useRoute } from "vue-router"
  import { Back } from "@element-plus/icons-vue"
  import {ElMessage, ElMessageBox} from "element-plus";
  import axios from "axios";

  const menu = ref("1")
  const identity = localStorage.getItem('identity')
  const fullscreenLoading = ref(false)

  function goback() {
    window.history.go(-1);
  }

  const { query } = useRoute()
  const { id, index, name, area, date, duration, award, type, details, checked, status, username, institution, proof } = query

  function selectMenu() {
    if (identity === '用户') {
      menu.value = '1'
    } else if (identity === '管理员') {
      menu.value = '2'
    }
  }

  function refuse() {
    ElMessage.warning('已拒绝')
    goback()
  }

  function passMission() {
    ElMessageBox.confirm('是否通过该任务？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      fullscreenLoading.value = true
      if (index === '3') {
        axios.post('http://localhost:5000/passmission', {
          id: id
        }).then(res => {
          if (res.status === 200) {
            ElMessage.success('操作成功')
            window.history.go(-1)
          }
        }).catch(() => {
          ElMessage.info('通信错误')
        })
      } else if (index === '5') {
        axios.post('http://localhost:5000/PassProof', {
          id: id
        }).then(res => {
          if (res.status === 200) {
            ElMessage.success('操作成功')
            window.history.go(-1)
          }
        }).catch(() => {
          ElMessage.info('通信错误')
        }).finally(() => {
          fullscreenLoading.value = false
        })
      }
    }).catch(() => {
      ElMessage.info('已取消')
    }).finally(() => {
      fullscreenLoading.value = false
    })
  }

  onMounted(() => {
    selectMenu()
  })
</script>


<style scoped>
  .title {
    width: 15vw;
    margin: 10px 20px 0;
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

  .popover {
    color: #40b9dc;
    font-size: 16px;
  }

  .pText {
    line-height: 4vh;
    font-family: "黑体";
    font-size: 16px;
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

  .backbtn{
    margin-left: 17.5vw;
    margin-top: 7.13vh;
    width: 6.25vw;
  }

  .contenttop {
    display: flex;
  }

  .taskTitle {
    width: max-content;
    margin-top: 3vw;
    font-size: 1.7vw;
    margin-left: 5.5vw;
  }

  /deep/ .el-scrollbar__view {
      overflow-x: hidden;
  }

  .taskKey {
    display: inline-block;
    margin-left: 29.5vw;
    margin-top: 1vw;
    line-height: 3vh;
    width: 6vw;
    text-align: left;
    font-weight: 600;
  }

  .taskValue {
    display: inline-block;
    margin-top: 1vw;
    margin-left: 0;
    line-height: 3vh;
    width: 15vw;
  }

  #taskContent {
    display: inline-block;
    margin-top: 2vw;
    width: 29vw;
    height: 6vw;
    border: #40b9dc solid 1px;
    border-radius: 3px;
  }

  .condition {
    margin-top: 7.8vh;
    flex-basis: 80px;
    margin-left: 35px;
    font-size: 14px;
    text-align: center;
    height: 22px;
    line-height: 22px;
    color: rgb(64, 185, 220);
    border-radius: 25px;
    border: rgb(64, 185, 220) solid 1px;
  }

  .button {
    display: flex;
    margin-top: 2vw;
    margin-left: 42vw;
  }

  .passBtn {
    width: 4vw;
    background-color: #40b9dc;
    color: white;
  }

  .passBtn:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .passBtn:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

  .RefuseBtn {
    background-color: #f89898;
    color: white;
    width: 4vw;
    margin-left: 1vw;
  }

  .RefuseBtn:hover {
    background-color: rgba(248, 152, 152, 0.5);
  }

  .RefuseBtn:active {
    background-color: rgba(248, 152, 152, 0.3);
  }

</style>