import flask
from flask import Flask, request, render_template, jsonify
#from flask_request_params import bind_request_params
from flask_cors import *
import os
import docx

server = flask.Flask(__name__)
CORS(server, supports_credentials=True)
@server.route('/upload_file', methods=['get', 'post'])
def upload_file():
  FILE_PATH='upload'
  #post请求获取请求的参数，返回结果类型是str
  #https://www.cnblogs.com/liuye1990/articles/10127424.html
  #print('header',request.headers)
  #print('method',request.method)
  #print('form',request.form)
  #print('args',request.args)
  #print('json',request.json)
  #print('values',request.values)
  #print('data',request.data)
  #print('files',request.files['file'].filename)
  file=request.files['file']
  if file:
    filename = file.filename
    file.save(os.path.join(FILE_PATH, filename))
    file=docx.Document(os.path.join(FILE_PATH, filename))
    content=''
    for para in file.paragraphs:
      content+='  '+para.text+'\n'
    return jsonify({"code": 0, "content": content})
  return jsonify({"code": 0, "msg": "上传文件失败"})
 
 
if __name__ == '__main__':
 #port可以指定端口，默认端口是5000
 #host默认是127.0.0.1,写成0.0.0.0的话，其他人可以访问，代表监听多块网卡上面，
 server.run(debug=True, port=8899, host='127.0.0.1')