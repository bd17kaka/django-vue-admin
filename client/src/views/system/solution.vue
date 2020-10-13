<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入方案名称进行搜索"
        style="width: 200px;"
        class="filter-item"
        @keyup.native="handleFilter"
      />
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增方案</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="tableData.filter(data => !search || data.solutionName.toLowerCase().includes(search.toLowerCase()))"
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

<!--      <el-table-column label="创建日期">-->
<!--        <template slot-scope="scope">-->
<!--          <span>{{ scope.row.create_time }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->

<!--      <el-table-column label="任务描述">-->
<!--        <template slot-scope="scope">-->
<!--          <span>{{ scope.row.description }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->

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
            :disabled="!checkPermission(['solutionUpdate'])"
            @click="handleEdit(scope)"
            title="修改"
          />
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            :disabled="!checkPermission(['solutionDelete'])"
            @click="handleDelete(scope)"
            title="删除"
          />
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogTableVisible" title="方案详情">
        <el-table >
            <el-table-column property="solutionName" label="方案名称" width="50">
                    <template scope="scope"><span>{{ scope.row.solutionName }}</span></template>
            </el-table-column>
            <el-table-column property="task_type" label="任务类型" width="50"></el-table-column>
            <el-table-column property="create_time" label="创建日期" width="100"></el-table-column>
            <el-table-column property="update_time" label="修改日期" width="100"></el-table-column>
            <el-table-column property="matched_dataset" label="数据集" width="100"></el-table-column>
            <el-table-column property="description" label="任务描述" width="100"></el-table-column>
            <el-table-column property="task_status" label="任务状态" width="100"></el-table-column>
        </el-table>
    </el-dialog>

    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑岗位':'新增方案'">
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
<!--        <el-form-item label="任务名称" prop="taskName">-->
<!--          <el-input v-model="solution.taskName" placeholder="所属名称" />-->
<!--        </el-form-item>-->
        <el-form-item label="任务名称" prop="taskName">
          <select v-model="solution.taskName">
            <option v-for="x in taskList">{{x.task_name}}</option>
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
  </div>
</template>

<script>
import {
  getSolutionAll,
  createSolution,
  deleteSolution,
  updateSolution
} from '@/api/solution'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'
import {getTaskAll} from "@/api/task";
import {upHeaders, upUrl} from "@/api/file";

const defaultM = {
  id: '',
  solutionName: ''
}
export default {
  data() {
    return {
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      solution: {
        id: '',
        solutionName: '',
        taskName:'',
        codeAddr:'',
      },
      search: '',
      tableData: [],
      solutionList: [],
      taskList:[],
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
    getList() {
      this.listLoading = true
      getSolutionAll().then(response => {
        this.solutionList = response.data
        this.tableData = response.data
        this.listLoading = false
      })
      getTaskAll().then(response => {
        this.taskList = response.data
      })
    },
    resetFilter() {
      this.getList()
    },
    handleFilter() {       //搜索
      const newData = this.solutionList.filter(
        data =>
          !this.search ||
          data.solutionName.toLowerCase().includes(this.search.toLowerCase())
      )
      this.tableData = genTree(newData)
    },

    handleShow(scope) {
        this.dialogTableVisible = true

    },

    handleAdd() {
      this.solution = Object.assign({}, defaultM)
      this.dialogType = 'new'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {             //TODO
      this.solution = Object.assign({}, scope.row)
      this.dialogType = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleDelete(scope) {           //TODO
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
