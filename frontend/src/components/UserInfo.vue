<template>
  <div class="intro">
    <h2>Dialectr</h2>
    <h3>为什么要调查方言</h3>
    <p>自 20 世纪以来，方言一直是语言学家的研究课题，也是民众饶有兴趣的聊天话题。通过方言调查，可以了解一个语言社区的语音差异和相似性，定量计算<a
        href="https://en.wikipedia.org/wiki/Linguistic_distance" target="_blank" rel="noopener noreferrer"
        title="linguistic distance">语言距离</a>，理解或收集语言形式的细节，这也是<a href="https://en.wikipedia.org/wiki/Dialectology"
        target="_blank" rel="noopener noreferrer" title="dialectology">方言学</a>所关注的内容。</p>
    <h3>如何调查</h3>
    <p>我们采用在互联网发布互动问卷的方式收集方言资料，尤其是语音数据。通过我们的页面，您可以通过近似游戏的形式，在看图说话的互动中完成调查问卷。</p>
    <p>访问我们的页面时，需要浏览器授权使用您的设备录音权限，这通常可以通过几次轻松的点击完成。您可以在下面的录音测试中调试麦克风。</p>
    <p>点击<span class="button">录音</span>按钮可以录制声音，录音完成后点击<span class="button">结束录音</span>按钮完成一次录音。如果对录音不满意，您可以点击<span
        class="button">重新录制</span>按钮。录制的声音可以回放试听。</p>
    <p>每一个页面通常只需调查一项内容。当完成录音之后，就可以点击<span class="button">下一个</span>按钮来推进调查进度。本次调查大约占用您5分钟时间。</p>
    <h3>录音测试</h3>
    <p>录音时，请尽量保持环境安静，以免影响录制效果。</p>
    <div class="recorder-container">
      <button id="btn-record" class="btn" :class="{ 'btn-primary': !isRecording, 'btn-danger': isRecording }"
        @click="startRecording" v-if="!isCompleted">
        {{ isRecording ? '结束录音' : recorded ? '重新录制' : '录音' }}
      </button>
      <span style="display:inline-block;width: 3em" v-if="recorded"></span>
      <button id="btn-replay" class="btn btn-primary" @click="playRecording" v-if="recorded">播放录音</button>
      <audio ref="audioPlayer"></audio>
    </div>
    <h3>我们是谁</h3>
    <p>我们是来自高校的方言学科研团队，同时也是乡土文化的爱好者和实践者。欢迎来自社会各界的指导和建议！</p>
    <button id="btn-submit" class="btn btn-primary" @click="next">我已阅读，开始录音</button>
  </div>
</template>
<style scoped>
.intro {
  max-width: 100%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.intro h2 {
  width: 90%;
  font-size: 56px;
  font-weight: 600;
  color: transparent;
  background-image: linear-gradient(to right, #553c9a, #ee4b2b, #00c2cb, #ff7f50, #553c9a);
  -webkit-background-clip: text;
  background-clip: text;
  background-size: 140%;
  background-position: -140%;
  transition: all ease-in-out 2s;
  cursor: pointer;
  text-align: center;
  margin: 0 auto;
}

.intro h2:hover {
  background-position: 140%;
}

.intro h3 {
  text-align: center;
  margin: 1rem auto;
}

.intro h3::before {
  content: '🎤 ';
}

.intro h3::after {
  content: ' 🎤';
}

.intro p {
  text-align: start;
  text-indent: 2em;
  margin: 0.3rem auto;
  line-height: 1.8em;
  max-width: 90%;
  font: 1.2em sans-serif;
}

.intro span.button {
  background-color: #4285f4;
  border: 1px solid #3bafda;
  border-radius: 8px;
  padding: 2px 4px;
  margin-left: 0.2em;
  margin-right: 0.2em;
  color: #eee;
  white-space: nowrap;
  font: 0.7em sans-serif;
}

.intro a {
  text-decoration: none;
  color: #4285f4;
}

*[title] {
  text-decoration: none;
  color: #3bafda;
  font-weight: bold;
}


.btn.btn-danger {
  background-color: red !important;
  border-color: red !important;
}

div.recorder-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

div.btn-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

button {
  display: block;
  width: 100%;
  max-width: 16rem;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 16px;
  padding: 12px;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: #fff;
}

#btn-record {
  width: 100%;
}

#btn-submit {
  width: 100%;
  margin-top: 16px;
}
</style>


<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import { MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';

export default {
  data() {
    return {
      recorded: false,
      isRecording: false,
      isCompleted: false
    };
  },

  beforeMount() {
    this.reau();
  },

  methods: {
    async reau() {
      await register(await connect());
    },

    startRecording() {
      console.log('start recording')
      if (!this.isRecording) {
        this.isRecording = true;
        this.recordedChunks = [];
        const mediaConstraints = {
          audio: true
        };
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          navigator.mediaDevices.getUserMedia(mediaConstraints)
            .then((stream) => {
              this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/wav' });
              this.mediaRecorder.start();

              this.mediaRecorder.addEventListener('dataavailable', (event) => {
                if (event.data.size > 0) {
                  this.recordedChunks.push(event.data);
                }
              });

              this.mediaRecorder.addEventListener('stop', () => {
                this.audioBlob = new Blob(this.recordedChunks, { type: 'audio/wav' });
                // Now you can upload or update the recorded audio.
                this.recorded = true;
              });
            })
            .catch((error) => {
              console.error('Error starting recording:', error);
              alert('无法访问麦克风，请检查您的设备权限设置。');
              this.isRecording = false;
            });
        } else {
          alert('您的浏览器不支持录音功能，请尝试使用其他浏览器。');
          this.isRecording = false;
        }
      } else {
        if (this.mediaRecorder) {
          this.isRecording = false;
          this.mediaRecorder.stop();
        } else {
          console.error('MediaRecorder is not available.');
        }
      }
    },

    playRecording() {
      if (this.recorded) {
        this.audioUrl = URL.createObjectURL(this.audioBlob);
        const audioPlayer = this.$refs.audioPlayer;
        audioPlayer.src = this.audioUrl;
        audioPlayer.play();
      }
    },
    async next() {
      this.$store.commit('setAccessToken', '');
      this.$store.commit('setWordId', 1);
      this.$router.replace('/user-registration');
    },
  },
}

</script>