import request from '@/utils/request'

export function sendQuestion(question, paper_id) {
    return request({
        url: '/chat/',
        method: 'get',
        params: { question, paper_id }
    })
}
