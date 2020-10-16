<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入任务名称进行搜索"
        style="width: 200px;"
        class="filter-item"
      />
      <el-button type="primary" icon="el-icon-search" @click="handleFilter" >搜索</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增任务</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="tableData"
      style="width: 100%;margin-top:10px;"
      border
      fit
      stripe
      highlight-current-row
      max-height="600"
      row-key="id"
    >
      <el-table-column type="index" width="50" />

      <el-table-column label="任务名称">
        <template slot-scope="scope">{{ scope.row.task_name }}</template>
      </el-table-column>

      <el-table-column label="任务类型">
        <template slot-scope="scope">{{ scope.row.task_type }}</template>
      </el-table-column>

      <el-table-column label="创建日期">
        <template slot-scope="scope">
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>

      <el-table-column label="任务描述">
        <template slot-scope="scope">
          <span>{{ scope.row.description }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button
            type="info"
            size="small"
            icon="el-icon-message"
            :disabled="!checkPermission(['task_query'])"
            @click="handleShow(scope)"
            title="查看详细信息"
          />
          <el-button
            type="primary"
            size="small"
            icon="el-icon-edit"
            :disabled="!checkPermission(['task_update'])"
            @click="handleEdit(scope)"
            title="修改"
          />
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            :disabled="!checkPermission(['task_delete'])"
            @click="handleDelete(scope)"
            title="删除"
          />
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogTableVisible" title="任务详细信息">
        <el-table :data="tableData.filter(data => !search || data.task_name.toLowerCase().includes(search.toLowerCase()))">
            <el-table-column property="task_name" label="任务名称" width="150"></el-table-column>
            <el-table-column property="task_type" label="任务类型" width="150"></el-table-column>
            <el-table-column property="create_time" label="创建日期" width="200"></el-table-column>
            <el-table-column property="update_time" label="修改日期" width="200"></el-table-column>
            <el-table-column property="matched_dataset" label="数据集" width="300"></el-table-column>
            <el-table-column property="description" label="任务描述" width="200"></el-table-column>
            <el-table-column property="task_status" label="任务状态" width="100"></el-table-column>
        </el-table>
    </el-dialog>

    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑岗位':'新增岗位'">
      <el-form
        ref="Form"
        :model="task"
        label-width="80px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="名称" prop="task_name">
          <el-input v-model="task.task_name" placeholder="名称" />
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
  getTaskAll,
  createTask,
  deleteTask,
  updateTask
} from '@/api/task'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'

const defaultM = {
  id: '',
  task_name: ''
}
export default {
  data() {
    return {
      task: {
        id: '',
        task_name: ''
      },
      search: '',
      tableData: [],
      taskList: [],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogType: 'new',
      rule1: {
        task_name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
      }
    }
  },
  computed: {},
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true
      getTaskAll().then(response => {
        this.taskList = response.data
        this.tableData = response.data
        this.listLoading = false
      })
    },
    resetFilter() {
      this.getList()
    },
    handleFilter() {       //搜索
      const newData = this.taskList.filter(
        data => !this.search || data.task_name.toLowerCase().includes(this.search.toLowerCase())
      )
      this.tableData = genTree(newData)
    },

    handleShow(scope) {
        //this.getList()
        //this.task = Object.assign({},scope.row)
        this.dialogTableVisible = true

    },

    handleAdd() {
      this.task = Object.assign({}, defaultM)
      this.dialogType = 'new'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {
      this.task = Object.assign({}, scope.row)
      this.dialogType = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleDelete(scope) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteTask(scope.row.id)
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
            updateTask(this.task.id, this.task).then(() => {
              this.getList()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
          } else {
            createTask(this.task).then(res => {
              // this.task = res.data
              // this.tableData.unshift(this.task)
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
