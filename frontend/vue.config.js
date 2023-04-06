const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: "0.0.0.0",
    allowedHosts: "all",
    //https: true,
    server: "https",
    proxy: {
      "/api": {
        // '/api'是代理标识，用于告诉node，url前面是/api的就是使用代理的
        // target: "http://backend:5000/api/", //目标地址，一般是指后台服务器地址
        target: "http://backend:5000/api/",
        changeOrigin: true, //是否跨域
        pathRewrite: {
          // pathRewrite 的作用是把实际Request Url中的'/api'用""代替
          "^/api": "",
        },
      },
    },
  },
});
