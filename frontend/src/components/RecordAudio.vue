<template>
    <nav>
        <ul>
            <li><a href="/" @click.prevent="confirmBackToMainPage">回到首页</a></li>
        </ul>
    </nav>

    <div class="mobile-container">
        <h1>录制您的声音</h1>
        <h3>完成度：{{ wordId ? `${(wordId - 1)} / 25` : 0 }}</h3>
        <div class="data-container" v-if="!isLoading">
            <p>{{ prompt }}</p>
            <div class="btn-container"><button class="hint" v-if="!clickedStem" @click="showStem">提示</button></div>
            <div class="hint-text" v-if="clickedStem">
                <p>{{ stem }}</p>
            </div>
            <div class="img-container">
                <!-- <img :src="img" alt="Dialect image" /> -->
                <img :src="`/dialect_imgs/${wordId ? wordId : 1}.webp`" alt="Dialect image" />
            </div>
            <p class="desc">{{ desc }}</p>
        </div>
        <div v-if="isLoading">
            <p>正在加载...</p>
        </div>
        <div class="recorder-container">
            <button id="btn-record" class="btn" :class="{ 'btn-primary': !isRecording, 'btn-danger': isRecording }"
                @click="startRecording" v-if="!isCompleted">
                {{ isRecording ? '结束录音' : recorded ? '重新录制' : '录音' }}
            </button>
            <span style="display:inline-block;width: 3em" v-if="recorded"></span>
            <button id="btn-replay" class="btn btn-primary" @click="playRecording" v-if="recorded">播放录音</button>
            <audio ref="audioPlayer"></audio>
        </div>

        <button id="btn-submit" class="btn btn-primary" @click="next" :disabled="!recorded || submitIsDisabled" v-if="!isCompleted">
            {{ wordId < 25 ? '下一个' : '完成' }} </button>
    </div>
</template>
<style scoped>
.mobile-container {
    max-width: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

h1,
h3 {
    margin-top: 0;
}

.btn.btn-danger {
    background-color: red !important;
    border-color: red !important;
}

.img-container {
    height: 300px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

button {
    display: block;
    width: 100%;
    margin-bottom: 0;
    font-size: 16px;
    padding: 12px;
    border-radius: 4px;
    border: none;
    background-color: #007bff;
    color: #fff;
}

div.data-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

div.btn-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

div.recorder-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

#btn-record {
    width: 100%;
}

#btn-submit {
    width: 100%;
    margin-top: 16px;
}

button.hint {
    background-color: #6c757d;
    width: 15%;
    min-width: fit-content;
    height: 3em;
    margin: 0.5rem auto;
}

div.hint-text {
    font-size: 16px;
    color: #6c757d;
    height: 3em;
    display: flex;
    margin: 0.5rem auto;
}

div.hint-text p {
    margin: auto;
    align-items: center;
}

.desc {
    margin-top: 0.3em;
    display: flex;
    font-size: 16px;
    color: #6c757d;
    height: 2.5em;
}


/* navibar temp */
nav {
    display: block;
    background-color: #2182ea;
    border-bottom: 1px solid #e7e7e7;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    height: 50px;
    line-height: 50px;
    position: relative;
    top: 0;
    width: 100%;
    z-index: 100;
    text-align: start;
}

ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

li {
    display: inline-block;
    margin: 0 10px;
    font: 14px/1.5 "Helvetica Neue", Helvetica, Arial, sans-serif;
}

a {
    color: #ccc;
    text-decoration: none;
}

a:hover {
    color: #ccc;
    text-decoration: none;
}

a:active {
    color: #ccc;
    text-decoration: none;
}

a:visited {
    color: #ccc;
    text-decoration: none;
}

a:link {
    color: #ccc;
    text-decoration: none;
}
</style>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useStore } from 'vuex';
import { MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';



export default {

    setup() {
        const store = useStore();
        const accessToken = store.getters.accessToken;
        const wordId = store.getters.wordId;
        return {
            accessToken, wordId
        };
    },

    data() {
        return {
            img: '',
            desc: '',
            stem: '',
            prompt: '',
            isLoading: false,
            clickedStem: false,
            isRecording: false,
            mediaRecorder: null,
            recordedChunks: [],
            audioBlob: null,
            recorded: false,
            isCompleted: false,
            submitIsDisabled: false,
        };
    },
    beforeMount() {
        this.reau();
    },
    created() {
        this.fetchWord();
    },
    methods: {


        showStem() {
            this.clickedStem = true;
        },


        async fetchWord() {
            this.isLoading = true;
            this.submitIsDisabled = false;
            try {
                const response = await axios.get(`/api/audio/word/${this.wordId}`);
                // this.img = response.data.img;
                this.desc = response.data.desc;
                this.prompt = response.data.prompt;
                this.stem = response.data.stem;
                this.isLoading = false;
            } catch (error) {
                console.error('Error fetching word:', error);
            }
        },

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

        async blobToBase64(blob) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });
        },

        async calculateMD5(data) {
            const buffer = new Uint8Array(data);
            const digest = await crypto.subtle.digest('MD5', buffer);
            const digestArray = new Uint8Array(digest);
            return Array.from(digestArray).map(b => b.toString(16).padStart(2, '0')).join('');
        },

        async uploadRecording() {
            if (!this.audioBlob)
                return;

            try {
                this.submitIsDisabled = true;
                const base64Audio = await this.blobToBase64(this.audioBlob);
                const base64String = base64Audio.split(',')[1];
                console.log(base64Audio, this.wordId, this.stem)
                const response = await axios.post('/api/userRecord/upload', {
                    record_file: base64String,
                    word_id: this.wordId,
                    audio_feat: this.stem,
                }, {
                    headers: {
                        'Authorization': `Bearer ${this.accessToken}`,
                    },
                });

                if (response.data.status === 201) {
                    console.log('Recording uploaded successfully');
                }
            } catch (error) {
                console.error('Error uploading recording:', error);
            }
        },

        confirmBackToMainPage() {
            if (confirm('确认要回到主页吗？未完成的录音调查将不被保存。')) {
                this.$store.commit('setAccessToken', '');
                this.$store.commit('setWordId', 1);
                window.location.href = '/';
            }
        },

        async next() {
            if (this.isRecording) {
                this.mediaRecorder.stop();
                this.isRecording = false;
            }

            await this.uploadRecording();
            this.recorded = false

            if (this.wordId < 25) {
                this.wordId++;
                this.clickedStem = false;
                console.log("wordId:" + this.wordId);
                localStorage.setItem('wordId', this.wordId);
                this.fetchWord();
            } else {
                this.isCompleted = true;
                this.$router.push('/record-complete');
            }
        },
    },
};
</script>