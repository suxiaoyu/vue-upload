import request from '@/utils/request'

export function uploadFile(params) {
  return request({
    url: 'http://127.0.0.1:8899/upload_file',
    method: 'post',
    params: params,
    data:params
  })
}

