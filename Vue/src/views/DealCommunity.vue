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
              <el-menu-item index="1">任务中心</el-menu-item>
              <el-menu-item v-if="identity === '志愿者'" index="2">交易社区</el-menu-item>
              <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
            </el-menu>
          <el-popover trigger="hover" popper-style="border: #40b9dc solid 1px; border-radius: 8px" offset="5" width="19vw">
            <template #reference>
              <div class="title-icon">
                <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
              </div>
            </template>

            <template #default>
              <div class="popover" v-if="identity === '志愿者'">
                <el-radio-group v-model="accountNumber">
                  <el-radio-button class="acButton" :value="1">
                    <div class="VAccount">
                      <div style="margin-bottom: 1.5vh">
                        <div style="display: flex; margin-bottom: 1vh">
                          <span class="acText1">地址: {{ address1 }}</span><br>
                          <span class="acText2">交易次数: {{ dealTimes1 }}</span><br>
                          <el-button v-if="accountNumber === 1" class="acClose" :icon="CircleCloseFilled"></el-button>
                          <el-button v-else class="acClose" style="color: #40b9dc" :icon="CircleClose"></el-button>
                        </div>
                        <div style="margin-top: 1.5vh; display: flex">
                          <el-icon v-if="accountNumber === 1" color="white" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <el-icon v-else color="#40b9dc" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <span class="acText3">时间币: &nbsp;</span><span style="font-size: 18px; width: 6vw"> {{ timeCoin1 }}</span>
                          <el-button v-if="accountNumber === 1" class="acWatch">查看</el-button>
                          <el-button v-else class="acNotWatch">查看</el-button>
                        </div>
                      </div>
                    </div>
                  </el-radio-button>
                  <el-radio-button class="acButton" :value="2">
                    <div class="VAccount">
                      <div style="margin-bottom: 1.5vh">
                        <div style="display: flex; margin-bottom: 1vh">
                          <span class="acText1">地址: {{ address2 }}</span><br>
                          <span class="acText2">交易次数: {{ dealTimes2 }}</span><br>
                          <el-button v-if="accountNumber === 2" class="acClose" :icon="CircleCloseFilled"></el-button>
                          <el-button v-else class="acClose" style="color: #40b9dc" :icon="CircleClose"></el-button>
                        </div>
                        <div style="margin-top: 1.5vh; display: flex">
                          <el-icon v-if="accountNumber === 2" color="white" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <el-icon v-else color="#40b9dc" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <span class="acText3">时间币: &nbsp;</span><span style="font-size: 18px; width: 6vw"> {{ timeCoin2 }}</span>
                          <el-button v-if="accountNumber === 2" class="acWatch">查看</el-button>
                          <el-button v-else class="acNotWatch">查看</el-button>
                        </div>
                      </div>
                    </div>
                  </el-radio-button>
                  <el-radio-button class="acButton" :value="3">
                    <div class="VAccount">
                      <div style="margin-bottom: 1.5vh">
                        <div style="display: flex; margin-bottom: 1vh">
                          <span class="acText1">地址: {{ address3 }}</span><br>
                          <span class="acText2">交易次数: {{ dealTimes3 }}</span><br>
                          <el-button v-if="accountNumber === 3" class="acClose" :icon="CircleCloseFilled"></el-button>
                          <el-button v-else class="acClose" style="color: #40b9dc" :icon="CircleClose"></el-button>
                        </div>
                        <div style="margin-top: 1.5vh; display: flex">
                          <el-icon v-if="accountNumber === 3" color="white" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <el-icon v-else color="#40b9dc" size="20px" style="margin-left: 1.2vw"><Coin /></el-icon>
                          <span class="acText3">时间币: &nbsp;</span><span style="font-size: 18px; width: 6vw"> {{ timeCoin3 }}</span>
                          <el-button v-if="accountNumber === 3" class="acWatch">查看</el-button>
                          <el-button v-else class="acNotWatch">查看</el-button>
                        </div>
                      </div>
                    </div>
                  </el-radio-button>
                </el-radio-group>
              </div>
              <div v-if="identity === '志愿者'" style="margin-top: 3vh; margin-left: 8vw">
                <el-button class="add">
                  <el-icon size="2vw"><CirclePlus /></el-icon>
                </el-button>
              </div>
            </template>
          </el-popover>
        </div>
      </el-header>
      <div class="h-separate"></div>
    </el-container>
  </div>
  <div style="display: flex">
    <el-button class="openTask" @click="openDeal">发布交易</el-button>
    <el-input v-model="search" style="width: 11.46vw; margin-left: 50vw; height: 3.5vh; margin-top: 3vh"
            :prefix-icon="Search" placeholder="请输入" clearable/>
    <el-button class="detail" style="margin-left: 10px; margin-right: 0; margin-top: 3vh">搜索</el-button>
    <el-button style="margin-left: 10px; margin-top: 3vh">重置</el-button>
  </div>
  <div style="margin-left: 12vw; width: 80vw" v-loading="loading" element-loading-text="Loading..." :element-loading-spinner="svg"
                  element-loading-svg-view-box="-10, -10, 50, 50" element-loading-background="rgba(122, 122, 122, 0.8)">
    <div style="display: flex;">
      <DealDetail :detail="dealData[0]" style="margin-left: 4vw" :index="1"/>
      <DealDetail :detail="dealData[1]" style="margin-left: 4vw" :index="1"/>
    </div>
    <div style="display: flex;">
      <DealDetail :detail="dealData[2]" style="margin-left: 4vw" :index="1"/>
      <DealDetail :detail="dealData[3]" style="margin-left: 4vw" :index="1"/>
    </div>
    <div style="display: flex;">
      <DealDetail :detail="dealData[4]" style="margin-left: 4vw" :index="1"/>
      <DealDetail :detail="dealData[5]" style="margin-left: 4vw" :index="1"/>
    </div>
  </div>
  <div style="text-align: center; display: flex; margin-left: 20vw; margin-top: 3vh">
    <span style="margin-top: 2vh; margin-left: 20vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
    <el-pagination class="pagination" :current-page="curPage" :page-size="4" :pager-count="6" layout="prev, pager, next" @current-change="change" :total="total"></el-pagination>
  </div>
  <el-dialog width="35%" v-model="dealDetail" :close-on-click-modal="false" :onClose="close">
    <div style="text-align: center; font-size: 32px; font-family: Consolas">发布交易</div>
    <div class="dialog">
      <div class="detailTitle">
        <span>SenderAddress :</span> <br>
        <span>Amount :</span> <br>
        <span>Fees :</span> <br>
        <span>Recipient :</span> <br>
        <span>PrivateKey :</span>
      </div>
      <div class="detailValue">
        <el-form ref="formRef" :model="form" status-icon :rules="rules">
          <el-form-item prop="senderAddress">
            <el-input style="width: 250px; margin-top: 1.8vh; margin-left: 0.5vw" v-model="form.senderAddress" placeholder="请输入"/>
          </el-form-item>
          <el-form-item prop="amount">
            <el-input style="width: 250px; margin-top: 1.5vh; margin-left: 0.5vw" v-model="form.amount" placeholder="请输入"/>
          </el-form-item>
          <el-form-item prop="fees">
            <el-input style="width: 250px; margin-top: 1.5vh; margin-left: 0.5vw" v-model="form.fees" placeholder="请输入"/>
          </el-form-item>
          <el-form-item prop="recipient">
            <el-input style="width: 250px; margin-top: 1.5vh; margin-left: 0.5vw" v-model="form.recipient" placeholder="请输入"/>
          </el-form-item>
          <el-form-item prop="password">
            <el-input style="width: 250px; margin-top: 1.5vh; margin-left: 0.5vw" v-model="form.password" placeholder="请输入" show-password />
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div style="text-align: center">
      <el-button class="plus" @click="up">发布</el-button>
    </div>
    <div style="margin-top: 5vh"></div>
  </el-dialog>
