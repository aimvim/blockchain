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
              <el-menu-item index="1">任务审核</el-menu-item>
              <el-menu-item index="2">账号审核</el-menu-item> <!-- TODO -->
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
        <span class="taskKey">活动日期</span> <span class="taskValue" style="width: 25vw">{{ date }}</span><br>
        <span class="taskKey">活动时长</span> <span class="taskValue">{{ duration }}</span><br>
        <span class="taskKey">活动奖励</span> <span class="taskValue">{{ award }}</span><br>
        <span class="taskKey">性质</span> <span class="taskValue">{{ type }}</span><br>
        <div style="display: flex;">
          <span class="taskKey">活动内容</span>
          <div style="margin-top: 1vw; padding: 10px" id="taskContent" >{{ details }}</div><br>
        </div>

        <span class="taskKey"><img :src="proof !== '' ? proof : '../assets/imgs/pictureNotLoaded.png'" alt="图片未加载"></span>
        <!-- TODO: 图片 -->

      </div>
    </div>
  </div>

</template>


<script setup lang="ts" name="AdminTaskDetail">
import { reactive, ref } from "vue"
import { useRoute } from "vue-router"
import { Back } from "@element-plus/icons-vue"

const menu = ref("1")
const username = localStorage.getItem('username')
const institution = localStorage.getItem('institution') !== "" ? localStorage.getItem('institution') : "无" // 可能 bug

// add for this page

function goback() {
  window.history.go(-1);
}

const { query } = useRoute()
const { name, area, date, duration, award, type, details, checked, status, proof } = query
console.log(type)

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
  width: 30vw;
  height: 7vw;
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

</style>