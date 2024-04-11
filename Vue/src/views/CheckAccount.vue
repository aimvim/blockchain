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
                   class="menu" mode="horizontal" @select="handleSelect1" :ellipsis="false"> <!-- 菜单激活回调 -->
            <el-menu-item index="1" v-if="identity === '用户' || identity === '志愿者'">任务中心</el-menu-item>
            <el-menu-item v-if="identity === '志愿者'" index="2">交易社区</el-menu-item>
            <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
            <el-menu-item v-if="identity === '管理员'" index="4">任务审核</el-menu-item>
            <el-menu-item v-if="identity === '管理员'" index="5">账号审核</el-menu-item>
          </el-menu>
          <div class="title-icon">
            <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
          </div>
        </div>
      </el-header>
      <div class="h-separate"></div>
      <el-container>
        <el-aside width="20.05vw">
          <div class="option">
            <el-menu active-text-color="#303133" background-color="#fff" @select="handleSelect2"
                     text-color="#1b1c1f" class="taskMenu" :default-active="taskMenu">
              <el-menu-item index='1'>未审核</el-menu-item>
              <el-menu-item index='2'>已审核</el-menu-item>
            </el-menu>
          </div>
        </el-aside>
        <el-main>
          <div class="search">
            <div style="display: flex">
              <el-input v-model="search" style="width: 11.46vw" :prefix-icon="Search" placeholder="请输入" clearable/>
              <el-button class="detail" style="margin-left: 10px; margin-right: 0">搜索</el-button>
              <el-button style="margin-left: 10px">重置</el-button>
            </div>
          </div>
          <div v-loading="loading" element-loading-text="Loading..." :element-loading-spinner="svg"
               element-loading-svg-view-box="-10, -10, 50, 50" element-loading-background="rgba(122, 122, 122, 0.8)"
               style="width: 52vw; margin-top: 1vw">
            <div style="display: flex">
              <AccountDetail :detail="acData[0]" :index="curIndex"/>
              <AccountDetail :detail="acData[1]" :index="curIndex" style="margin-left: 5vw"/>
            </div>
            <div style="display: flex">
              <AccountDetail :detail="acData[2]" :index="curIndex" />
              <AccountDetail :detail="acData[3]" :index="curIndex" style="margin-left: 5vw"/>
            </div>
          </div>
          <div style="text-align: center; display: flex">
            <span style="margin-top: 2vh; margin-left: 20vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
            <el-pagination class="pagination" :current-page="curPage" :page-size="4" :pager-count="6" layout="prev, pager, next" @current-change="change" :total="total"></el-pagination>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
  
<script setup lang="ts" name="CheckAccount">
  import {reactive, ref} from "vue"
  import {Search} from "@element-plus/icons-vue"
  import AccountDetail from "@/components/AccountDetail.vue"

  const menu = ref("5")
  const identity = localStorage.getItem('identity')
  const taskMenu = ref('1')
  const search = ref("")
  const curPage = ref(1)
  const loading = ref(false)
  const total = ref(0)
  const curIndex = ref('1')
  const openTask = ref(false)

  import { onMounted } from "vue";
  import axios from "axios";
  import router from "@/router";

  const svg = `
    <path class="path" d="
      M 30 15
      L 28 17
      M 25.61 25.61
      A 15 15, 0, 0, 1, 15 30
      A 15 15, 0, 1, 1, 27.99 7.5
      L 15 15
    " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
  `

  let acData = reactive([{
    username: '',
    proof: '',
    checked: '',
    password: '',
    register_code: '',
    institution: ''
  },])

  function handleSelect1(index: string) {
    if (index === '4') {
      router.push('/home')
    }
  }

  function handleSelect2(index: string) {
    curIndex.value = index
    if (index === '1') {
      load1()
    } else {
      load2()
    }
  }

  function load1() {
    loading.value = true
    axios.post('http://localhost:5000/NtUser', {
      page: curPage.value,
    }).then(res => {
      acData = reactive([{
        username: '',
        proof: '',
        checked: '',
        password: '',
        register_code: '',
        institution: ''
      },])
      Object.assign(acData, res.data)
      if (res.data.length > 1) {
        acData[0].institution = 'Helper Inst.'
        if (res.data.length > 2) {
          acData[1].institution = 'Good Man'
          if (res.data.length > 3) {
            acData[2].institution = 'Global Inc'
            if (res.data.length > 4) {
              acData[3].institution = 'Worldwide'
            }
          }
        }
      }
      total.value = res.data[res.data.length - 1].num
    }).catch(res => {
      console.log(res)
    }).finally(() => {
      loading.value = false
    })
  }

  function load2() {
    loading.value = true
    axios.post('http://localhost:5000/CtUser', {
      page: curPage.value,
    }).then(res => {
      acData = reactive([{
        username: '',
        proof: '',
        checked: '',
        password: '',
        register_code: '',
        institution: ''
      },])
      Object.assign(acData, res.data)
      if (res.data.length > 1) {
        acData[0].institution = 'Helper Inst.'
        if (res.data.length > 2) {
          acData[1].institution = 'Good Man'
          if (res.data.length > 3) {
            acData[2].institution = 'Global Inc'
            if (res.data.length > 4) {
              acData[3].institution = 'Worldwide'
            }
          }
        }
      }
      total.value = res.data[res.data.length - 1].num
    }).catch(res => {
      console.log(res)
    }).finally(() => {
      loading.value = false
    })
  }

  function change(page: number) {
    curPage.value = page
    load1()
  }

  onMounted(() => {
    load1()
  });

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
    white-space: nowrap;
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
    margin-left: 45vw;
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

  .detail {
    margin-right: 10px;
    width: 4vw;
    background-color: #40b9dc;
    color: white;
  }

  .detail:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .detail:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

</style>