import request from '@/utils/request'

//依据请求得到当前用户的树状表结构
export function get_nodes_list(username) {
    return request({
        url: '/get_nodes_list/',
        method: 'get',
        params: { username }
    })
}
//传当前选中的节点path
export function post_selected_node(node_path) {
    return request({
        url: '/post_selected_node/',
        method: 'post',
        data: { node_path }
    })
}
//新增folder节点
export function post_new_folder(message) {
    return request({
        url: '/post_new_folder/',
        method: 'post',
        data: { message }
    })
}
//新增pdf节点
export function post_new_document(active_document_path) {
    return request({
        url: '/post_new_document/',
        method: 'post',
        data: { active_document_path }
    })
}
//删除节点
export function post_deleted_node(node_path) {
    return request({
        url: '/post_deleted_node/',
        method: 'post',
        data: { node_path }
    })
}