</template>
  
<script setup lang="ts" name="DealCommunity">
  import {reactive, ref, onMounted} from "vue"
  import {CircleClose, CircleCloseFilled, CirclePlus, Search} from "@element-plus/icons-vue"
  import Detail from "../components/Detail.vue"
  import axios from "axios";
  import {ElMessage} from "element-plus";
  import router from "@/router";
  
  const menu = ref("2")
  const identity = localStorage.getItem('identity')
  const username = localStorage.getItem('username')
  const loading = ref(false)
  const search = ref("")
  const total = ref(0)
  const curPage = ref(1)
  const curIndex = ref('1')
  const fullscreenLoading = ref(false)
  const dealDetail = ref(false)
  const accountNumber = ref(1)
  const formRef = ref()
  const form = reactive({
    senderAddress: '',
    amount: '',
    fees: '',
    recipient: '',
    password: ''
  })
  let dealData = reactive([{
    amount: '',
    fees: '',
    miner: '',
    onchain: '',
    recipient: '',
    senderadress: '',
    signature: '',
    tx_nonce: ''
  },])

  const address1 ='asdgre5j7';
  const address2 = 'asedfjh3r';
  const address3 = 'ytrfdcvb3';
  const dealTimes1 = 222;
  const dealTimes2 = 56;
  const dealTimes3 = 3;
  const timeCoin1 = 2311.01;
  const timeCoin2 = 547.50;
  const timeCoin3 = 14.92;

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

  const rules = reactive({
    senderAddress: [
      {required: true, message: "请输入发送者地址", trigger: "blur"}
    ],
    amount: [
      {required: true, message: "请输入金额", trigger: "blur"}
    ],
    fees: [
      {required: true, message: "请输入手续费", trigger: "blur"}
    ],
    recipient: [
      {required: true, message: "请输入接收者地址", trigger: "blur"}
    ],
    password: [
      {required: true, message: "请输入私钥", trigger: "blur"}
    ]
  })

  const handleSelect2 = (index: string) => {
    curIndex.value = index
    if (index === '1') {
      router.push('/home')
    } else if (index === '2') {
      router.push('/dealCommunity')
    } else if (index === '3') {
      router.push('/MyBlock')
    }
  }

  function up() {
    formRef.value.validate((valid: boolean) => {
      if (valid) {
        fullscreenLoading.value = true
        axios.post('http://localhost:5000/sig/tx/publish', {
          sender_adress: form.senderAddress,
          amount: form.amount,
          Fees: form.fees,
          recipient: form.recipient,
          private_key: form.password
        }).then(res => {
          ElMessage.success('发布成功')
          dealDetail.value = false
          load()
        }).catch(() => {
          ElMessage.error('发布失败')
        }).finally(() => {
          fullscreenLoading.value = false
        })
      } else {
        return false
      }
    })
  }

  function openDeal() {
    dealDetail.value = true
  }

  function close() {
    formRef.value.resetFields()
  }

  function change() {
    load()
  }

  function load() {
    loading.value = true
    axios.post('http://localhost:5000/ShowTX', {
      page: curPage.value,
    }).then(res => {
      dealData = reactive([{
        amount: '',
        fees: '',
        miner: '',
        onchain: '',
        recipient: '',
        senderadress: '',
        signature: '',
        tx_nonce: ''
      },])
      Object.assign(dealData, res.data)
      total.value = dealData[dealData.length - 1].num
    }).catch(() => {
      ElMessage.error('加载失败')
    }).finally(() => {
      loading.value = false
    })
  }

  onMounted(() => {
    load()
  })

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

  .popover {
    color: #40b9dc;
    font-size: 16px;
    width: 19vw;
  }

  .title {
    width: 15vw;
    margin: 10px 20px 0;
    background: linear-gradient(to right, rgb(0, 132, 208), rgb(88, 142, 212) 40%, rgb(64, 185, 220));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-family: 'siYuanHeavy';
  }

  /deep/ .acButton .el-radio-button__inner {
    border: 0;
    padding: 0;
    margin-left: 0.75vw;
    margin-top: 1vh;
    margin-bottom: 1.5vh;
    border-radius: 7px;
    --myColor1: #fff;
    --myColor2: #fff;
    --myColor3: #fff;
    background: linear-gradient(to right, var(--myColor1), var(--myColor2) 45%, var(--myColor3));
    color: #40b9dc;
    transition: color 0.5s 0s ease-in-out, --myColor1 0.5s 0s ease-in-out, --myColor2 0.5s 0s ease-in-out, --myColor3 0.5s 0s ease-in-out;
  }

  /deep/ .acButton .el-radio-button__original-radio:hover + .el-radio-button__inner {
    border: 0;
    padding: 0;
    margin-left: 0.75vw;
    margin-top: 1vh;
    margin-bottom: 1.5vh;
    --myColor1: rgba(0, 0, 0, 0.2);
    --myColor2: rgba(0, 0, 0, 0.2);
    --myColor3: rgba(0, 0, 0, 0.2);
    background: linear-gradient(to right, var(--myColor1), var(--myColor2) 45%, var(--myColor3));
    transition: color 0.5s 0s ease-in-out, --myColor1 0.5s 0s ease-in-out, --myColor2 0.5s 0s ease-in-out, --myColor3 0.5s 0s ease-in-out;
    color: rgba(44, 165, 200, 1);
    box-shadow: 0 0 0 0 rgba(64, 185, 220, 0.5);
  }

  /deep/ .acButton .el-radio-button__original-radio:checked + .el-radio-button__inner {
    border: 0;
    padding: 0;
    margin-left: 0.75vw;
    margin-top: 1vh;
    margin-bottom: 1.5vh;
    background: linear-gradient(to right, var(--myColor1), var(--myColor2) 45%, var(--myColor3));
    transition: --myColor1 0.5s 0s ease-in-out, --myColor2 0.5s 0s ease-in-out, --myColor3 0.5s 0s ease-in-out, color 0.5s 0s ease-in-out;
    --myColor1: #0889d1;
    --myColor2: #1d91d3;
    --myColor3: #35accf;
    color: white;
    box-shadow: 0 0 0 0 rgba(64, 185, 220, 0.5);
  }

  .acClose {
    width: 0.1vw;
    background: transparent;
    border: 0;
    color: white;
    margin-left: 0.5vw;
    border-radius: 50px;
  }

  .acClose:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  .acClose:active {
    background: rgba(255, 255, 255, 0.3);
  }

  .acWatch {
    width: 2vw;
    height: 2vh;
    background: rgba(255, 255, 255, 0.3);
    color: white;
    font-size: 12px;
    border: 0;
    border-radius: 6px;
  }

  .acWatch:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  .acWatch:active {
    background: rgba(255, 255, 255, 0.8);
  }

  .acNotWatch {
    width: 2vw;
    height: 2vh;
    background-color: #e3f5fa;
    color: #40b9dc;
    font-size: 12px;
    border: 0;
    border-radius: 6px;
  }

  .acNotWatch:hover {
    background-color: #c6f0ff;
  }

  .acNotWatch:active {
    background-color: #a8eaff;
  }

  .add {
    width: 1.5vw;
    height: 1.5vw;
    color: #40b9dc;
    border-radius: 50px;
    border: 0;
  }

  .add:hover {
    background-color: rgba(64, 185, 220, 0.4);
  }

  .add:active {
    background-color: rgba(64, 185, 220, 0.2);
  }

  .VAccount {
    text-align: left;
    width: 16vw;
    border: #40b9dc solid 1px;
    border-radius: 7px;
  }

  @property --myColor1 {
    syntax: "<color>";
    initial-value: #fff;
    inherits: false;
  }

  @property --myColor2 {
    syntax: "<color>";
    initial-value: #fff;
    inherits: false;
  }

  @property --myColor3 {
    syntax: "<color>";
    initial-value: #fff;
    inherits: false;
  }

  .acText1 {
    margin-left: 1.2vw;
    margin-top: 2vh;
    font-size: 15px;
    width: 7.5vw;
    font-family: "Consolas";
  }

  .acText2 {
    margin-left: 0.5vw;
    margin-top: 2vh;
    font-size: 15px;
    width: 5vw;
    font-family: "Consolas";
  }

  .acText3 {
    margin-left: 0.3vw;
    margin-top: 0.3vh;
    font-size: 15px;
    font-family: "Consolas";
  }

  .openTask {
    width: 8.29vw;
    height: 3.98vh;
    margin-left: 6vw;
    margin-top: 3vh;
    margin-bottom: 3vh;
    background: linear-gradient(to right, rgb(2, 132, 208), rgb(64, 185, 220));
    color: white;
    border-radius: 7px;
  }

  .openTask:hover {
    background: linear-gradient(to right, rgba(2, 132, 208, 0.5), rgba(64, 185, 220, 0.7));
  }

  .openTask:active {
    background: linear-gradient(to right, rgba(2, 132, 208, 0.3), rgba(64, 185, 220, 0.5));
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

  .pagination {
    margin-left: 1vw;
  }

  .dialog {
    line-height: 6vh;
    margin-top: 2vh;
    margin-left: 4vw;
    font-size: 17px;
    display: flex;
  }

  .detailTitle {
    display: block;
    color: #40b9dc;
    width: 8vw;
    text-align: right;
    line-height: 7vh;
  }

  .detailValue {
    display: block;
    width: 24vw;
    float: left;
    color: #606060;
  }

  .plus {
    margin-top: 2vh;
    width: 5vw;
    height: 3.2vh;
    background-color: #40b9dc;
    color: white;
  }

  .plus:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .plus:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

  
</style>