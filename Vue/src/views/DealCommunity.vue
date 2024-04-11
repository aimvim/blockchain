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
                <el-menu-item index="1">任务中心</el-menu-item>
                <el-menu-item v-if="identity === '志愿者'" index="2">交易社区</el-menu-item>
                <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
              </el-menu>
            <el-popover popper-style="border: #40b9dc solid 1px; border-radius: 8px" offset="5" width="13vw">
              <template #reference>
                <div class="title-icon">
                  <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
                </div>
              </template>
  
  
              
              <template #default>
                <div class="popover" id="popover">
                  <div class="Vaccount ac1">
                    <span class="pText">地址：{{ address1 }}</span><br>
                    <span class="pText">交易次数:{{ dealtimes1 }}</span><br>
                    <span>时间币：</span>{{ timeCoin1 }}
                  </div>
                  <div class="Vaccount ac2">
                    <span class="pText">地址：{{ address2 }}</span><br>
                    <span class="pText">交易次数:{{ dealtimes2 }}</span><br>
                    <span>时间币：</span>{{ timeCoin2 }}
                  </div>
                  <div class="Vaccount ac3"><span class="pText">地址：{{ address3 }}</span><br>
                    <span class="pText">交易次数:{{ dealtimes3 }}</span><br>
                    <span>时间币：</span>{{ timeCoin3 }}
                  </div>
                </div>
              </template>



              
            </el-popover>
          </div>
        </el-header>
        <div class="h-separate"></div>
        
      </el-container>
    </div>
    <button class="backbtn" @click="goback()" >发布交易</button>
    <div style="margin-left: 12vw;">
      <div style="display: flex;">
        <div class="dealInfo">&nbsp;Recieipient:{{  }} <br>
          &nbsp;SenderAddress:{{  }} <br>
          &nbsp;Fees:{{  }} 
        </div>
        <div class="inforight">+</div>
        
        <div class="dealInfo">&nbsp;Recieipient:{{  }} <br>
          &nbsp;SenderAddress:{{  }} <br>
          &nbsp;Fees:{{  }} 
        </div>
        <div class="inforight">+</div>
    </div>
    <div style="display: flex;">
        <div class="dealInfo">&nbsp;Recieipient:{{  }} <br>
          &nbsp;SenderAddress:{{  }} <br>
          &nbsp;Fees:{{  }} 
        </div><div class="inforight">+</div>
        <div class="dealInfo">Recieipient:{{  }} <br>
            SenderAddress:{{  }} <br>
            Fees:{{  }} 
        </div><div class="inforight">+</div>
    </div>
    <div style="display: flex;">
        <div class="dealInfo">&nbsp;Recieipient:{{  }} <br>
          &nbsp;SenderAddress:{{  }} <br>
          &nbsp;Fees:{{  }} 
        </div><div class="inforight">+</div>
        <div class="dealInfo">Recieipient:{{  }} <br>
            SenderAddress:{{  }} <br>
            Fees:{{  }} 
        </div><div class="inforight">+</div>
    </div>
    </div>
  </template>
  
<script setup lang="ts" name="DealCommunity">
    import {reactive, ref} from "vue"
    import {Search} from "@element-plus/icons-vue"
    import Detail from "../components/Detail.vue"
  
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
    const rules = reactive({
      name: [
        {required: true, message: "请输入名称", trigger: "blur"}
      ],
      location: [
        {required: true, message: "请输入活动区域", trigger: "blur"}
      ],
      time: [
        {required: true, message: "请选择活动时间", trigger: "blur"}
      ],
      trait: [
        {required: true, message: "请选择性质", trigger: "blur"}
      ],
      description: [
        {required: true, message: "请输入描述", trigger: "blur"}
      ]
    })
  
    const handleSelect2 = (index: string) => {
      curIndex.value = index
    }
  
    function reset() {
      formRef.value.resetFields()
    }
  
    function close() {
      reset()
      openTask.value = false
    }
  
    
    
    //add for new 
    var address1 ='asdadasdas';
    var address2 = 'adsasdaqwe';
    var address3 = 'awdasdwgggg';
    var dealtimes1 = 222;
    var dealtimes2 = 333;
    var dealtimes3 = 123;
    var timeCoin1 = 2.3;
    var timeCoin2 = 23.3;
    var timeCoin3 = 0;
  
    var accountNumber = 3;
    var popover = document.getElementById("popover");
  

    var recieipient = 'a2sdad23';
    var senderaddress = '23ertfgh87eudst56d';
    
    function goback() {
  window.history.go(-1);
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
    /* add for new */
    .Vaccount{
      text-align: center;
      width: 12vw;
      border: #40b9dc solid 1px;
      border-radius: 1vh;
    }
    .ac1{
      background: linear-gradient(to right, rgb(0, 132, 208), rgb(88, 142, 212) 40%, rgb(64, 185, 220));
      color: #fff;
    }
    .dealInfo{
      color: #40b9dc;
      margin-top: 5vh ;
      margin-left: 6vw;
      width: 27vw;
      height: 18vh;
      line-height: 5vh;
      border: #40b9dc solid 1px;
      border-radius: 1.2vw 0 0 1.2vw;

    }
    .backbtn{
  
    border:0 ;
    border-radius: 8%;
    font-size: 1vw;
    color: white;
    margin-top: 6vh;
    background:  linear-gradient(to right, rgb(0, 132, 208), rgb(88, 142, 212) 40%, rgb(64, 185, 220));;
    margin-left: 10vw;
    width: 8vw;
    height: 4vh;

  }
  .inforight{
    
    background-color: #40b9dc;
    margin-top: 5vh ;
    margin-left: 0;
    width: 3vw;
    height: 18vh;
    border: #40b9dc solid 1px;
    border-radius: 0 1.2vw 1.2vw 0;
    line-height: 18vh;
    vertical-align: middle;
    text-align: center;
    font-size:x-large;
    font-weight: 200;
    color: white;
  }
  
  </style>