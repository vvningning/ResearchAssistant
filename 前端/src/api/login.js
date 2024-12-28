import request from '@/utils/request'

export function sendUser(username, password) {
    return request({
        url: '/login/',
        method: 'get',
        params: { username, password }
    })
}