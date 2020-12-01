<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input v-model="listQuery.search" placeholder="请输入方案名称进行搜索"
        style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-refresh-left" @click="resetFilter">刷新重置</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增方案</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="solutionList.results"
      style="width: 100%;margin-top:10px;"
      border
      fit
      stripe
      highlight-current-row
      max-height="600"
      row-key="id"
    >
      <el-table-column type="index" width="50" />

      <el-table-column label="方案名称">
        <template slot-scope="scope">{{ scope.row.solutionName }}</template>
      </el-table-column>

      <el-table-column label="任务名称">
        <template slot-scope="scope">{{ scope.row.taskName }}</template>
      </el-table-column>

      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button
            type="info"
            size="small"
            icon="el-icon-view"
            :disabled="!checkPermission(['solution_query'])"
            @click="handleShow(scope)"
            title="查看方案详情"
          />
          <el-button
            type="primary"
            size="small"
            icon="el-icon-edit"
            :disabled="!checkPermission(['solution_update'])"
            @click="handleEdit(scope)"
            title="修改"
          />
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            :disabled="!checkPermission(['solution_delete'])"
            @click="handleDelete(scope)"
            title="删除"
          />
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogTableVisible" title="方案详细信息" width="80%">
        <el-table :data="solutionShowList" border>
            <el-table-column property="userName" label="用户名"></el-table-column>
            <el-table-column property="solutionName" label="方案名称"></el-table-column>
            <el-table-column property="taskName" label="任务名称"></el-table-column>
            <el-table-column property="solutionResult" label="方案结果"></el-table-column>
          <el-table-column property="solution_status" label="方案状态"></el-table-column>
        </el-table>
    </el-dialog>


    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑方案':'新增方案'">
      <el-form
        ref="Form"
        :model="solution"
        label-width="80px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="任务名称" prop="taskName">

          <el-select v-model="solution.taskName" placeholder="请选择任务名称" style="width:100%">
            <el-option
            v-for="item in taskList"
             :key="item.id"
             :label="item.label"
             :value="item.task_name"
           />
          </el-select>
        </el-form-item>

        <el-form-item label="上传方案">
          <el-upload
            ref="upload"
            class="upload-demo"
            accept=".zip"
            :action="upUrl"
            :before-upload="beforeUpload"
            :headers="upHeaders"
            :on-success="UploadSuccess"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传zip文件</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="方案名称" prop="solutionName">
          <el-input v-model="solution.solutionName" :disabled="true" placeholder="方案名称" />
        </el-form-item>
      </el-form>

      <div style="text-align:right;">
        <el-button type="danger" @click="dialogFormVisible=false">取消</el-button>
        <el-button type="primary" @click="confirm('Form')">确认</el-button>
      </div>
    </el-dialog>
    <pagination
      v-show="solutionList.count>0"
      :total="solutionList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
  </div>
</template>

<script>
import {
  getSolutionList,
  getSolutionAll,
  createSolution,
  deleteSolution,
  updateSolution
} from '@/api/solution'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'
import {getTaskAll} from "@/api/task";
import {upHeaders, upUrl} from "@/api/file";
import Pagination from "@/components/Pagination"
import {getInfo, getUserAll} from "@/api/user";


const defaultM = {
  id: '',
  solutionName: ''
}
export default {
  components: { Pagination },
  data() {
    return {
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      solution: {
        id: '',
        solutionName: '',
        taskName: '',
        userId: ''
      },
      search: '',
      tableData: [],
      solutionList: {count:0},
      solutionShowList: [{
        id: '',
        solutionName: '',
        taskName: '',
        userName: '',
        solutionResult: '',
        solution_status: ''
      }],
      listQuery: {
        page: 1,
        page_size: 20
      },
      taskList:[],
      user: [],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogType: 'new',
      rule1: {
        solutionName: [{ required: true, message: '请输入名称', trigger: 'blur' }]
      }
    }
  },
  computed: {},
  created() {
    this.getList()
    this.getTaskAll()
    this.getUserAll()
  },
  methods: {
    checkPermission,
    UploadSuccess(res,file) {
      var str=res.data.name;
      this.solution.solutionName=str.substr(0,str.length -4);
    },
    beforeUpload(file) {                //返回fasle停止上传,检查压缩包名称和格式
      const isZip = file.name.endsWith('.zip');
      if(!isZip){
        this.$message.error('请选择zip文件！');
        return false;
      }
      else return true;
    },
    getTaskAll() {
      getTaskAll().then(response => {
        this.taskList = genTree(response.data.results);
      });
    },
    getUserAll() {
      getUserAll().then(response => {
        this.user = genTree(response.data.results);
      });
    },
    getList() {
      this.listLoading = true;
      getSolutionList(this.listQuery).then(response => {
        if (response.data) {
          this.solutionList = response.data
        }
        this.listLoading = false;
      });
    },
    resetFilter() {
      this.listQuery = {
        page: 1,
        page_size: 20
      };
      this.getList();
    },
    handleFilter() {
      this.listQuery.page = 1;
      this.getList();
    },
    handleShow(scope) {
      // this.solutionShowList[0].id = scope.row.id
      this.solutionShowList[0].solutionName = scope.row.solutionName
      this.solutionShowList[0].taskName = scope.row.taskName
      for (var i = 0; i < this.user.length; i++) {
        if (this.user[i].id == scope.row.userId) {
          this.solutionShowList[0].userName = this.user[i].username
        }
      }
      this.solutionShowList[0].solutionResult = scope.row.solutionResult
      this.solutionShowList[0].solution_status = scope.row.solution_status
      this.dialogTableVisible = true
    },
    handleAdd() {
      getInfo().then(response => {
        this.solution.userId = response.data.id
      })
      this.solution = Object.assign({}, defaultM)
      this.dialogType = 'new'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {
      this.solution = Object.assign({}, scope.row)
      this.dialogType = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleDelete(scope) {
      console.log(scope)
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          // console.log("这里")
          // console.log(scope.row.solutionId)
          await deleteSolution(scope.row.solutionId)
          // console.log(scope.row.id)
          this.getList()
          this.$message({
            type: 'success',
            message: '成功删除!'
          })
        })
        .catch(err => {
          console.error(err)
        })
    },
    async confirm(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          const isEdit = this.dialogType === 'edit'
          if (isEdit) {
            // console.log(this.solution)
            updateSolution(this.solution.solutionId, this.solution).then(() => {
              this.getList()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
          } else {
            createSolution(this.solution).then(res => {
              this.getList()
              this.$refs.upload.clearFiles()
              this.dialogFormVisible = false
              this.$message({
                message: '新增成功',
                type: 'success',
              })
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>
