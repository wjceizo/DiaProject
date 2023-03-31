<template>
    <div>
        <h1>Upload Recording</h1>
        <h3>完成度：{{ (wordId / 3 * 100).toFixed(0) }}%</h3>
        <div class="img-container">
            <img :src="img" alt="Dialect image" />
        </div>
        <p>{{ desc }}</p>
        <button class="btn btn-primary" @click="startRecording" v-if="!isCompleted">{{ isRecording ? 'End Recording' : recorded ? 'UpdateRecord' : 'Record' }}</button>
        <button class="btn btn-primary" @click="next" :disabled="!recorded" v-if="!isCompleted">
            {{ wordId < 3 ? 'Next' : 'Complete' }} </button>
    </div>
</template>

<style scoped>
.img-container img {
    max-height: 50vh;
    object-fit: contain;
    width: auto;
}
</style>

<script>
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useStore } from 'vuex';

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
            isRecording: false,
            mediaRecorder: null,
            recordedChunks: [],
            audioBlob: null,
            recorded: false,
            isCompleted: false
        };
    },
    created() {
        this.fetchWord();
    },
    methods: {


        async fetchWord() {
            try {
                const response = await axios.get(`/api/audio/word/${this.wordId}`);
                this.img = response.data.img;
                this.desc = response.data.desc;
                this.stem = response.data.stem;
            } catch (error) {
                console.error('Error fetching word:', error);
            }
        },

        startRecording() {
            console.log('start recording')
            if (!this.isRecording) {
                this.isRecording = true;
                this.recordedChunks = [];

                const mediaConstraints = { audio: true };
                if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                    navigator.mediaDevices.getUserMedia(mediaConstraints)
                        .then((stream) => {
                            this.mediaRecorder = new MediaRecorder(stream);
                            this.mediaRecorder.start();

                            this.mediaRecorder.addEventListener('dataavailable', (event) => {
                                if (event.data.size > 0) {
                                    this.recordedChunks.push(event.data);
                                }
                            });

                            this.mediaRecorder.addEventListener('stop', () => {
                                this.audioBlob = new Blob(this.recordedChunks, { type: 'audio/webm' });
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

                const base64Audio = await this.blobToBase64(this.audioBlob);
                // const md5 = await this.calculateMD5(this.audioBlob);
                const base64String = base64Audio.split(',')[1];
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



        async next() {
            if (this.isRecording) {
                this.mediaRecorder.stop();
                this.isRecording = false;
            }

            await this.uploadRecording();
            this.recorded = false

            if (this.wordId < 3) {
                this.wordId++;
                console.log("wordId:" + this.wordId)
                localStorage.setItem('wordId', this.wordId);
                this.fetchWord();
            } else {
                this.isCompleted = true
                // this.$emit('recordings-completed');
                this.$router.push('/record-complete');
            }
        },
    },
};
</script>