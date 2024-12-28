import request from '@/utils/request'

export function register(username, password, email) {
    return request({
        url: '/register/',
        method: 'get',
        params: { username, password, email }
    })
}