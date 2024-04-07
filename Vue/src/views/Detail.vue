<!--
 * @Descripttion: 
 * @version: 
 * @Author: tac
 * @Date: 2024-03-28 16:59:20
 * @LastEditTime: 2024-03-29 18:37:03
-->
<template>
  
    <div class="task" v-if="detail !== undefined && detail.activitytime !== undefined">
      <div class="title">
        <span style="font-size: 1.5vw; font-family: '黑体'; margin-top: 10px; width: 15vw">{{ detail.name }}</span>
        <span class="time-loc">{{ time }} <br> {{ detail.area }}</span>
      </div>
      <div class="h-separate"></div>
      <div class="text" id="text"> <!-- 时间地点描述要传过来 -->
        <span style="height: auto;">{{ detail.details }}</span>
      </div>  

        <div style="display: flex; flex-wrap: nowrap; margin-bottom: 2.6vh; align-items: center; justify-content: space-between">
          <div class="condition" style="color: rgb(120, 120, 120); border: rgb(120, 120, 120) solid 1px;" v-if="detail.checked === 'not'">待审核</div>
          <div class="condition" style="color: rgb(230, 136, 100); border: rgb(230, 136, 100) solid 1px;" v-if="detail.checked === 'yes' && detail.status === 'not finished'">未完成</div>
          <div class="condition" style="color: rgb(102, 183, 153); border: rgb(102, 183, 153) solid 1px;" v-if="detail.checked === 'yes' && detail.status === 'finished'">已完成</div>
          <el-button class="detail" @click="dialog = true">查看详情</el-button>
        </div>
      
    </div>
  
  
</template>

<script setup lang="ts" name="Detail">
  import { DCaret } from "@element-plus/icons-vue";
  import {defineProps, reactive, ref, toRefs, watch} from "vue"

  const time = ref("")
  const dialog = ref(false)

  const tmp = defineProps(['detail']);
  const { detail } = toRefs(tmp)

  watch(() => detail?.value, (newVal, oldVal) => {
    if (detail?.value !== undefined && detail.value.begintime !== undefined) {
      let tmp = detail.value.begintime.split(' ')
      tmp[0] = tmp[0].slice(0, 3)
      const tmp0 = tmp[1]
      tmp[1] = tmp[2]
      tmp[2] = tmp0
      tmp[tmp.length - 1] += '+0800'
      time.value = new Date(tmp.join(' ')).toLocaleString().replaceAll('/', '-').slice(0, 10)
      tmp = time.value.split('-')
      if (tmp[1].length === 1) {
        tmp[1] = '0' + tmp[1]
      }
      if (tmp[2].length === 1) {
        tmp[2] = '0' + tmp[2]
      }
      time.value = tmp.join('-')
    }
  })




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
    margin-top: 8px;
    margin-left: 10px;
    display: flex;
  }

  .time-loc {
    font-size: clamp(1vw, 1.2vw, 12px);
    color: rgb(120, 120, 120);
    margin-left: 3vw;
    line-height: 2vw;
    white-space: nowrap;
    text-align: right;
    width: 8.4vw;
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
    /* 下面设置超出行数显示省略号 */
    overflow: hidden;
    -webkit-line-clamp:4;
    -webkit-box-orient: vertical;
    display: -webkit-box;
    text-overflow: ellipsis;

  }

  .detail {
    margin-right: 10px;
    width: 5.625vw;
    background-color: #40b9dc;
    color: white;
  }

  .condition {
    margin-top: 0;
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