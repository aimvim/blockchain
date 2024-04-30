<template>
  <div class="common-layout">
    <el-container>
      <el-header height="8.26vh" style="">
        <div style="display: flex;">
          <div class="title" style="margin-left: 0">
            <span style="margin-left: 1.3vw; font-size: 1.5vw">智慧养老服务平台</span><br>
            <span style="font-size: 0.8vw">Smart Elderly Care Service Platform</span>
          </div>
          <el-menu active-text-color="#fff" text-color="#40b9dc" :default-active="menu"
                   class="menu" mode="horizontal" @select="handleSelect2" :ellipsis="false"> <!-- 菜单激活回调 -->
            <el-menu-item index="1">任务中心</el-menu-item>
            <el-menu-item v-if="identity === '志愿者'" index="2">交易社区</el-menu-item>
            <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
          </el-menu>
          <el-popover popper-style="border: #40b9dc solid 1px; border-radius: 8px" offset="5" width="19vw">
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
      <el-container>
      <el-main style="display: flex; padding: 0">
        <div class="leftcontent">
          <div class="chain" ><div class="line" style="margin-left: 5vw;"></div>
            <el-button class="block" :icon="ZoomIn" style="margin-left: 8vw" @click="fake"></el-button>
            <el-button class="block" :icon="ZoomIn"></el-button>
            <el-button class="block" :icon="ZoomIn"></el-button>
            <el-button v-if="flag === true" class="block" :icon="ZoomIn"></el-button>
          </div>
          <hr color=#40b9dc SIZE=1>
          <button class="dealbtn">交易</button>
          <div style="width: 63vw;" v-loading="loading" element-loading-text="Loading..." :element-loading-spinner="svg"
                  element-loading-svg-view-box="-10, -10, 50, 50" element-loading-background="rgba(122, 122, 122, 0.8)">
            <div style="display: flex;">
              <DealDetail :detail="dealData[0]" style="margin-bottom: 3vh" :index="2"/>
              <DealDetail :detail="dealData[1]" style="margin-bottom: 3vh" :index="2"/>
            </div>
            <div style="display: flex;">
              <DealDetail :detail="dealData[2]" style="margin-bottom: 3vh" :index="2"/>
              <DealDetail :detail="dealData[3]" style="margin-bottom: 3vh" :index="2"/>
            </div>
          </div>
          <div style="text-align: center; display: flex; margin-top: 2vh; margin-left: 5vw">
            <span style="margin-top: 2vh; margin-left: 17vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
            <el-pagination class="pagination" :current-page="curPage" :page-size="4" :pager-count="6" layout="prev, pager, next" @current-change="change" :total="total"></el-pagination>
          </div>
        </div>
        <div class="rightcontent">
          <div class="righttop" style="height: 55%;">
            <span class="infoKey" style="margin-top: 6vh;">version</span>1.0 <br>
            <span class="infoKey">prehash</span>a8fdc205a9f19cc1c7507a60c4f01b13d11d7fd0<br>
            <span class="infoKey">index</span>4<br>
            <span class="infoKey">nonce</span>7.26<br>
            <span class="infoKey">markle_root</span>as5sda56wer5cc1sad5548a77a6fgh7n7fw66gh<br>
            <span class="infoKey">target</span>7<br>
            <button class="rightbtn" @click="commit" v-loading.fullscreen.lock="fullscreenLoading">提交</button>
          </div>
          <hr color=#40b9dc SIZE=1>
          <div style="text-align: center; font-family: Consolas; font-size: 24px; margin-top: 1vh">JSON</div>
          <div class="rightbottom">
            <el-scrollbar>
              <div style="word-break: break-all">
                { <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "txid": "000000000000000000000000000000000000000000000000000000000000000", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "size": 205, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "version": 2, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "locktime": 0, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "fee": 1232, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "inputs": [ <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp; { <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"coinbase": false, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"txid": "3a37b81f3e916adfe121e593a8ddb74717e11195a24387da1a20715ffdf773d6", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"output": 1, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"sigscript": "", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"sequence": 4294967293, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"pkscript": "5120e0383d30ff85a28d7cbd4b97e6deee1c1486b1616ee70e24d4c15689ea7d5070", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"value": 158842, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"address": "1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;"witness": [ <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"bfbd7f959a8d235a555c31d5ac646f189941a1aab9a2b51af4da419f7dd9fe907be254b3eb13f45a2e88f5812734fb56900f7486bbaaa7a93ef45e5b1996a673" <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;] <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp; } <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; ], <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "outputs": [ <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;{ <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"address": "1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"pkscript": "512027afe9959d0316ca80bccdf6ced1c22c57ccbf4d99f98e1dd9ff69ef181fb48e", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"value": 1762, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"spent": true, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"spender": { <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"txid": "6455a82939ae19f748dfc4ed21fc02c2ed69cfaba25a3f9da7173e8acfcb2921", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"input": 0 <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;} <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;}, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;{ <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"address": "1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"pkscript": "5120e0383d30ff85a28d7cbd4b97e6deee1c1486b1616ee70e24d4c15689ea7d5070", <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"value": 155848, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"spent": false, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;"spender": null <br>
                  &nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;} <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; ], <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "block": { <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;  "mempool": 1712391064 <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; }, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "deleted": false, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "time": 1712391064, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "rbf": true, <br>
                  &nbsp;&nbsp;&nbsp;&nbsp; "weight": 616 <br>
                } <br>
              </div>
            </el-scrollbar>
          </div>
        </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
  
