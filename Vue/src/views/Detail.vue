<template>
  <div>
    <div class="task">
      <div class="title">
        <span style="font-size: 18px; font-family: '黑体'; margin-top: 10px; width: 15vw">任务名称任务名称</span>
        <span class="time-loc">2024-04-12 <br> 四川省成都市成华区</span>
      </div>
      <div class="h-separate"></div>
      <div class="text"> <!-- 时间地点描述要传过来 -->
        <span>活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述活动描述。</span>
      </div>
      <div style="display: flex; flex-wrap: nowrap; margin-top: 6.5vh; align-items: center; justify-content: space-between">
        <div class="condition" style="color: rgb(120, 120, 120); border: rgb(120, 120, 120) solid 1px;" v-if="index === '1'">待接取</div>
        <div class="condition" v-if="index === '2'">进行中</div>
        <div class="condition" style="color: rgb(230, 136, 100); border: rgb(230, 136, 100) solid 1px;" v-if="index === '3' && pass === false">未通过</div>
        <div class="condition" style="color: rgb(102, 183, 153); border: rgb(102, 183, 153) solid 1px;" v-if="index === '3' && pass === true">已通过</div>
        <el-button class="detail" @click="dialog = true">查看详情</el-button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts" name="Detail">
  import {defineProps, reactive, ref} from "vue"

  const pass = ref(true)
  const dialog = ref(false)

  const { index } = defineProps(['index'])
</script>

<style scoped>
  .task {
    border: #40b9dc solid 1px;
    margin: 1.83vh 2.2vw 2.6vh;
    width: 27.86vw;
    height: 25.74vh;
    border-radius: 7px;
    padding: 10px;
  }
  .title {
    margin-top: 10px;
    margin-left: 10px;
    display: flex;
  }

  .time-loc {
    font-size: 12px;
    color: rgb(120, 120, 120);
    margin-left: 6vw;
    line-height: 20px;
    text-align: right;
  }

  .h-separate {
    border-top: 1px solid #40b9dc;
    margin: 10px 10px;
  }

  .text {
    margin: 15px 10px;
    font-size: 14px;
    line-height: 20px;
    color: rgb(100, 100, 100);
  }

  .detail {
    margin-right: 10px;
    width: 5.625vw;
    background-color: #40b9dc;
    color: white;
  }

  .condition {
    flex-basis: 80px;
    margin-left: 8px;
    font-size: 14px;
    text-align: center;
    height: 22px;
    line-height: 22px;
    color: rgb(64, 185, 220);
    border-radius: 25px;
    border: rgb(64, 185, 220) solid 1px;
  }

  .detail:hover {
    background-color: rgba(64, 185, 220, 0.5);
  }

  .detail:active {
    background-color: rgba(64, 185, 220, 0.3);
  }

</style>