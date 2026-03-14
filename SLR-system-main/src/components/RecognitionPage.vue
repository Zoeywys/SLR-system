<template>
  <div class="scroll-hide-container">
    <section id="about" style="height: auto; min-height: 100vh; padding: 50px 20px;">
      <div class="section-wrap" style="height: auto; min-height: 100%; width: 100%; max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
        
        <h3 class="section-title"><span>开始</span>识别</h3>

        <p class="p1">
          欢迎使用实时手语识别界面！请确保摄像头已开启且光线条件良好，
          支持拖拽视频、本地上传或摄像头录制。
        </p>

        <!-- 功能按钮 -->
        <div class="function-btn-group">

          <button
            class="section-btn function-btn"
            :class="{ active: mode === 'upload' }"
            @click="switchMode('upload')"
          >
            上传视频
          </button>

          <button
            class="section-btn function-btn"
            :class="{ active: mode === 'camera' }"
            @click="switchMode('camera')"
          >
            摄像头录制
          </button>

        </div>

        <!-- 核心区域 -->
        <div class="recognition-content">

          <!-- 上传区域 -->
          <div v-if="mode === 'upload'" class="upload-section">

            <el-upload
              drag
              action=""
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFile"
              class="upload-area"
            >

              <i class="el-icon-upload upload-icon"></i>

              <div class="upload-text">
                拖拽视频到这里
                <br>
                <span class="upload-click">或点击选择本地视频</span>
                <br>
                <span class="upload-format">(支持 MP4 / WEBM)</span>
              </div>

            </el-upload>

            <!-- 视频预览 -->
            <div class="video-preview" v-if="videoUrl">
              <video :src="videoUrl" controls></video>
            </div>

            <button
              class="section-btn"
              @click="uploadVideo"
              :disabled="!videoFile"
            >
              上传识别
            </button>

          </div>


          <!-- 摄像头区域 -->
          <div v-if="mode === 'camera'" class="camera-section">

            <video
              ref="cameraVideo"
              autoplay
              class="camera-video"
            ></video>

            <div class="camera-btn-group">

              <button class="section-btn" @click="startCamera">
                打开摄像头
              </button>

              <button class="section-btn" @click="startRecording">
                开始录制
              </button>

              <button class="section-btn" @click="stopRecording">
                停止录制
              </button>

              <button class="section-btn" @click="stopCamera">
                关闭摄像头
              </button>

            </div>

            <div v-if="recording" class="recording-time">
              录制时间：{{recordTime}} 秒
            </div>

            <div class="video-preview" v-if="videoUrl">
              <video :src="videoUrl" controls></video>
            </div>

            <button
              class="section-btn"
              @click="uploadVideo"
              :disabled="!videoFile"
            >
              上传识别
            </button>

          </div>

          <!-- 识别结果 -->
          <div v-if="resultText" class="result-box">
            <h3>识别结果</h3>
            <p class="result-text">{{resultText}}</p>
          </div>

        </div>

      </div>
    </section>
  </div>
</template>


<script setup>

import { ref } from "vue"
import axios from "axios"

const mode = ref("upload")

const videoFile = ref(null)

const videoUrl = ref("")

const resultText = ref("")

const cameraVideo = ref(null)

let cameraStream = null

let mediaRecorder = null

let chunks = []

const recording = ref(false)

const recordTime = ref(0)

let timer = null


function switchMode(newMode){

  stopCamera()

  videoFile.value = null

  videoUrl.value = ""

  resultText.value = ""

  mode.value = newMode

}


function handleFile(file){

  videoFile.value = file.raw

  videoUrl.value = URL.createObjectURL(videoFile.value)

}


async function uploadVideo(){

  if(!videoFile.value) return

  const formData = new FormData()

  formData.append("file", videoFile.value)

  try{

    const res = await axios.post(
      "http://localhost:5000/predict",
      formData
    )

    resultText.value = res.data.result

  }catch(e){

    resultText.value = "识别失败，请检查后端服务"

  }

}


async function startCamera(){

  try{

    cameraStream = await navigator.mediaDevices.getUserMedia({ video: true })

    cameraVideo.value.srcObject = cameraStream

    mediaRecorder = new MediaRecorder(cameraStream)

    mediaRecorder.ondataavailable = e => chunks.push(e.data)

    mediaRecorder.onstop = ()=>{

      const blob = new Blob(chunks,{type:"video/webm"})

      chunks = []

      videoFile.value = blob

      videoUrl.value = URL.createObjectURL(blob)

    }

  }catch(e){

    console.log(e)

  }

}


function startRecording(){

  if(!mediaRecorder) return

  recording.value = true

  recordTime.value = 0

  timer = setInterval(()=>{

    recordTime.value++

  },1000)

  mediaRecorder.start()

}


function stopRecording(){

  if(mediaRecorder && mediaRecorder.state==="recording"){

    mediaRecorder.stop()

  }

  recording.value = false

  clearInterval(timer)

}


function stopCamera(){

  if(cameraStream){

    cameraStream.getTracks().forEach(track=>track.stop())

    cameraStream = null

  }

  recording.value = false

  clearInterval(timer)

}

</script>



<style scoped>

/* 标题 */

.section-title{
color:#f5e6c8;
text-align:center;
margin-bottom:20px;
}

.p1{
text-align:center;
color:#eee;
margin-bottom:30px;
}


/* 按钮样式 */

.section-btn{
padding:12px 30px;
border-radius:25px;
border:none;
background:#e8ecd8;
color:#333;
font-weight:600;
cursor:pointer;
}


/* 功能按钮居中 */

.function-btn-group{
display:flex;
justify-content:center;
gap:20px;
margin-bottom:40px;
}


/* 摄像头按钮居中 */

.camera-btn-group{
display:flex;
justify-content:center;
gap:20px;
margin-top:20px;
flex-wrap:wrap;
}


/* 上传按钮居中 */

.upload-section button,
.camera-section button{
display:block;
margin:30px auto;
}


/* 上传区域 */

.upload-area{
border:2px dashed #bbb;
border-radius:15px;
padding:30px;
background:rgba(255,255,255,0.95);
cursor:pointer;
text-align:center;
}

.upload-text{
font-size:18px;
font-weight:600;
color:#1a1a1a;
}

.upload-click{
color:#2e7d32;
font-weight:bold;
}

.upload-format{
color:#555;
font-size:14px;
}


/* 摄像头 */

.camera-video{
width:520px;
height:320px;
border-radius:15px;
object-fit:cover;
display:block;
margin:0 auto;
}


/* 视频预览 */

.video-preview{
display:flex;
justify-content:center;
}

.video-preview video{
width:520px;
margin-top:20px;
border-radius:15px;
}


/* 录制时间 */

.recording-time{
margin-top:10px;
color:red;
font-size:18px;
text-align:center;
}


/* 结果 */

.result-box{
margin-top:30px;
text-align:center;
}

.result-text{
font-size:22px;
color:#FFE4B5;
}

</style>