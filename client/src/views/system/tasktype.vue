<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入任务类型名称进行搜索"
        style="width: 200px;"
        class="filter-item"
        @keyup.native="handleFilter"
      />
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增任务类型</el-button>
    </div>

  <el-table
      v-loading="listLoading"
      :data="tasktypeList.results"
      style="width: 100%;margin-top:10px;"
      border
      fit
      stripe
      highlight-current-row
      max-height="600"
      row-key="id"
    >
      <el-table-column type="index" width="50" />
       <el-table-column prop="tasktype_name" label="任务类型名称" align="center" min-width="120"></el-table-column>
       <el-table-column prop="tasktype_description" label="任务类型描述" align="center" min-width="100"></el-table-column>
       <el-table-column prop="create_time" label="创建时间" align="center" min-width="120"></el-table-column>
       <el-table-column prop="update_time" label="修改时间" align="center" min-width="100"></el-table-column>
       <el-table-column label="操作" align="center" min-width="100">
         <template slot-scope="scope">
          <el-button
          type="info"
          size="small"
          icon="el-icon-view"
          title="查看详细信息"
          :disabled="!checkPermission(['tasktype_query'])"
          @click="checkDetail(scope.row)" />
          <el-button
          type="primary"
          size="small"
          icon="el-icon-edit"
          title="编辑"
          :disabled="!checkPermission(['tasktype_update'])"
          @click="handleEdit(scope)" />
          <el-button
          type="danger"
          size="small"
          icon="el-icon-delete"
          title="删除"
          :disabled="!checkPermission(['tasktype_delete'])"
          @click="handleDelete(scope)" />
         </template>
       </el-table-column>
  </el-table>

  <!--
    查看详情-对话框
    -->
  <el-dialog :visible.sync="dialogTableVisible" title="任务类型详细信息" width="80%">
        <el-table :data="present_row">
            <el-table-column property="tasktype_name" label="任务类型名称"></el-table-column>
            <el-table-column property="tasktype_description" label="任务类型描述"></el-table-column>
            <el-table-column property="create_time" label="创建时间"></el-table-column>
            <el-table-column property="update_time" label="修改时间"></el-table-column>
        </el-table>
  </el-dialog>

  <!--
    新建任务类型-对话框
    -->
    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑岗位':'新建任务类型'">
      <el-form
        ref="Form"
        :model="tasktype"
        label-width="120px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="任务类型名称" prop="tasktype_name">
          <el-input v-model="tasktype.tasktype_name" placeholder="任务类型名称" />
        </el-form-item>
        <el-form-item label="任务类型描述" prop="tasktype_description">
          <el-input v-model="tasktype.tasktype_description" placeholder="任务类型描述" />
        </el-form-item>
        </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogFormVisible=false">取消</el-button>
        <el-button type="primary" @click="confirm('Form')">确认</el-button>
      </div>
    </el-dialog>
    <pagination
      v-show="tasktypeList.count>0"
      :total="tasktypeList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
  </div>
</template>

<script>
import {
  getTasktypeAll,
  createTasktype,
  deleteTasktype,
  updateTasktype,
  getTasktypeList,
} from '@/api/tasktype'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'
import Pagination from "@/components/Pagination"

const defaultM = {
  id: '',
  tasktype: ''
}
export default {
  components: { Pagination },
  data() {
    return {
      tasktype: {
        id: '',
        tasktype_name: ''
      },
      search: '',
      tableData: [],
      tasktypeList: {count:0},
      listQuery: {
        page: 1,
        page_size: 20
      },
      present_row: [{
        tasktype_name: "",
        tasktype_description: "",
        create_time: "",
        update_time: "",
        id:"",
        is_deleted:""
      }],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogType: 'new',
      rule1: {
        tasktype_name: [{ required: true, message: '请输入任务类型名称', trigger: 'blur' }]
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
      this.listLoading = true;
      getTasktypeList(this.listQuery).then(response => {
        if (response.data) {
          this.tasktypeList = response.data
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

    checkDetail(row){        //查看详情
      this.present_row[0].tasktype_name = row.tasktype_name;
      this.present_row[0].tasktype_description = row.tasktype_description;
      this.present_row[0].create_time = row.create_time;
      this.present_row[0].update_time = row.update_time;
      this.present_row[0].id = row.id;
      this.dialogTableVisible = true;
    },

    handleAdd() {                    //新增
      this.tasktype = Object.assign({}, defaultM)
      this.dialogType = 'new'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {             //编辑
      this.tasktype = Object.assign({}, scope.row)
      this.dialogType = 'edit'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleDelete(scope) {           //删除
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteTasktype(scope.row.id)
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
    async confirm(form) {               //编辑校验
      this.$refs[form].validate(valid => {
        if (valid) {
          const isEdit = this.dialogType === 'edit'
          if (isEdit) {
            updateTasktype(this.tasktype.id, this.tasktype).then(() => {
              this.getList()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
          } else {
            createTasktype(this.tasktype).then(res => {
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
