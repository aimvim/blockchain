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
                
                <el-menu-item  index="2"  @click="taskAH">任务审核</el-menu-item>
                <el-menu-item  index="1">账号审核</el-menu-item>
                
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
        <el-container>
          <el-aside width="20.05vw">
            <div class="option">
              
              <el-menu active-text-color="#303133" background-color="#fff" @select="handleSelect2"
                       text-color="#1b1c1f" class="taskMenu" :default-active="taskMenu">
                <el-menu-item index='2' @click="auditing">未审核</el-menu-item>
                <el-menu-item index='1' @click="passedAccount">已审核</el-menu-item>
              </el-menu>
            </div>
          </el-aside>
          <el-main>
            <div class="search">
              <el-input v-model="search" style="width: 240px"
                        :prefix-icon="Search" placeholder="请输入" clearable/>
            </div>
          <div style="display: flex;margin-top: 1vh;">
            <div class="accountContent">
            <div class="text" id="username">用户名:</div>
            <div class="text" id="department">机构：</div>
            <div class="photoStyle"><img src="../image/pictureNotLoaded.png" alt=""  style="margin-left: 5vw;width: 19vw;margin-top: 4vh;"></div>

          </div>
          <div class="accountContent">
            <div class="text" id="username">用户名:</div>
            <div class="text" id="department">机构：</div>
            <div class="photoStyle"><img src="../image/pictureNotLoaded.png" alt=""  style="margin-left: 5vw;width: 19vw;margin-top: 4vh;"></div>

          </div>
          </div>
          <div style="display: flex;margin-top: 1vh;">
            <div class="accountContent">
            <div class="text" id="username">用户名:</div>
            <div class="text" id="department">机构：</div>
            <div class="photoStyle"><img src="../image/pictureNotLoaded.png" alt=""  style="margin-left: 5vw;width: 19vw;margin-top: 4vh;"></div>

          </div>
          <div class="accountContent">
            <div class="text" id="username">用户名:</div>
            <div class="text" id="department">机构：</div>
            <div class="photoStyle"><img src="../image/pictureNotLoaded.png" alt=""  style="margin-left: 5vw;width: 19vw;margin-top: 4vh;"></div>

          </div>
          </div>

            <div style="text-align: center; display: flex">
              <span style="margin-top: 2vh; margin-left: 20vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
              <el-pagination class="pagination" :page-size="4" :pager-count="6" layout="prev, pager, next" :total="total"></el-pagination>
            </div>
            
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
  
  <script setup lang="ts" name="Home">
    import {reactive, ref} from "vue"
    import {Search} from "@element-plus/icons-vue"


  
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
    const defaultTime = new Date(2000, 1, 1, 8, 0, 0)
    
  
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
    function passedAccount() {
      window.location.href='./passedAccount';
    }
    function auditing() {
        window.location.href='./accountAudit';
    }
    function taskAH() {
      window.location.href='./taskAuditHome';
    }

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
  
    ::v-deep .form .el-form-item__label {
      font-size: 14px;
      color: rgb(120, 120, 120);
      font-family: '黑体';
    }
  
    .dialog {
      margin-top: 2vh;
      margin-left: 3vw;
    }
  
    .popover {
      color: #40b9dc;
      font-size: 16px;
    }
  
    .pText {
      height: 2vh;
      font-family: "黑体";
    }
    .accountContent{
      border: #40b9dc solid 2px;
      margin-left: 2vw;
      border-radius: 0.8vw;
      width: 28vw;
      height: 34vh;
    }
    .text{
      margin-left: 1vw;
      text-align: right;
      width: 4vw;
      height: 4vh;
      color: #40b9dc;
      line-height: 4vh;
    }
    
    
    

  
  </style>