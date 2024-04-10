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
              <el-menu-item v-if="identity === '志愿者'" index="2" @click='dealCommunity'>交易社区</el-menu-item>
              <el-menu-item v-if="identity === '志愿者'" index="3">我的区块</el-menu-item>
              <el-menu-item v-if="identity === '管理员'" index="4">任务审核</el-menu-item>
              <el-menu-item v-if="identity === '管理员'" index="5">账号审核</el-menu-item>
            </el-menu>
          <el-popover popper-style="border: #40b9dc solid 1px; border-radius: 8px" offset="5" width="13vw">
            <template #reference>
              <div class="title-icon">
                <el-icon color="#fff" style="margin-left: 13px; margin-top: 11px" size="30px"><UserFilled /></el-icon>
              </div>
            </template>
            <template #default>
              <div class="popover" v-if="identity === '用户'">
                <span class="pText">用户名：{{ username }}</span>
                <br>
                <span class="pText">机构：{{ institution }}</span>
              </div>
              <div class="popover" id="popover" v-if="identity === '志愿者'">
                <div class="Vaccount ac1"><span class="pText">地址：  {{ address1 }}</span> <br><span class="pText">交易次数:{{ dealtimes1 }}</span><br>
                  <span>时间币：</span>{{ timeCoin1 }}
                </div>
                <div class="Vaccount ac2"><span class="pText">地址： {{ address2 }}</span> <br><span class="pText">交易次数:{{ dealtimes2 }}</span><br>
                  <span>时间币：</span>{{ timeCoin2 }}
                </div>
                <div class="Vaccount ac3"><span class="pText">地址： {{ address3 }}</span> <br><span class="pText">交易次数:{{ dealtimes3 }}</span><br>
                  <span>时间币：</span>{{ timeCoin3 }}
                </div>
              </div>
            </template>
          </el-popover>
        </div>
      </el-header>
      <div class="h-separate"></div>
      <el-container>
        <el-aside width="20.05vw">
          <div class="option">
            <el-button class="openTask" @click="openTask = true" v-if="identity === '用户'">发布任务</el-button>
            <el-menu active-text-color="#303133" background-color="#fff" @select="handleSelect2"
                     text-color="#1b1c1f" class="taskMenu" :default-active="taskMenu">
              <el-menu-item index='1' v-if="identity === '用户'">已发布</el-menu-item>
              <el-menu-item index='2' v-if="identity === '用户'">已完成</el-menu-item>
              <el-menu-item index='3' v-if="identity === '管理员'">未审核发布</el-menu-item>
              <el-menu-item index='4' v-if="identity === '管理员'">已审核发布</el-menu-item>
              <el-menu-item index='5' v-if="identity === '管理员'">未审核提交</el-menu-item>
              <el-menu-item index='6' v-if="identity === '管理员'">已审核提交</el-menu-item>
            </el-menu>
          </div>
        </el-aside>
        <el-main>
          <div class="search">
            <div style="display: flex">
              <el-input v-model="search" style="width: 11.46vw"
                      :prefix-icon="Search" placeholder="请输入" clearable/>
              <el-button class="detail" style="margin-left: 10px; margin-right: 0" @click="searching">搜索</el-button>
              <el-button style="margin-left: 10px" @click="change(1)">重置</el-button>
            </div>
          </div>
          <div v-loading="loading" element-loading-text="Loading..." :element-loading-spinner="svg"
                  element-loading-svg-view-box="-10, -10, 50, 50" element-loading-background="rgba(122, 122, 122, 0.8)" style="width: 66.15vw; margin-top: 5px">
            <div style="display: flex">
              <Detail :detail="detailData[0]" :index="taskMenu"/>
              <Detail :detail="detailData[1]" :index="taskMenu"/>
            </div>
            <div style="display: flex">
              <Detail :detail="detailData[2]" :index="taskMenu"/>
              <Detail :detail="detailData[3]" :index="taskMenu"/>
            </div>
          </div>
          <div style="text-align: center; display: flex">
            <span style="margin-top: 2vh; margin-left: 20vw; padding: 7px; font-size: 15px; font-family: '黑体'; color: rgb(120, 120, 120)">共 {{ total }} 条</span>
            <el-pagination class="pagination" :current-page="curPage" :page-size="4" :pager-count="6" layout="prev, pager, next" @current-change="change" :total="total"></el-pagination>
          </div>
          <el-dialog width="30%" v-model="openTask" title="发布任务" :close-on-click-modal="false" :onClose="close">
            <div class="dialog">
              <el-form :model="form" label-width="80px" class="form" label-position="left" ref="formRef" :rules="rules" status-icon>
                <el-row>
                  <el-col :span="20">
                    <el-form-item label="名称" prop="name">
                      <el-input v-model="form.name" placeholder="请输入" clearable/>
                    </el-form-item>
                    <el-form-item label="活动区域" prop="location">
                      <el-input v-model="form.location" placeholder="请输入" clearable/>
                    </el-form-item>
                    <el-form-item label="起止时间" prop="time">
                      <el-date-picker v-model="form.time" type="datetimerange" format="YYYY-MM-DD HH:mm"
                                      start-placeholder="Start Time" end-placeholder="End Time" :default-time="defaultTime"/>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="活动时长" prop="duration">
                  <el-input-number v-model.number="form.duration" :precision="1" :step="0.5" :max="24" type="number" step-strictly /> &nbsp;&nbsp; 小时
                </el-form-item>
                <el-form-item label="活动奖励" prop="award">
                  <el-input-number v-model.number="form.award" :precision="2" :step="0.5" :max="100" type="number" /> &nbsp;&nbsp; 时间币
                </el-form-item>
                <el-row>
                  <el-col :span="16">
                    <el-form-item label="性质" prop="trait">
                      <el-radio-group v-model="form.trait">
                        <el-radio label="文本 1" :value="0"/>
                        <el-radio label="文本 2" :value="1"/>
                        <el-radio label="文本 3" :value="2"/>
                        <el-radio label="文本 4" :value="3"/>
                      </el-radio-group>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="20">
                    <el-form-item label="描述" prop="description">
                      <el-input v-model="form.description" :autosize="{minRows: 4}" type="textarea" placeholder="请输入" clearable/>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            <template #footer>
              <span class="dialog-footer">
                <el-button type="danger" @click="close">取 消</el-button>
                <el-button type="primary" @click="reset">重 置</el-button>
                <el-button v-loading.fullscreen.lock="fullscreenLoading" style="background-color: #40b9dc; color: white"
                          class="out" @click="save">立即发布</el-button>
              </span>
            </template>
          </el-dialog>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts" name="Home">
