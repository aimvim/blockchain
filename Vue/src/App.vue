<template>
  <div>
    <Count />
    <br>
    <LoveTalk />
  </div>
</template>

<script lang="ts" setup name="App">
  // JS / TS
  import Count from './components/Count.vue'
  import LoveTalk from './components/LoveTalk.vue'

  // 存数据 - store 文件夹，.ts 文件中的 state
  // 读数据 - use...Store
  // 修改数据 - 三种方法：直接修改、多数据修改、通过 action 修改
  // 解构赋值 - storeToRefs
  // 计算属性 - getters
  // 监视 - $subscribe
  // 组合式写法

</script>

<style scoped>


</style>