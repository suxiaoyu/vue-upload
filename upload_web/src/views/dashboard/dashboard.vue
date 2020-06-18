<template>
  <div class="app-container">
  <div class="item">
      <h4>统计数据展示</h4>
      <nx-data-icons :option="easyDataOption2"></nx-data-icons>
    </div>

    <div class="item">
      <h4>详细信息展示</h4>
      <nx-data-tabs :option="easyDataOption"></nx-data-tabs>
    </div>
  
    <div class="item">
        <h4>系统消息展示</h4>
        <div class="container">
            <el-tabs v-model="message">
                <el-tab-pane :label="`未读消息(${unread.length})`" name="first">
                    <el-table :data="unread" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title">{{scope.row.title}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="date" width="180"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button size="small" @click="handleRead(scope.$index)">标为已读</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="primary">全部标为已读</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane :label="`已读消息(${read.length})`" name="second">
                    <template v-if="message === 'second'">
                        <el-table :data="read" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="date" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button type="danger" @click="handleDel(scope.$index)">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">删除全部</el-button>
                        </div>
                    </template>
                </el-tab-pane>
                <el-tab-pane :label="`回收站(${recycle.length})`" name="third">
                    <template v-if="message === 'third'">
                        <el-table :data="recycle" :show-header="false" style="width: 100%">
                            <el-table-column>
                                <template slot-scope="scope">
                                    <span class="message-title">{{scope.row.title}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="date" width="150"></el-table-column>
                            <el-table-column width="120">
                                <template slot-scope="scope">
                                    <el-button @click="handleRestore(scope.$index)">还原</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <div class="handle-row">
                            <el-button type="danger">清空回收站</el-button>
                        </div>
                    </template>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
    
  </div>
</template>


<style>
.message-title{
    cursor: pointer;
}
.handle-row{
    margin-top: 30px;
}
</style>


<script>

import nxDataDisplay from '@/components/nx-data-display/nx-data-display'
import nxDataCard from '@/components/nx-data-card/nx-data-card'
import nxDataTabs from '@/components/nx-data-tabs/nx-data-tabs'
import nxDataIcons from '@/components/nx-data-icons/nx-data-icons'

export default {
  name: 'report',
  components: {
    nxDataDisplay,
    nxDataCard,
    nxDataTabs,
    nxDataIcons  
  },
  data() {
    return {
          message: 'first',
          showHeader: false,
          unread: [{
            date: '2020-04-19 20:00:00',
            title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
          }, {
            date: '2020-04-19 21:00:00',
            title: '海南省工商局提交文件B001-002待审核'
          }, {
            date: '2020-04-18 21:00:00',
            title: '海南省海口市交通局提交文件C001-021待审核'
          }, {
            date: '2020-04-16 21:00:00',
            title: '海南省海口市交通局文件C001-003已完成专家审核'
          }],
          read: [{
            date: '2020-04-19 20:00:00',
            title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
          }],
          recycle: [{
            date: '2020-04-19 20:00:00',
            title: '【系统通知】该系统将于今晚凌晨2点到5点进行升级维护'
          }],
      easyDataOption: {
        span: 6,
        data: [
          {
            title: '待提交政策公文',
            subtitle: '实时',
            count: 126,
            allcount: 10222,
            text: '关于深化改革推进出租车行业规范的相关...',
            time:'2020-01-22 00:00:00',
            text1: '海南省海口市人民政府关于改革野生动物...',
            time1:'2020-01-22 00:00:00',
            color: 'rgb(49, 180, 141)',
            key: '类'
          },
          {
            title: '待审核公文',
            subtitle: '实时',
            count: 3112,
            allcount: 10222,
            text: '关于深化改革推进出租车行业规范的相关...',
            time:'2020-01-22 00:00:00',
            text1: '海南省海口市人民政府关于改革野生动物...',
            time1:'2020-01-22 00:00:00',
            color: 'rgb(56, 161, 242)',
            key: '附'
          },
          {
            title: '已审核公文',
            subtitle: '实时',
            count: 908,
            allcount: 10222,
            text: '关于深化改革推进出租车行业规范的相关...',
            time:'2020-01-22 00:00:00',
            text1: '海南省海口市人民政府关于改革野生动物...',
            time1:'2020-01-22 00:00:00',
            color: 'rgb(117, 56, 199)',
            key: '评'
          },
          {
            title: '专家审核排名',
            subtitle: '实时',
            count: 908,
            allcount: 10222,
            text: '张文',
            time:'100条                   1',
            text1: '李文',
            time1:'80条                   2',
            color: 'rgb(59, 103, 164)',
            key: '新'
          }
        ]
      },

      easyDataOption2: {
        color: 'rgb(63, 161, 255)',
        span: 4,
        discount: true,
        data: [
         
          {
            title: '机构数量',
            count: 126,
            icon: 'icon-jiaoseguanli'
          },
          {
            title: '专家数量',
            count: 126,
            icon: 'icon-jiaoseguanli'
          },
          {
            title: '待审核公文',
            count: 120,
            icon: 'icon-caidanguanli'
          },
          {
            title: '待专家审核公文',
            count: 80,
            icon: 'icon-caidanguanli'
          },
          {
            title: '已审核公文',
            count: 600,
            icon: 'icon-caidanguanli'
          }
        ]
      }
    }
  },
  methods: {
        handleRead(index) {
          const item = this.unread.splice(index, 1)
          console.log(item)
          this.read = item.concat(this.read)
        },
        handleDel(index) {
          const item = this.read.splice(index, 1)
          this.recycle = item.concat(this.recycle)
        },
        handleRestore(index) {
          const item = this.recycle.splice(index, 1)
          this.read = item.concat(this.read)
        }
      },
  created() {},
  watch: {},
  mounted() {},
  computed: {
        unreadNum() {
          return this.unread.length
        }
      }
}

</script>

<style scoped>
.item {
  margin-bottom: 16px;
}
</style>
<style lang ="scss">
    @import '../../styles/data-card.scss';
    @import '../../styles/data-display.scss';
    @import '../../styles/data-icons.scss';
    @import '../../styles/data-tabs.scss';
</style>
