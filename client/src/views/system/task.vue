<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input v-model="listQuery.search" placeholder="请输入任务名称进行搜索"
        style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-refresh-left" @click="resetFilter">刷新重置</el-button>
      <el-button type="primary" icon="el-icon-plus" :disabled="!checkPermission(['task_create'])" @click="handleAdd">新增任务</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="taskList.results"
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
            icon="el-icon-view"
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

    <el-dialog :visible.sync="dialogTableVisible" title="任务详细信息" width="80%">
        <el-table :data="taskshowList" border>
            <el-table-column property="task_name" label="任务名称" width="120"></el-table-column>
            <el-table-column property="task_type" label="任务类型" width="120"></el-table-column>
            <el-table-column property="create_time" label="创建日期" width="180"></el-table-column>
            <el-table-column property="update_time" label="修改日期" width="180"></el-table-column>
            <el-table-column property="matched_dataset" label="数据集" width="120"></el-table-column>
            <el-table-column property="task_measurement" label="评价指标" width="120"></el-table-column>
            <el-table-column property="description" label="任务描述" width="200"></el-table-column>
            <el-table-column property="task_status" label="任务状态" width="130"></el-table-column>
        </el-table>
    </el-dialog>

    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑任务':'新增任务'">
      <el-form
        ref="Form"
        :model="task"
        label-width="80px"
        label-position="right"
        :rules="rule1"
      >
            <el-form-item label="任务名称" prop="task_name">
          <el-input v-model="task.task_name" placeholder="任务名称" />
        </el-form-item>
        <el-form-item label="任务类型" prop="task_type">
          <el-select v-model="task.task_type" placeholder="请选择任务类型" style="width:100%">
           <el-option
            v-for="item in tasktype"
             :key="item.id"
             :label="item.label"
             :value="item.tasktype_name"
           />
          </el-select>
        </el-form-item>
        <el-form-item label="数据集" prop="matched_dataset">
          <el-select v-model ="task.matched_dataset" placeholder="请选择数据集" style = "width:100%">
            <el-option
            v-for="item in dataset"
            :key="item.id"
            :label="item.label"
            :value="item.dataset_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评价指标" prop="task_measurement">
          <el-select v-model ="task.task_measurement" multiple placeholder="请选择评价指标" style = "width:100%">
            <el-option
            v-for="item in measurement"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input type = "textarea" autosize v-model="task.description" placeholder="任务描述" />
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogFormVisible=false">取消</el-button>
        <el-button type="primary" @click="confirm('Form')">确认</el-button>
      </div>
    </el-dialog>
    <pagination
      v-show="taskList.count>0"
      :total="taskList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
  </div>
</template>

<script>
import { getTasktypeAll } from "@/api/tasktype"
import { getDatasetAll } from "@/api/dataset"
import {getMeasurementAll} from"@/api/measurement"
import {
  getTaskList,
  getTaskAll,
  createTask,
  deleteTask,
  updateTask
} from '@/api/task'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'
import Pagination from "@/components/Pagination"

const defaultM = {
  id: '',
  task_name: ''
}
export default {
  components: { Pagination },
  data() {
    return {
      task: {
        id: '',
        task_name: ''
      },
      search: '',
      tableData: [],
      taskList:  {count:0},
      listQuery: {
        page: 1,
        page_size: 20
      },
      tasktype: [],
      dataset: [],
      measurement: [],
      taskshowList: [{
        id: '',
        task_name: '',
        task_type: '',
        create_time: '',
        update_time: '',
        matched_dataset: '',
        task_measurement: '',
        description: '',
        task_status: ''
      }],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogType: 'new',
      rule1: {
        task_name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        task_type: [{ required: true, message: '请选择任务类型', trigger: 'blur' }],
        matched_dataset: [{ required: true, message: '请选择数据集', trigger: 'blur' }],
        task_measurement: [{ required: true, message: '请选择评价指标', trigger: 'blur' }],
      },
    }
  },
  computed: {},
  created() {
    this.getList();
    this.getTasktypeAll()
    this.getDatasetAll()
    this.getMeasurementAll()
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true;
      getTaskList(this.listQuery).then(response => {
        if (response.data) {
          this.taskList = response.data        }
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
    getTasktypeAll() {
      getTasktypeAll().then(response => {
        this.tasktype = genTree(response.data.results);
      });
    },
    getDatasetAll() {
      getDatasetAll().then(response => {
        this.dataset = genTree(response.data.results);
      });
    },
    getMeasurementAll() {
      getMeasurementAll().then(response => {
        this.measurement = genTree(response.data);
      });
    },
    handleShow(scope) {
      this.taskshowList[0].id = scope.row.id
      this.taskshowList[0].task_name = scope.row.task_name
      this.taskshowList[0].task_type = scope.row.task_type
      this.taskshowList[0].create_time = scope.row.create_time
      this.taskshowList[0].update_time = scope.row.update_time
      this.taskshowList[0].matched_dataset = scope.row.matched_dataset
      this.taskshowList[0].description = scope.row.description
      this.taskshowList[0].task_status = scope.row.task_status
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
              console.log(this.task)
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
