<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input v-model="listQuery.search" placeholder="请输入方案名称进行搜索"
        style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-refresh-left" @click="resetFilter">刷新重置</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增方案</el-button>
      <el-button type="primary" icon="el-icon-document" @click="handleResult">查看所有方案</el-button>
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
            <el-table-column property="userName" label="学号"></el-table-column>
            <el-table-column property="solutionName" label="方案名称"></el-table-column>
            <el-table-column property="taskName" label="任务名称"></el-table-column>
            <el-table-column property="codeAddr" label="代码地址"></el-table-column>
            <el-table-column property="solutionResult" label="方案结果"></el-table-column>
        </el-table>
    </el-dialog>
    <el-dialog :visible.sync="dialogTableAllVisible" title="方案详细信息" width="80%">
        <el-table :data="solutionList.results" border>
            <el-table-column property="userName" label="学号" ></el-table-column>
            <el-table-column property="solutionName" label="方案名称" ></el-table-column>
            <el-table-column property="taskName" label="任务名称" ></el-table-column>
            <el-table-column property="solutionResult" label="方案结果"></el-table-column>
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
        <el-form-item label="方案名称" prop="solutionName">
          <el-input v-model="solution.solutionName" placeholder="方案名称" />
        </el-form-item>
        <el-form-item label="任务名称" prop="taskName">

          <el-select v-model="solution.taskName" placeholder="请选择任务名称" style="width:100%">
            <el-option
            v-for="item in taskList"
             :key="item.id"
             :label="item.label"
             :value="item.task_name"
           />
          </el-select>
          </select>
        </el-form-item>

        <el-form-item label="代码地址" prop="solutionName">
          <el-input v-model="solution.codeAddr" placeholder="代码地址" />
        </el-form-item>
              <el-form-item label="上传文件" prop="dept">
                <el-upload
                  class="avatar-uploader"
                  :action="upUrl"
                  accept=".zip"
                  :show-file-list="false"
                  :on-success="handleAvatarSuccess"
                  :before-upload="beforeAvatarUpload"
                  :headers="upHeaders"
                >
                  <i class="el-icon-plus avatar-uploader-icon" />
                </el-upload>
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
import {getInfo} from "@/api/user";

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
        codeAddr: '',
        userName: ''
      },
      search: '',
      tableData: [],
      solutionList: {count:0},
      solutionShowList: [{
        id: '',
        solutionName: '',
        taskName: '',
        codeAddr: '',
        userName: '',
        solutionResult: ''
      }],
      listQuery: {
        page: 1,
        page_size: 20
      },
      taskList:[],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogTableAllVisible: false,
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
  },
  methods: {
    checkPermission,
    handleAvatarSuccess(res, file) {
      this.user.avatar = res.data.path
    },
    beforeAvatarUpload(file) {
      const notNull = file.size / 1024 / 1024 > 0;
      if (!notNull) {
        this.$message.error("文件不能为空");
      }
      return notNull;
    },
    getTaskAll() {
      getTaskAll().then(response => {
        this.taskList = genTree(response.data.results);
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
    handleResult() {
      this.dialogTableAllVisible = true
    },
    handleShow(scope) {
      this.solutionShowList[0].id = scope.row.id
      this.solutionShowList[0].solutionName = scope.row.solutionName
      this.solutionShowList[0].taskName = scope.row.taskName
      this.solutionShowList[0].codeAddr = scope.row.codeAddr
      this.solutionShowList[0].userName = scope.row.userName
      this.solutionShowList[0].solutionResult = scope.row.solutionResult
      this.dialogTableVisible = true
    },
    handleAdd() {
      getInfo().then(response => {
        console.log(response.data.username)
        this.solution.userName = response.data.username
        console.log(this.solution.userName)
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