<script setup lang="ts" name="MyBlock">
import {onMounted, reactive, ref} from "vue"
import {CircleClose, CircleCloseFilled, ZoomIn} from "@element-plus/icons-vue"
  import Detail from "../components/DealDetail.vue"
  import router from "@/router";
  import axios from "axios";
  import {ElMessage} from "element-plus";

  const menu = ref("3")
  const identity = localStorage.getItem('identity')
  const username = localStorage.getItem('username')
  const total = ref(0)
  const loading = ref(false)
  const curPage = ref(1)
  const flag = ref(false)
  const curIndex = ref('1')
  const accountNumber = ref(1)
  const fullscreenLoading = ref(false)
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

  const handleSelect2 = (index: string) => {
    curIndex.value = index
    if (index === '1') {
      router.push('/home')
    } else if (index === '2') {
      router.push('/dealCommunity')
    } else if (index === '3') {
      router.push('/myBlock')
    }
  }
    
  const address1 ='asdgre5j7';
  const address2 = 'asedfjh3r';
  const address3 = 'ytrfdcvb3';
  const dealTimes1 = 222;
  const dealTimes2 = 56;
  const dealTimes3 = 3;
  const timeCoin1 = 2311.01;
  const timeCoin2 = 547.50;
  const timeCoin3 = 14.92;

  function change() {
    load()
  }

  function fake() {
    router.push('/blockDetail')
  }

  function commit() {
    fullscreenLoading.value = true
    setTimeout(() => {
      fullscreenLoading.value = false
      ElMessage.success('提交成功')
      flag.value = true
    }, 2000)

  }

  function load() {
    loading.value = true
    axios.post('http://localhost:5000/ShowTX4', {
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

  .pagination {
    margin-top: 2vh;
    margin-left: 1vw;
  }

  .leftcontent {
    height: 91vh;
    width: 65vw;
    border-right: #40b9dc solid 1px;
  }

  .rightcontent {
      width: 35vw;
  }

  .dealbtn {
    margin-top: 4vh;
    margin-left: 2vw;
    width: 7vw;
    height: 4vh;
    background:linear-gradient(to right bottom,rgb(2, 105, 201),#40b9dc);
    border: #40b9dc solid 1px;
    color: #fff;
    border-radius: 0.3vw;
  }

  .chain {
    display: flex;
    height: 20vh;
    align-items: center;
  }

  .block {
    vertical-align: middle;
    background:linear-gradient(to right bottom,rgb(2, 105, 201),#40b9dc);
    height: 4vw;
    width: 4vw;
    border-radius: 0.9vh;
    color: rgba(255, 255, 255, 0);
    margin-left: 2vw;
    font-size: 18px;
  }

  .block:hover {
    transition: color 0.3s 0s ease-in-out;
    color: white;
  }

  .block:active {
    background: #40b9dc;
  }

  .line {
    position: absolute;
    vertical-align: middle;
    background-color: black;
    height: 2px;
    width: 55vw;
    box-shadow: 0 0 10px rgb(165, 207, 148);
    z-index: -1;
  }

  .infoKey {
    display: inline-block;
    width: 8vw;
    margin-bottom: 2vh;
    font-family: '黑体';
    margin-left: 4vw;
    font-size: 18px;
    font-weight: 600;
  }

  .rightbtn {
    margin-top: 5vh;
    margin-left: 15vw;
    width: 5vw;
    height: 3.5vh;
    background:linear-gradient(to right bottom,rgb(2, 105, 201),#40b9dc);
    border: 0;
    border-radius: 0.6vh;
    color: #fff;
  }

  .rightbtn:hover{
    border: white solid 1px;
  }

  .rightbtn:active{
    background:#40b9dc;
  }

  .dealbtn:hover{
    border: white solid 1px;
  }

  .dealbtn:active{
    background:#40b9dc;
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

  .rightbottom {
    width: 31vw;
    height: 30vh;
    border: #40b9dc solid 1px;
    border-radius: 7px;
    margin-left: 2vw;
    margin-top: 2vh;
  }

</style>