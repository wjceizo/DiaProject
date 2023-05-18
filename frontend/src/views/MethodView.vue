<template>

  <div >

    <h1>相似度分析方法介绍</h1>

    <p>本方法计算主要使用Python语言，包含库如librosa, pandas, numpy, scipy, sklearn, torch等，并使用了深度学习模型Wav2vec2.0。</p>
    
    <h3>计算文献分区</h3>
    <p>根据曹志耘先生的<a href="https://zh.wikipedia.org/wiki/%E6%BC%A2%E8%AA%9E%E6%96%B9%E8%A8%80%E5%9C%B0%E5%9C%96%E9%9B%86">汉语方言地图集</a>，得出文献分区，以便下面对比。</p>
    <div class="image-container">
      <img src="https://dialectr.oss-cn-hangzhou.aliyuncs.com/imgs/article/my_plots_jiangsu.png" alt="文献分区">
    </div>

    <h3>前处理</h3>
    <p>获取调查者的方言录音文件后，对音频文件进行处理，包括加载和重采样音频，计算短时傅里叶变换（STFT），计算分贝值，识别非静音部分，对齐音频头部和填充静音，以及保存处理后的音频。</p>
    <div class="image-container">
      <img src="https://dialectr.oss-cn-hangzhou.aliyuncs.com/imgs/article/before_process.png" alt="前处理">
    </div>
    
    <h3>特征提短时傅里叶变换（STFT）提取</h3>
    <p>使用Wav2vec2.0声学模型，通过对音频文件的处理以提取特征。</p>

    <h3>相似度矩阵</h3>
    <p>使用欧几里得法计算方言音频数据特征值之间的距离矩阵，并进行归一化处理以得到相似度矩阵。之后通过K均值，层次聚类，谱聚类对距离矩阵进行分析，并绘制树状图和热图。</p>
    <div class="image-row">
      <div class="image-container">
        <img src="https://dialectr.oss-cn-hangzhou.aliyuncs.com/imgs/article/complete_matrice.png" alt="前处理">
      </div>
      <div class="image-container">
        <img src="https://dialectr.oss-cn-hangzhou.aliyuncs.com/imgs/article/complete_distance.png" alt="前处理">
      </div>
    </div>
    
    <h3>几何剖分</h3>
    <p>使用Voronoi的算法来根据调查者地点的形心进行几何剖分，得出方言地图</p>

    <h3>后处理</h3>
    <p>对相似度矩阵进行分析，使用聚类算法如k均值，完全链接聚类和谱聚类对结果进行处理。</p>

    <h3>结果分析</h3>
    <p>对25个方言词汇合并进行预处理，分析后，得到一个新的相似度矩阵，并使用聚类算法进行分析。最后使用调整兰德指数将文献分区与聚类进行比较。</p>

  </div>

</template>

<style scoped>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      /* align-items: center; */
    }
  }

  p {
    text-align: justify;
    text-indent: 2em;
    font-size: larger;
  }

  .image-container {
    margin: 20px auto; /* Updated */
    width: 40%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .image-container img {
    max-width: 100%;
    height: auto;
  }

  .image-row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    flex-wrap: wrap;
  }

  .image-row .image-container {
    width: 48%;
    margin-bottom: 20px;
  }
</style>


