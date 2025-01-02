import request from '@/utils/request'

export function sendQuestion(question, paper_id) {
    return request({
        url: '/chat/',
        method: 'get',
        params: { question, paper_id }
    })
}

export function showChatHistory(paper_id) {
    return request({
        url: '/show_history/',
        method: 'get',
        params: { paper_id }
    })
}

export function clearChat(paper_id) {
    return request({
        url: '/clear_chat/',
        method: 'post',
        data: { paper_id }
    });
}
