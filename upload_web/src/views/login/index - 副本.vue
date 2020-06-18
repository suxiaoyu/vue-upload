<template>
    <div class="app-container">
        
        <div class="container">
         <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item>
                        <el-button type="primary" @click="handleAdd(-1,'')" style="float:right">导入文件</el-button>
                    </el-form-item>
                    <el-form-item label="文件名称">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="文件内容">
                        <el-input type="textarea" rows="25" v-model="form.desc"></el-input>
                    </el-form-item>
                </el-form>

             
        </div>
         

      <!--编辑界面-->
    <el-dialog :title="导入文件" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
      <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
         <el-upload
           class="upload-demo"
            ref="upload"
            action="doUpload"    
           :file-list="fileList"
           :before-upload="beforeUpload">
           <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
      
           <div slot="tip" class="el-upload__tip">只能上传一个word文件，且大小不超过5MB</div>
           <div slot="tip" class="el-upload-list__item-name">{{fileName}}</div>
         </el-upload> 

      </el-form>
      <div slot="footer" class="dialog-footer">
       <el-button @click.native="dialogFormVisible=false">取消</el-button>
        <el-button type="primary" @click="submitUpload()">确定上传</el-button>
      </div>
    </el-dialog>


    </div>
</template>

<script>
  import {
   uploadFile,
  } from '@/api/upload'

  export default {
      name: 'baseform',
      data: function() {
        return {
          supDoc:[],
          //文件在系统中的名称
          doc_id:0,
          dialogFormVisible: false,
          editFormRules: {
            name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
          },
          fileList:[],
          fileName:'',
          uploadFileName:'',
          uploadFilePath:'',
          uploadSup:0,//判断是上传文件还是上传上级文件
          //记录上传文件是哪一行的数据
          uploadFileRowIndex:-1,
          matchingResult:[],
          // 编辑界面数据
          editForm: {
          id: '0',
            name: '',
            sex: 1,
            age: 0,
            birth: '',
            addr: ''
          },
          form: {
            name: '',
            region: '',
            date1: '',
            date2: '',
            delivery: true,
            type: ['步步高'],
            resource: '小天才',
            desc: '',
            options: []
          }
        }
      },
      methods: {      
        //上传文档
        //校验
    beforeUpload(file){
      this.files = file;
      const extension = file.name.split('.')[1] === 'doc'
      const extension2 = file.name.split('.')[1] === 'docx'
      const isLt2M = file.size / 1024 / 1024 < 5

      if (!extension && !extension2) {
       this.$message.warning('上传模板只能是 doc、docx格式!')
       return
      }
      if (!isLt2M) {
       this.$message.warning('上传模板大小不能超过 5MB!')
       return
      }
      this.fileName = file.name;
      this.form.name=file.name.split('.')[0]

      return false // 返回false不会自动上传
    },
    //上传文档
    submitUpload() {

        this.$confirm('确认上传吗?').then(() => {
          if(this.files){
            let fd = new FormData()
            fd.append('file',this.files,this.fileName)
            fd.append('password','passwordsusu')
            uploadFile(fd).then(res => {
              this.$refs['editForm'].resetFields()
              this.dialogFormVisible = false
              this.form.desc=res.content
              this.uploadFileName=res.filename
              this.uploadFilePath=res.filepath
            })
            
         }
         else
          {
            alert('请选择文件后上传');
          }
        })
        .catch(() => {
         this.$message({
              message: '保存成功',
              type: 'success'
            })
        })
    },
    
    // 显示上传界面
    handleAdd(index,row) {
          if(index>-1)
          {
             this.uploadSup=1
             this.dialogStatus='update'
             this.uploadFileRowIndex=index
          }
          else
          {
             this.uploadSup=0
             this.dialogStatus='create'
          }
          this.dialogFormVisible = true
          this.fileName=''
          this.editForm = {
           id: '0',
           name: '',
           sex: 1,
           age: 0,
           birth: '',
           addr: ''
        }
    },
   

      }
    }
</script>
<style>
    .over {
             position: fixed;
             top: 0;
             left: 0;
             width: 100%;
             height: 100%;
             background-color: #f5f5f5;
             opacity:0.5;
             z-index: 5000;
         }
 
         .layouts {
             position: fixed;
             top: 40%;
             left: 40%;
             width: 20%;
             height: 20%;
             z-index: 5000;
             text-align:center;
         }
</style>