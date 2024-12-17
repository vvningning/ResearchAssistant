import request from '@/utils/request'

export function sendQuestion(question) {
    return request({
        url: '/chat/',
        method: 'get',
        params: { question }
    })
}
