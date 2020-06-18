<template>
    <div class="app-container">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-date"></i> 发文审核</el-breadcrumb-item>
                <el-breadcrumb-item>新建公文1111</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
        <el-tabs v-model="tabValue">
          <el-tab-pane :label="`公文录入`" name="first">              
            <div class="form-box">
            
              <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item>
                        <el-button type="primary" @click="handleAdd(-1,'')" style="float:right">导入公文</el-button>
                    </el-form-item>
                    <el-form-item label="公文名称">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <!--
                    <el-form-item label="公文日期">
                        <el-col :span="11">
                            <el-date-picker type="date" placeholder="开始日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
                        </el-col>
                        <el-col class="line" :span="2">-</el-col>
                        <el-col :span="11">
                            <el-date-picker placeholder="截止日期" v-model="form.date2" style="width: 100%;"></el-date-picker>
                        </el-col>
                    </el-form-item>
                   -->
                    <el-form-item label="公文内容">
                        <el-input type="textarea" rows="25" v-model="form.desc"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="firstToSecond">下一步</el-button>
                    </el-form-item>
                </el-form>
            </div>
          </el-tab-pane>
          <el-tab-pane :label="`上级依赖文件分析`" name="second" v-if="tabValueSecond">
                <el-table :data.async="supDoc" highlight-current-row style="width: 100%;">
                  <el-table-column type="index" label="序号" width="100">
                  </el-table-column>
                  <el-table-column prop="name" label="上级公文名称" min-width="160">
                  </el-table-column>
                  <el-table-column prop="exist" label="状态" min-width ="120" >
                  </el-table-column>
                  <el-table-column label="操作" width="300">
                    <template slot-scope="scope">
                     <el-button type="primary" size="small" @click="updateSupDocx(scope.$index,1,scope.row)">正确</el-button>
                     <el-button type="danger" size="small" @click="updateSupDocx(scope.$index,0,scope.row)"">错误</el-button>
                     <el-button type="primary" size="small" v-if="scope.row.is_analysised==false && scope.row.is_correct!=0" @click="handleAdd(scope.$index,scope.row)">上传公文</el-button>
                    </template>
                  </el-table-column>
              </el-table>
              <span style="color:gray;margin-top:5px">&nbsp&nbsp&nbsp注：若抽取的公文是上级依赖公文，请点击正确按钮；若抽取的公文不是上级依赖公文，请点击错误按钮！</span>

              <div style='margin-top:10px'>
              <el-button type="primary" @click="secondToThird">下一步</el-button>
              </div>
          </el-tab-pane>
          <el-tab-pane :label="`上级依赖文件分析`" name="second" disabled v-else>
          
          </el-tab-pane>
            <el-tab-pane :label="`审核结果`" name="third" v-if="tabValueThird">               
              <el-col v-for="(item,index) in matchingResult" :key="index" >
                    <div style='border: 1px solid #ddd;border-radius: 5px;padding-left:10px;padding-bottom:10px;margin-bottom:10px'>

                      <h5 class="count" style='color:red' v-if="item.is_correct==-1">段落：{{item.start}}（用户未确认）</h5>
                      <h5 class="count" v-if="item.is_correct==1">段落：{{item.start}}（用户确认正确）</h5>
                      <h5 class="count" v-if="item.is_correct==0">段落：{{item.start}}（用户确认错误）</h5>
                            <span class="splitLine" />
                            <p>原文：{{item.original}}</p>
                            <p>匹配段落：{{item.target}}</p>
                            <p>匹配得分：{{item.score}}</p>
                            <p>上级文件：《{{item.supName}}》</p>
                            <el-button type="primary" size="small" @click="updateResult(item.matchingId,1,item.start-1)">正确</el-button>
                            <el-button type="danger" size="small" @click="updateResult(item.matchingId,0,item.start-1)"">错误</el-button>
                    </div>
                    
                  </el-col>
               </el-row>
             
          </el-tab-pane>
          <el-tab-pane :label="`审核结果`" name="third" disabled v-else>
          
          </el-tab-pane>
        </el-tabs>

             
        </div>
         
      <div id="over" class="over" v-if="loading"></div>
      <div id="layout" class="layouts" v-if="loading"><img src="../../assets/images/loading.gif" /></div>

      <!--编辑界面-->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
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
   parseDocx,
   extractSupDoc,
   updateSupDoc,
   parseSupDoc,
   fetchMatchingResult,
   userConfirmMatching
  } from '@/api/upload'

  //根据上级文件的状态，返回exist内容
  function getExistText(is_correct,is_analysised)
    {
        var exists='待确认'
        switch(is_correct)
        {
           case 0:
              exists='确认错误'
              break
           case 1:
              exists='确认正确'
              break
        }
        if(is_analysised)
        {
           exists=exists+'（已存在）'
        }
        else
        {
           if(is_correct!=0)
              exists=exists+'（待上传）'
        }
        return exists
    }

  export default {
      name: 'baseform',
      data: function() {
        return {
          loading:false,
          isLoading:true,
          tabValue:'first',
          tabValueSecond:false,
          tabValueThird:false,
          supDoc:[],
          //公文在系统中的名称
          doc_id:0,
          dialogStatus: 'create',

          textMap: {
            update: '上传公文',
            create: '新建公文'
          },
          dialogFormVisible: false,
          editFormRules: {
            name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
          },
          fileList:[],
          fileName:'',
          uploadFileName:'',
          uploadFilePath:'',
          uploadSup:0,//判断是上传公文还是上传上级文件
          //记录上传公文是哪一行的数据
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

              //若是上传公文，需要同时解析公文
              if(this.uploadSup)
               {
                 this.loading=true
                 const para = {
                    inf_doc_id: this.doc_id,
                    file_name: this.fileName,
                    dir_path:this.uploadFilePath
                 }
                 parseSupDoc(para).then(res => {
                    //修改前端显示内容
                    if(this.uploadFileRowIndex>0)
                    {
                       this.supDoc[this.uploadFileRowIndex]['is_analysised']=true
                       var exists=getExistText(this.supDoc[this.uploadFileRowIndex]['is_correct'],this.supDoc[this.uploadFileRowIndex]['is_analysised'])
                       this.supDoc[this.uploadFileRowIndex]['exist']=exists
                    }
                    this.loading=false
                    this.$message({
                      message: '上级公文上传成功',
                      type: 'success'
                    })
                 })
              }
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