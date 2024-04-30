<template>
  <div style="display: flex" v-if="detail !== undefined && detail.amount !== undefined">
    <div class="dealBox">
      <div style="display: flex;">
        <div class="info">
          <span>Recipient : &nbsp;</span> <br>
          <span>SenderAddress : &nbsp;</span>  <br>
          <span>Fees : &nbsp;</span>
        </div>
        <div style="display: block">
          <span class="detail">{{ detail.recipient }}</span> <br>
          <span class="detail">{{ detail.senderadress }}</span> <br>
          <span class="detail">{{ detail.fees }}</span>
        </div>
      </div>
    </div>

    <el-button v-if="index === 1" class="plusButton" :icon="Plus" @click="openDetail"></el-button>
    <el-button v-else class="plusButton" @click="openDetail">详情</el-button>
    <el-dialog width="35%" v-model="dealDetail" :close-on-click-modal="false">
      <div style="text-align: center; font-size: 32px; font-family: Consolas">DETAILS</div>
      <div class="dialog">
        <div class="detailTitle">
          <span>SenderAddress :</span> <br>
          <span>Signature :</span> <br>
          <span>Amount :</span> <br>
          <span>Fees :</span> <br>
          <span>Recipient :</span> <br>
        </div>
        <div class="detailValue">
          <span>&nbsp;&nbsp;{{ detail.senderadress }}</span> <br>
          <span>&nbsp;&nbsp;{{ detail.signature }}</span> <br>
          <span>&nbsp;&nbsp;{{ detail.amount }}</span> <br>
          <span>&nbsp;&nbsp;{{ detail.fees }}</span> <br>
          <span>&nbsp;&nbsp;{{ detail.recipient }}</span> <br>
        </div>
      </div>
      <div style="text-align: center" v-if="index === 1">
        <el-button class="plus" :icon="Plus" @click="add"></el-button>
      </div>
      <div style="margin-top: 5vh"></div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="DealDetail">
  import {Plus} from "@element-plus/icons-vue";
  import {defineProps, ref, reactive} from "vue";
  import axios from "axios";

  const dealDetail = ref(false);
  const formRef = ref()

  let { detail, index } = defineProps(['detail', 'index']);

  function openDetail() {
    dealDetail.value = true;
  }

  function add() {
    formRef.value.validate((valid) => {
      if (valid) {
        axios.post('http://localhost:5000/AddToMyBlock', {
          Senderadress: detail.senderadress,
          Recipient: detail.recipient,
          Amount: detail.amount,
          Fees: detail.fees,
          Signature: detail.signature,
          miner: localStorage.getItem('username')
        }).then(res => {
          if (res.data === 'success') {
            dealDetail.value = false;
            form.password = '';
            formRef.value.clearValidate()
            alert('添加成功')
          } else {
            alert('添加失败')
          }
        })
      }
    })
  }

</script>

<style scoped>
  .dealBox {
    font-size: 14px;
    margin-top: 4vh;
    margin-left: 2vw;
    padding-top: 1vh;
    width: 27vw;
    height: 13vh;
    line-height: 4vh;
    border: #40b9dc solid 1px;
    border-right: 0;
    border-radius: 10px 0 0 10px;
  }

  .info {
    color: #40b9dc;
    margin-left: 1vw;
    width: 7vw;
    text-align: right;
  }

  .plusButton {
    margin-top: 4vh;
    width: 2.2vw;
    border-radius: 0 10px 10px 0;
    height: 14.172vh;
    background-color: #40b9dc;
    color: white;
    border: #40b9dc solid 1px;
    border-left: 0;
  }

  .plusButton:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .plusButton:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

  .detail {
    width: 10vw;
    float: left;
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