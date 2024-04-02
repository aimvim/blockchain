<template>
    <div class="common-layout">
      <el-container>
        <el-header height="8.26vh" style="">
          <div style="display: flex;">
            <div class="title">
              <span style="margin-left: 0.4vw; font-size:1.65vw">时间银行管理系统</span><br>
              <span style="font-size: 0.9vw">Time Bank Management System</span>
            </div>
              <el-menu active-text-color="#fff" text-color="#40b9dc" :default-active="menu"
                       class="menu" mode="horizontal" @select="handleSelect2" :ellipsis="false"> <!-- 菜单激活回调 -->
                
                <el-menu-item  index="1">任务审核</el-menu-item>
                <el-menu-item  index="2">账号审核</el-menu-item>
                
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
                  <br>
                  <span class="pText">机构：电子科技大学</span>
                </div>
              </template>
            </el-popover><!-- 用户icon显示信息 -->
          </div>
        </el-header>
        <div class="h-separate"></div>
        
      
      </el-container>

      <div class="content">
        <div class="contenttop" id="backbtn">
          <button class="backbtn" @click="goback()" >⬅返回</button>
          <p class="taskTitle">任务详情</p>
          <div id="status">状态</div>
        </div>
        <div contentbody>
          <span class="taskKey">发布用户</span> <span class="taskValue">{{ releaseUser }}</span><br>
          <span class="taskKey">机构</span> <span class="taskValue">{{ department }}</span><br>
          <span class="taskKey">名称</span> <span class="taskValue">{{ taskName }}</span><br>
          <span class="taskKey">活动区域</span> <span class="taskValue">{{ taskArea }}</span><br>
          <span class="taskKey">活动日期</span> <span class="taskValue">{{ taskDate }}</span><br>
          <span class="taskKey">活动时长</span> <span class="taskValue">{{ taskDuring }}</span><br>
          <span class="taskKey">活动奖励</span> <span class="taskValue">{{ taskPaidBack }}</span><br>
          <span class="taskKey">性质</span> <span class="taskValue">{{ taskType }}</span><br>
          <span class="taskKey" style="vertical-align:140%;">活动内容</span> <div class="taskValue" id="taskContent" >{{ taskContent }}</div>
        </div>
      </div>
    </div>

</template>


<script setup lang="ts" name="taskAudit">
import {reactive, ref} from "vue"
import {Search} from "@element-plus/icons-vue"
import Detail from "./Detail.vue"
import { dataType } from "element-plus/es/components/table-v2/src/common.mjs";

const menu = ref("1")
const identity = localStorage.getItem('identity')
const username = localStorage.getItem('username')
const taskMenu = ref('1')
const search = ref("")
const total = ref(6532)
const curIndex = ref('1')
const openTask = ref(false)
const fullscreenLoading = ref(false)
const formRef = ref()
const form = reactive({
  name: "",
  location: "",
  time: "",
  trait: [],
  description: ""
})



const handleSelect2 = (index: string) => {
  console.log(index)
  curIndex.value = index
}

function reset() {
  formRef.value.resetFields()
}

function close() {
  reset()
  openTask.value = false
}



// add for this page



function goback() {
  window.history.go(-1);
}
var releaseUser='namenamename';
var department='电子科技大学';
var taskName='任务名称';
var taskArea='活动区域';
var taskDate='time';
var taskDuring='xxhrs';
var taskPaidBack='奖励';
var taskType='活动性质';
var taskContent='活动内容活动内容活动内容活动内容活动内容活动内容活动内容活动内容活动内容活动内容活动内容活活动内容活动内容活动内容动内';

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
    white-space:nowrap; 
    
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
  .backbtn{
    
    border:0 ;
    border-radius: 8%;
    font-size: 1vw;
    color: gray;
    margin-top: 5vw;
    background-color: rgb(223,240,246);
    margin-left: 17vw;
    width: 7vw;
    height: 2vw;

  }
  .contenttop{
    display: flex;
  }
  .taskTitle{
    width: max-content;
    margin-top: 3vw;
    font-size: 1.7vw;
    margin-left: 5.5vw;
  }
  #status{
    border-radius: 3vw;
    border: green solid 1px;
    width: 3.6vw;
    margin-top:3.5vw;
    margin-left: 0.9vw;
    height: 1.4vw;

    font-size: 1vw;
    text-align: center;
    color: green;
  }
  .taskKey{
    display: inline-block;
    margin-left: 29.5vw;
    margin-top: 1.4vw;
    width: 8vw;

    text-align: left;
    font-weight:600;
  }
  .taskValue{
    margin-left: 2vw;
    
  }
  #taskContent{
    display: inline-block;
    margin-top: 2vw;
    width: 40vw;
    height: 10vw;
    border: #40b9dc solid 1px;
    border-radius: 3px;
  }
  

  

</style>