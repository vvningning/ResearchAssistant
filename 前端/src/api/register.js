import request from '@/utils/request'

export function register(username, password, email, verification, sentVerification) {
    return request({
        url: '/register/',
        method: 'get',
        params: { username, password, email, verification, sentVerification }
    })
}

export function sendVerification(email) {
    return request({
        url: '/sendVerification/',
        method: 'get',
        params: { email }
    })
}