import {onMounted, reactive, ref, watch} from "vue"
  import {Search} from "@element-plus/icons-vue"
  import Detail from "../components/Detail.vue"
  import axios from "axios";
  import {ElMessage} from "element-plus";
  import router from "@/router";

  const menu = ref('1')
  const identity = localStorage.getItem('identity')
  const username = localStorage.getItem('username')
  const institution = localStorage.getItem('institution') !== "" ? localStorage.getItem('institution') : "无" // 可能 bug
  const taskMenu = ref('1')
  const search = ref("")
  const loading = ref(false)
  const searchFlag = ref(false)
  const total = ref(1)
  const openTask = ref(false)
  const fullscreenLoading = ref(false)
  const formRef = ref()
  const curPage = ref(1)
  const form = reactive({
    name: "",
    location: "",
    time: [],
    trait: [],
    description: "",
    duration: 0,
    award: 0
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
    ],
    award: [
      {required: true, message: "请输入描述", trigger: "blur", type: "number"},
      {min: 0.01, message: "请输入活动奖励", trigger: "blur", type: "number"}
    ],
    duration: [
      {required: true, message: "请输入活动时长", trigger: "blur", type: "number"},
      {min: 0.5, message: "请输入活动时长", trigger: "blur", type: "number"}
    ]
  })
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
  let detailData = reactive([
    {
      activitytime: 0.,
      area: "",
      award: 0.,
      begintime: "",
      checked: "",
      details: "",
      endtime: "",
      id: 0,
      mcharacter: "",
      name: "",
      status: "",
      uploader: "",
      uploader_company: ""
    },
  ])
  const map = ["ABCD", "EFGH", "IJKL", "MNOP"]

  const createDetailData = () => [{
    activitytime: 0.,
    area: "",
    award: 0.,
    begintime: "",
    checked: "",
    details: "",
    endtime: "",
    id: 0,
    mcharacter: "",
    name: "",
    status: "",
    uploader: "",
    uploader_company: ""
  }]

  const handleSelect2 = (index: string) => {
    taskMenu.value = index
    localStorage.setItem('index', index)
    if (index === '1') {
      loadUserPublished()
    } else if (index === '2') {
      loadUserCompleted()
    } else if (index === '3') {
      loadAdminNCP()
    } else if (index === '4') {
      loadAdminCCP()
    } else if (index === '5') {
      loadAdminNCS()
    } else if (index === '6'){
      loadAdminCCS()
    }
  }

  function change(val: number) {
    if (!searchFlag.value) {
      curPage.value = val
      if (taskMenu.value === '1') {
        loadUserPublished()
      } else if (taskMenu.value === '2'){
        loadUserCompleted()
      }
    }
  }

  function reset() {
    formRef.value.resetFields()
  }

  function close() {
    reset()
    openTask.value = false
  }

  function save() {
    formRef.value.validate((valid) => {
      if (valid) {
        let time0 = form.time[0].toLocaleString().replaceAll('/', '-').split('-')
        if (time0[1].length === 1) {
          time0[1] = '0' + time0[1]
        }
        if (time0[2].length === 1) {
          time0[2] = '0' + time0[2]
        }
        let time1 = form.time[1].toLocaleString().replaceAll('/', '-').split('-')
        if (time1[1].length === 1) {
          time1[1] = '0' + time1[1]
        }
        if (time1[2].length === 1) {
          time1[2] = '0' + time1[2]
        }
        form.time[0] = time0.join('-').slice(0, 16) + ":00"
        form.time[1] = time1.join('-').slice(0, 16) + ":00"

        ElMessageBox.confirm(
          '是否确认发布任务？',
          'Warning',
          {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(() => {
          fullscreenLoading.value = true
          axios.post('http://localhost:5000/Publish/Mission', {
            name: form.name,
            area: form.location,
            begintime: form.time[0],
            endtime: form.time[1],
            mcharacter: map[form.trait],
            activitytime: form.duration,
            details: form.description,
            award: form.award,
            id: username
          }).then(res => {
            fullscreenLoading.value = false
            if (res.status === 200) {
              openTask.value = false
              router.push('/home')
              ElMessage({
                type: 'success',
                message: '发布成功，待审核',
              })
            } else {
              ElMessage({
                type: 'error',
                message: '发布失败',
              })
            }
          }).catch(() => {
            ElMessage({
              type: 'error',
              message: '发布失败',
            })
            fullscreenLoading.value = false
          })
        }).catch(() => {
          ElMessage({
            type: 'info',
            message: '取消发布',
          })
        })
      }
    })
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

  function loadUserPublished() {
    loading.value = true
    axios.post('http://localhost:5000/PublishedMission', {
      page: curPage.value,
      id: username
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function loadUserCompleted() {
    curPage.value = 1
    loading.value = true
    axios.post('http://localhost:5000/FinishedMission', {
      page: curPage.value,
      id: username
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function searching() {
    if (search.value === "") {
      ElMessage({
        type: 'warning',
        message: '请输入搜索内容',
      })
    } else {
      searchFlag.value = true
      loading.value = true
      axios.post('http://localhost:5000/select', {
        id: username,
        input: search.value
      }).then(res => {
        detailData = reactive([{
          activitytime: 0.,
          area: "",
          award: 0.,
          begintime: "",
          checked: "",
          details: "",
          endtime: "",
          id: 0,
          mcharacter: "",
          name: "",
          status: "",
          uploader: "",
          uploader_company: ""
        }])
        Object.assign(detailData, res.data)
        total.value = 1
        loading.value = false
      }).catch(res => {
        if (res.response.data.error === 'No results found')
        ElMessage({
          type: 'error',
          message: '没有找到任务（请输入任务全名）',
        })
        loading.value = false
      }).finally(() => {
        searchFlag.value = false
      })
    }
  }

  function loadAdminNCP() {
    loading.value = true
    axios.post('http://localhost:5000/NotCheckedMission', {
      page: curPage.value
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function loadAdminCCP() {
    loading.value = true
    axios.post('http://localhost:5000/CheckedMission', {
      page: curPage.value
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function loadAdminNCS() {
    loading.value = true
    axios.post('http://localhost:5000/Check/SubmittedProof', {
      page: curPage.value
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function loadAdminCCS() {
    loading.value = true
    axios.post('http://localhost:5000/Finished/SubmittedProof', {
      page: curPage.value
    }).then(res => {
      detailData = reactive([{
        activitytime: 0.,
        area: "",
        award: 0.,
        begintime: "",
        checked: "",
        details: "",
        endtime: "",
        id: 0,
        mcharacter: "",
        name: "",
        status: "",
        uploader: "",
        uploader_company: ""
      }])
      Object.assign(detailData, res.data)
      total.value = detailData[detailData.length - 1].num
      loading.value = false
    })
  }

  function handleSelect1() {

  }

  function selectLoad() {
    handleSelect2(taskMenu.value)
  }

  function selectMenu() {
    if (identity === '用户') {
      menu.value = '1'
    } else if (identity === '管理员') {
      menu.value = '4'
    }
  }

  function selectTaskMenu() {
    if (identity === '用户') {
      taskMenu.value = '1'
    } else if (identity === '管理员') {
      taskMenu.value = '3'
    }
  }

  onMounted(() => {
    selectMenu()
    selectTaskMenu()
    const getIndex = localStorage.getItem('index')
    if (getIndex !== null) {
      taskMenu.value = getIndex
    } else {
      if (identity === '用户') {
        localStorage.setItem('index', '1')
      } else if (identity === '管理员') {
        localStorage.setItem('index', '3')
      }
    }
    selectLoad()
  })

  function dealCommunity(){
    window.location.href='vPersonal';
  }

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

  .option {
    margin-top: 4.91vh;
    margin-left: 7.42vw;
  }

  .openTask {
    width: 8.29vw;
    height: 3.98vh;
    margin-left: 0.8vw;
    background: linear-gradient(to right bottom, rgb(2, 132, 208), rgb(64, 185, 220));
    color: white;
    border-radius: 7px;
  }

  .openTask:hover {
    background: linear-gradient(to right bottom, rgba(2, 132, 208, 0.5), rgba(64, 185, 220, 0.5));
  }

  .openTask:active {
    background: linear-gradient(to right bottom, rgba(2, 132, 208, 0.3), rgba(64, 185, 220, 0.3));
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
    margin-left: 44.3vw;
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
    line-height: 4vh;
    font-family: "黑体";
    font-size: 16px;
  }

  /* add for new */
  .Vaccount{
    text-align: center;
    width: 12vw;
    border: #40b9dc solid 1px;
    border-radius: 1vh;
  }

  .ac1 {
    background: linear-gradient(to right, rgb(0, 132, 208), rgb(88, 142, 212) 40%, rgb(64, 185, 220));
    color: #fff;
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