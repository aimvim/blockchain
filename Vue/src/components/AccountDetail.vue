<template>
  <div v-if="detail !== undefined && detail.id !== undefined">
    <div style="display: flex; margin-top: 1vh;">
      <div class="accountContent">
        <div class="text" style="margin-top: 2vh">用户名：{{ detail.id }}</div>
        <div class="text">机构：{{ detail.institution }}</div>
        <div>
          <img v-if="detail.proof !== '' && detail.proof !== 'picture'" class="photoStyle" :src="detail.proof" alt="">
          <img v-else class="photoStyle" src="../assets/imgs/pictureNotLoaded.png" alt="">
        </div>
        <div v-if="index === '1'" class="button">
          <el-button class="passBtn">通过</el-button>
          <el-button class="RefuseBtn">不通过</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="AccountDetail">
  import { defineProps } from 'vue';
  const { detail, index } = defineProps(['detail', 'index']);
</script>

<style scoped>
  .accountContent {
    border: #40b9dc solid 2px;
    margin-top: 1vw;
    margin-left: 2vw;
    border-radius: 0.8vw;
    width: 20vw;
    height: 30vh;
  }

  .text {
    margin-left: 2vw;
    text-align: left;
    width: 15vw;
    height: 4vh;
    color: #40b9dc;
  }

  .photoStyle {
    margin-left: 2vw;
    margin-top: 0;
    width: 16vw;
    height: 14vh;
  }

  .button {
    display: flex;
    margin-top: 0.5vw;
    margin-left: 6.5vw;
  }

  .passBtn {
    width: 3vw;
    height: 3vh;
    background-color: #40b9dc;
    color: white;
    font-size: 13px;
  }

  .passBtn:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .passBtn:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

  .RefuseBtn {
    width: 3vw;
    height: 3vh;
    background-color: #f89898;
    color: white;
    margin-left: 1vw;
    font-size: 12px;
  }

  .RefuseBtn:hover {
    background-color: rgba(248, 152, 152, 0.5);
  }

  .RefuseBtn:active {
    background-color: rgba(248, 152, 152, 0.3);
  }

</style>