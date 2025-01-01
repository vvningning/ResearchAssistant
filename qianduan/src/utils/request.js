//引入axios，实现前台数据往后传
import axios from 'axios'
import router from "@/router"
//通过axios创建request对象
const request = axios.create({
    baseURL: "/api"
})

// request 拦截器
// 可以自请求发送前对请求做一些处理
// 比如统一加token，对请求参数统一加密
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    // let userJson = sessionStorage.getItem("username")
    // //为空,未登录，强制跳转到登录
    // if(!userJson)
    // {
    //     router.push("/login")
    // }
    return config
}, error => {
    return Promise.reject(error)
});

// response 拦截器
// 可以在接口响应后统一处理结果
request.interceptors.response.use(
    response => {
        //axios默认所有返回的数据都存放在data里面
        let res = response.data;
        // 如果是返回的文件
        if (response.config.responseType === 'blob') {
            return res
        }
        // 兼容服务端返回的字符串数据
        if (typeof res === 'string') {
            res = res ? JSON.parse(res) : res
        }
        return res;
    },
    error => {
        console.log('err' + error) // for debug
        return Promise.reject(error)
    }
)


export default request

