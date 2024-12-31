// 跨域配置
//让浏览器能从8080端口访问到9090端口
module.exports = {
    transpileDependencies: true,
    devServer: {                //记住，别写错了devServer//设置本地默认端口  选填
        port: 8080,
        proxy: {                 //设置代理，必须填
            '/api': {              //设置拦截器  拦截器格式   斜杠+拦截器名字，名字可以自己定
                target: 'http://localhost:8000',     //代理的目标地址
                changeOrigin: true,              //是否设置同源，输入是的
                pathRewrite: {                   //路径重写
                    '/api': ''                     //选择忽略拦截器里面的单词
                }
            },
            '/baiduapi': {
                target: 'http://api.fanyi.baidu.com/api/trans/vip/translate',  // 目标地址
                changeOrigin: true,  // 是否改变原始请求头中的Host字段
                pathRewrite: {
                    '^/baiduapi': '',  // 重写路径：将 /api 去掉
                },
            },
        }
    }
}