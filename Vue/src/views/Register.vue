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
              <el-input style="width: 250px" v-model="form.invitationCode" :placeholder="codePlaceholder" />
            </el-form-item>
          </div>
          <div style="display: flex" v-if="form.identity === '管理员' || form.identity === '用户'">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="20px"><Message /></el-icon>
            <el-form-item prop="registrationCode">
              <el-input style="width: 250px" v-model="form.registrationCode" placeholder="注册码" />
            </el-form-item>
          </div>
          <div style="display: flex" v-if="form.identity === '用户'">
            <el-icon style="margin-right: 10px; margin-top: 5px" color="#fff" size="19px"><DocumentChecked /></el-icon>
            <el-upload class="upload" action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                       :auto-upload="false" drag multiple :before-upload="beforeUpload">
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将图片拖拽至这里或 <em>手动上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  上传格式：jpg/png
                </div>
              </template>
            </el-upload>
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
  import {type UploadProps} from "element-plus";
  import axios from "axios";
  import router from "@/router";

  const form = reactive({
    identity: "用户",
    username: "",
    password: "",
    confirmPassword: "",
    invitationCode: "",
    registrationCode: ""
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
    ],
    registrationCode: [
      {required: true, message: "请输入注册码", trigger: "blur"}
    ]
  })

  function changeGroup() {
    codePlaceholder.value = form.identity === '管理员' ? "邀请码（必填）" : "邀请码（选填）"
  }

  window.addEventListener('load', () => {
    const div = document.querySelector('.upper');
    const div2 = document.querySelector('.login-box');
    div.classList.add('loaded');
    div2.classList.add('loaded');
  });

  const beforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
    const allowedFormats = ['image/jpeg', 'image/png'];
    if (!allowedFormats.includes(rawFile.type)) {
      ElMessage.error('Avatar picture must be in JPG or PNG format!');
      return false;
    }

    return true;
  }

  function register() {
    formRef.value.validate((value) => {
      if (value) {
        if (form.identity === '用户') {
          axios.post('http://localhost:5000/user_register',
              {
                id: form.username,
                passwd: form.password,
                register_code: form.registrationCode,
                proof: "sdandsehnqoinqoi"
              }).then(res => {
            if (res.status === 200) {
              ElMessage.success('注册成功')
              localStorage.setItem('identity', form.identity)
              localStorage.setItem('username', form.username)
              router.push('/login')
            } else {
              ElMessage.error('注册失败')
            }
          }).catch(res => {
            if (res.response.data === 'Wrong Register Code!') {
              ElMessage.error('注册码错误')
            } else {
              ElMessage.error('注册失败')
            }
          })
        } else if (form.identity === '志愿者') {
          axios.post('http://localhost:5000/volunteer_register',
            {
              id: form.username,
              password: form.password,
              invitationCode: form.invitationCode
            }).then(res => {
            if (res.status === 200) {
              ElMessage.success('注册成功')
              localStorage.setItem('identity', form.identity)
              localStorage.setItem('username', form.username)
              ElNotification({
      title: '请保管好您的私钥',
      dangerouslyUseHTMLString: true,
      message: `在复制完毕前请勿关闭此通知。
<pre style="margin-left: 0; white-space: pre-wrap; float: left; width: 25vw; word-break: break-all;">
{
    "adress": "16xrj8WgLRNsJDfqA6i8BQPqtXJtbyeZoT",
    "pk": "4483e4e2e1077cb5bbf10be329e1f788b1c5e86a2c2895263da6e3a9ba51c7332b9c3c8795c6ea4223a6f89fea85fb5a6dcc7e9fbb3a2f480a771b1a77f027c0",
    "sk": "36e729872b09df5df6759f332c606066185946c5bd6ffbcb35ad35dd2b51d8eb"
}
</pre>

      `,
      type: 'warning',
      duration: 0,
      customClass: 'note'
    })
              router.push('/login')
            } else {
              ElMessage.error('注册失败')
            }
          })
        } else {
          axios.post('http://localhost:5000/admin_register',
              {
                id: form.username,
                passwd: form.password,
                register_code: form.registrationCode,
                invite_code: form.invitationCode
              }).then(res => {
            if (res.status === 200) {
              ElMessage.success('注册成功')
              localStorage.setItem('identity', form.identity)
              localStorage.setItem('username', form.username)
              router.push('/login')
            } else {
              ElMessage.error('注册失败')
            }
          }).catch(res => {
            if (res.response.data === 'Wrong Register Code!') {
              ElMessage.error('注册码错误')
            } else {
              ElMessage.error('注册失败')
            }
          })
        }
      }
    })
  }

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
    top: 12vh;
    color: rgba(255, 255, 255, 1);
  }

  .login-box {
    border-radius: 15px;
    margin: 16.63vh 36.72vw 40.65vh;
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
    width: 8.8vw;
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

  .upload {
    width: 13.1vw;
  }

  /deep/ .upload .el-upload-list {
    margin-top: 30px;
  }

  /deep/ .upload .el-upload-list__item {
    background-color: rgba(255, 255, 255, 0.4);
  }

  /deep/ .upload .el-upload-list__item:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  /deep/ .el-upload-list__item-name .el-icon {
    color: white;
  }

  /deep/ .upload .el-upload-list__item-name {
    color: white;
  }

  /deep/ .el-upload .el-upload-dragger {
    width: 13.1vw;
    height: 11vh;
    margin: 0;
    padding: 0;
    background-color: rgba(255, 255, 255, 0.4);
  }

  .el-icon--upload {
    margin: 0;
    color: rgba(255, 255, 255, 0.8);
  }

  .el-upload__text {
    margin: 0;
    padding: 0;
    color: white;
    font-size: 12px;
  }

  .el-upload__tip {
    color: white;
    float: left;
  }
</style>

<style>
  .note {
    width: 30vw;
  }
</style>
