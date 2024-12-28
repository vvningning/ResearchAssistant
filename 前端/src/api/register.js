import request from '@/utils/request'

export function register(username, password, email) {
    return request({
        url: '/register/',
        method: 'get',
        params: { username, password, email }
    })
}

export function sendVerification(email) {
    return request({
        url: '/sendVerification/',
        method: 'get',
        params: { email }
    })
}