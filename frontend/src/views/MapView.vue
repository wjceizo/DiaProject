<template>
  <div class="container">
    <h1>相似度查看及试听录音</h1>
    <div class="map-container">
      <l-map ref="map" v-model:zoom="zoom" :center="[32.91322, 119.719482]" :bounds="bounds" :max-bounds="bounds"
        :min-zoom="7" :max-zoom="10">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
          name="OpenStreetMap"></l-tile-layer>
        <l-geo-json :geojson="geojson" :options-style="geoStyler" @click="onPolygonClick"></l-geo-json>
      </l-map>
    </div>
    <div class="word-container">
  <div class="word-selection">
    <h3>选择词组：</h3>
    <select v-model="selectedWord" @change="updateWord">
      <option value="">请选择</option>
      <option v-for="(value, word) in wordDict" :value="word" :key="word">{{ word }}</option>
    </select>
  </div>
  <div v-if="selectedTown" class="town-info">
    <h3>选择的地点是:</h3>
    <p>{{ selectedTown }}</p>
    <div class="audio-container">
      <audio v-if="audioUrl" ref="audio" :src="audioUrl" @ended="onAudioEnded"></audio>
      <button v-if="audioUrl" @click="playAudio">Play audio</button>
    </div>
  </div>
</div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import { LGeoJson, LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
  },
  data() {
    return {
      zoom: 7,
      geojson: undefined,
      geoStyler: (feature) => {
        const colors = ["#FF5733", "#7D3C98", "#3498DB", "#27AE60", "#F1C40F", "#E74C3C"];
        const colorIndex = feature.properties.kmeans % colors.length;
        const fillColor = colors[colorIndex];
        return {
          fillColor: fillColor,
          fillOpacity: 0.5,
          weight: 2,
          color: "#333",
        };
      },
      bounds: [[29.573269, 115.267639], [36.039063, 124.122787]],
      selectedTown: null,
      audioUrl: null,
      selectedWord: "心", // 设置默认选项为"心"
      wordDict: { // 创建词组与数字的字典
        "心": 1,
        "耳": 2,
        "冰": 3,
        "火": 4,
        "骨": 5,
        "肉": 6,
        "狗": 7,
        "鱼": 8,
        "手": 9,
        "尾": 10,
        "路": 11,
        "死": 12,
        "云": 13,
        "地": 14,
        "蟹": 15,
        "水": 16,
        "红": 17,
        "白": 18,
        "圆": 19,
        "咬": 20,
        "听": 21,
        "站": 22,
        "说": 23,
        "我和我的祖国": 24,
        "如果明天下雪": 25
      },
    };
  },
  async created() {
    this.updateWord(); // 调用 updateWord 方法以加载默认词组的地图数据
  },

  methods: {
    onPolygonClick(e) {
      this.selectedTown = e.layer.feature.properties.town;
      const userId = e.layer.feature.properties.user;
      const wordIndex = this.wordDict[this.selectedWord]; // 获取选择词组对应的数字
      const geojsonUrl = `https://raw.githubusercontent.com/wjceizo/DiaProject/main/geojson/wav${wordIndex}.geojson`; // 更新 geojson 的 URL
      const audioUrl = `https://dialectr.oss-cn-hangzhou.aliyuncs.com/audios/Wav/${wordIndex}/${userId}_${wordIndex}.wav`; // 更新音频的 URL
      this.loadGeojson(geojsonUrl); // 加载新的 geojson 数据
      this.audioUrl = audioUrl; // 更新音频 URL
    },
    playAudio() {
      this.$refs.audio.play();
    },
    onAudioEnded() {
      this.audioUrl = null;
    },
    updateWord() {
      this.selectedTown = null; // 重置已选城镇
      this.audioUrl = null; // 重置音频 URL
      const wordIndex = this.wordDict[this.selectedWord]; // 获取选择词组对应的数字
      const geojsonUrl = `https://raw.githubusercontent.com/wjceizo/DiaProject/main/geojson/wav${wordIndex}.geojson`; // 更新 geojson 的 URL
      this.loadGeojson(geojsonUrl); // 加载新的 geojson 数据
    },
    async loadGeojson(url) {
      const response = await fetch(url);
      this.geojson = await response.json();
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
}

.word-container {
  display: flex;
  gap: 20px; /* 调整间距大小 */
}

.word-selection,
.town-info {
  flex: 1;
}

h1 {
  margin-top: 20px;
}

.map-container {
  margin: 20px auto;
  height: 65vh;
  width: 70vw;
}

.town-info {
  margin-top: 20px;
}

.audio-container {
  margin-top: 10px;
}

.word-selection {
  margin-top: 20px;
}

select {
  padding: 5px;
  font-size: 16px;
}

button {
  padding: 5px 10px;
  font-size: 16px;
  background-color: #3498DB;
  color: #FFF;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #27AE60;
}

p {
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
}


</style>
