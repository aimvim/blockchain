<template>
  <div class="back">
    <div class="upper">Register</div>
    <div class="login-box">
      <el-radio-group v-model="form.identity" @change="changeGroup" fill="rgba(255, 255, 255, 0.1)">
        <el-radio-button label="用户" value="用户" />
        <div class="v-separate"></div>
        <el-radio-button label="志愿者" value="志愿者" />
        <div class="v-separate"></div>
        <el-radio-button label="管理员" value="管理员" />
      </el-radio-group>
      <div class="h-separate"></div>
      <div class="login-form">
        <el-form ref="formRef" :model="form" status-icon :rules="rules">
          <div style="display: flex">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="20px"><User /></el-icon>
            <el-form-item prop="username">
              <el-input style="width: 250px" v-model="form.username" placeholder="用户名" />
            </el-form-item>
          </div>
          <div style="display: flex">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="20px"><Lock /></el-icon>
            <el-form-item prop="password">
              <el-input style="width: 250px" v-model="form.password" placeholder="密码" show-password />
            </el-form-item>
          </div>
          <div style="display: flex">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="20px"><Key /></el-icon>
            <el-form-item prop="confirmPassword">
              <el-input style="width: 250px" v-model="form.confirmPassword" placeholder="确认密码" show-password />
            </el-form-item>
          </div>
          <div style="display: flex">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="20px"><Link /></el-icon>
            <el-form-item prop="invitationCode">
              <el-input style="width: 250px" v-model="form.invitationCode" :placeholder="codePlaceholder" show-password />
            </el-form-item>
          </div>
          <el-link style="margin-top: 20px" href="/login">返回</el-link>
          <br>
          <el-button class="login-button" type="primary" @click="register">注册</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="Login">
import {reactive, ref, toRef} from "vue"

  const form = reactive({
    identity: "用户",
    username: "",
    password: "",
    confirmPassword: "",
    invitationCode: ""
  })
  const codePlaceholder = ref(form.identity === '管理员' ? "邀请码（必填）" : "邀请码（选填）")
  const formRef = ref()

  const passwordValidator = (rule, value, callback) => {
    if (form.password !== form.confirmPassword) {
      callback(new Error("两次输入密码不一致"))
    } else {
      callback()
    }
  }

  const codeValidator = (rule, value, callback) => {
    if (form.identity === '管理员' && !value) {
      callback(new Error("请输入邀请码"))
    } else if (value.length !== 0 && value.length !== 6) {
      callback(new Error("邀请码长度必须为 6 位"))
    } else {
      callback()
    }
  }

  const rules = reactive({
    username: [
      {required: true, message: "请输入用户名", trigger: "blur"},
      {max: 8, message: "用户名长度不能超过 8 个字符", trigger: ['blur', 'change']}
    ],
    password: [
      {required: true, message: "请输入密码", trigger: "blur"},
      {min: 6, message: "密码长度不能小于 6 个字符", trigger: ['blur', 'change']}
    ],
    confirmPassword: [
      {required: true, message: "请再次输入密码", trigger: "blur"},
      {validator: passwordValidator, trigger: ["blur", 'change']}
    ],
    invitationCode: [
      {validator: codeValidator, trigger: "blur"}
    ]
  })

  function changeGroup() {
    codePlaceholder.value = form.identity === '管理员' ? "邀请码（必填）" : "邀请码（选填）"
  }

  window.addEventListener('load', () => {
    const div = document.querySelector('.upper');
    const div2 = document.querySelector('.login-box');
    const div3 = document.querySelector('.optional');
    div.classList.add('loaded');
    div2.classList.add('loaded');
    div3.classList.add('loaded');
  });

</script>

<!--suppress CssInvalidPseudoSelector -->
<style scoped>
  .back {
    height: 100%;
    width: 100%;
    position: fixed;
    overflow: hidden;
    background-image: url("@/assets/imgs/bg.png");
    background-size: 100% 100%;
  }

  .upper {
    font-size: 40px;
    position: relative;
    text-align: center;
    top: -100px;
    color: white;
    color: rgba(255, 255, 255, 0);
    font-family: "Microsoft YaHei UI Light";
    transition: top 1.5s 0s ease-in-out, color 1s 0s ease-in-out;
  }

  .upper.loaded {
    top: 20vh;
    color: rgba(255, 255, 255, 1);
  }

  .login-box {
    border-radius: 15px;
    margin: 24.63vh 36.72vw 40.65vh;
    box-shadow: 0 10px 20px 5px rgba(0, 0, 0, 0.2);
    opacity: 0;
    transition: opacity 1.5s 0s ease-in-out;
  }

  .login-box.loaded {
    opacity: 1;
  }

  ::v-deep .el-radio-button .el-radio-button__inner {
    border: 0;
    background: rgba(255, 255, 255, 0.4);
    line-height: 6.944vh;
    width: 8.819vw;
    height: 6.944vh;
    font-size: 18px;
    color: white;
    padding: 0;
  }

  ::v-deep .el-radio-button__original-radio:checked + .el-radio-button__inner {
    margin: 0;
    padding: 0;
    background: transparent;
  }

  :deep(.el-radio-button:first-child .el-radio-button__inner) {
    border-top-left-radius: 15px;
  }

  :deep(.el-radio-button:last-child .el-radio-button__inner) {
    border-top-right-radius: 15px;
  }

  .login-form {
    padding: 6.944vh 6.03vw 4vh;
    text-align: center;
  }


  .v-separate:before {
    content: "";
    display: inline-block;
    width: 1px;
    height: 6.944vh;
    background-color: white;
  }

  .h-separate {
    content: "";
    width: 100%;
    height: 1px;
    background-color: white;
  }

  a {
    color: white;
    font-size: 12px;
  }

  .login-button {
    margin-top: 1vh;
    width: 7.45vw;
    background-color: rgba(255, 255, 255, 0.4);
    border-color: white;
    border-radius: 50px;
  }

  .el-input {
    --el-input-text-color: white;
    --el-input-icon-color: white;
    --el-input-placeholder-color: white;
  }

  .el-input /deep/ .el-input__wrapper {
    border-radius: 6px;
    background-color: rgba(255, 255, 255, 0.4);
  }

  .el-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  .el-button:active {
    background-color: rgba(255, 255, 255, 0);
  }

</style>
