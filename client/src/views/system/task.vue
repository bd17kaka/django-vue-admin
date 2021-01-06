<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input v-model="listQuery.search" placeholder="请输入任务名称进行搜索" style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-refresh-left" @click="resetFilter">刷新重置</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增任务</el-button>
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
        <template slot-scope="scope">{{ scope.row.tasktype_name }}</template>
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
            title="查看任务详细信息"
          />
          <el-button
            type="info"
            size="small"
            icon="el-icon-document"
            :disabled="!checkPermission(['task_query'])"
            @click="handleShowSolution(scope)"
            title="查看该任务下所有方案"
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
          <a :href="downloadurl + '/system/download/' + scope.row.task_name" target="_blank">
            <el-button
              type="success"
              size="small"
              icon="el-icon-download"
              title="批量下载此任务下所有方案"
              style="margin-left: 10px;"
            />
          </a>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogTableVisible" title="任务详细信息" width="80%">
      <el-table :data="taskShowList" border>
        <el-table-column property="task_name" label="任务名称"></el-table-column>
        <el-table-column prop="task_type_id" label="任务类型" :formatter="formatTasktype"></el-table-column>
        <el-table-column property="create_time" label="创建日期"></el-table-column>
        <el-table-column property="update_time" label="修改日期"></el-table-column>
        <el-table-column prop="dataset_id" :formatter="formatDataset" label="数据集"></el-table-column>
        <el-table-column prop="measurement_id" :formatter="formatMeasurement" label="评价指标"></el-table-column>
        <el-table-column property="description" label="任务描述"></el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog :visible.sync="dialogTableAllVisible" title="方案信息" width="80%">
      <el-table :data="solutionAllShowList" border>
        <el-table-column property="create_by" :formatter="formatUser" label="用户名"></el-table-column>
        <el-table-column property="solution_name" label="方案名称"></el-table-column>
        <el-table-column prop="dataset_id" :formatter="formatDataset" label="数据集"></el-table-column>
        <el-table-column prop="measurement_id" :formatter="formatMeasurement" label="评价指标"></el-table-column>
        <el-table-column property="solution_status" label="方案状态"></el-table-column>
        <el-table-column property="solution_result" label="方案结果"></el-table-column>
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
        <el-form-item label="任务类型" prop="task_type_id">
          <el-select v-model="task.task_type_id"  @change="changeMeasurement(task.task_type_id)" placeholder="请选择任务类型" style="width:100%">
            <el-option
              v-for="item in tasktype"
              :key="item.id"
              :label="item.tasktype_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据集" prop="matched_dataset">
          <el-select v-model ="task.matched_dataset" multiple placeholder="请选择数据集" style = "width:100%">
            <el-option
              v-for="item in dataset"
              :key="item.id"
              :label="item.dataset_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评价指标" prop="task_measurement">
          <el-select v-model ="task.task_measurement" multiple placeholder="请选择评价指标" style = "width:100%">
            <el-option
              v-for="item in temp_list"
              :key="item.value"
              :label="item.measurement_name"
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
import { getTasktypeAll } from '@/api/tasktype'
import { getDatasetAll } from '@/api/dataset'
import { getMeasurementAll } from '@/api/measurement'
import { getSolutionAll, getSolutionResultAll } from '@/api/solution'
import { getUserAll } from '@/api/user'
import {
  getTaskList,
  createTask,
  deleteTask,
  updateTask,
  getTasktypeMeasurementAll,
  getDatasetMeasurementAll
} from '@/api/task'
import { genTree } from '@/utils'
import checkPermission from '@/utils/permission'
import Pagination from '@/components/Pagination'

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
      downloadurl: process.env.VUE_APP_BASE_API,
      taskList: { count: 0 },
      listQuery: {
        page: 1,
        page_size: 20
      },
      tasktype: [],
      dataset: [],
      t_m_list: [],
      s_r_list: [],
      d_m_list: [],
      temp_list: [],
      user: [],
      solution: [],
      measurement: [],
      solutionAllShowList: [],
      s_temp_list: [],
      taskShowList: [],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogTableAllVisible: false,
      dialogType: 'new',
      rule1: {
        task_name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        task_type_id: [{ required: true, message: '请选择任务类型', trigger: 'blur' }],
        matched_dataset: [{ required: true, message: '请选择数据集', trigger: 'blur' }],
        task_measurement: [{ required: true, message: '请选择评价指标', trigger: 'blur' }],
      },
    }
  },
  computed: {},
  formatterTasktype: {},
  created() {
    this.getTasktypeAll()
    this.getDatasetAll()
    this.getMeasurementAll()
    this.getSolutionAll()
    this.getUserAll()
    this.getTasktypeMeasurementAll()
    this.getSolutionResultAll()
    this.getDatasetMeasurementAll()
  },
  mounted() {
    this.getList()
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true;
      getTaskList(this.listQuery).then(response => {
        if (response.data) {
          this.taskList = response.data
        }
        for (var i = 0; i < this.taskList.results.length; i++) {
          for (var j = 0; j < this.tasktype.length; j++) {
            if (this.tasktype[j].id == this.taskList.results[i].task_type_id) {
              this.taskList.results[i]['tasktype_name'] = this.tasktype[j].tasktype_name
              break
            }
          }
        }
        this.listLoading = false
      })
    },
    resetFilter() {
      this.listQuery = {
        page: 1,
        page_size: 20
      }
      this.getList()
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    getTasktypeAll() {
      getTasktypeAll().then(response => {
        this.tasktype = genTree(response.data.results)
      })
    },
    getDatasetAll() {
      getDatasetAll().then(response => {
        this.dataset = genTree(response.data.results)
      })
    },
    getSolutionAll() {
      getSolutionAll().then(response => {
        this.solution = response.data.results
      })
    },
    getUserAll() {
      getUserAll().then(response => {
        this.user = genTree(response.data.results)
      })
    },
    getMeasurementAll() {
      getMeasurementAll().then(response => {
        this.measurement = genTree(response.data)
      })
    },
    getTasktypeMeasurementAll() {
      getTasktypeMeasurementAll().then(response => {
        this.t_m_list = genTree(response.data.results)
      })
    },
    getSolutionResultAll() {
      getSolutionResultAll().then(response => {
        this.s_r_list = genTree(response.data.results)
      })
    },
    getDatasetMeasurementAll() {
      getDatasetMeasurementAll().then(response => {
        this.d_m_list = genTree(response.data.results)
      })
    },
    handleShow(scope) {
      this.taskShowList = this.d_m_list.filter(x => {
        return x.task_id == scope.row.id
      })
      for (var i = 0; i < this.taskShowList.length; i++) {
        this.taskShowList[i]['task_name'] = scope.row.task_name
        this.taskShowList[i]['task_type_id'] = scope.row.task_type_id
        this.taskShowList[i]['description'] = scope.row.description
      }
      this.dialogTableVisible = true
    },
    handleShowSolution(scope) {
      this.solutionAllShowList = []
      for (var i = 0; i < this.solution.length; i++) {
        this.s_temp_list = []
        if (this.solution[i].task_id == scope.row.id) {
          this.s_temp_list = this.s_r_list.filter(x => {
            return x.solution_id == this.solution[i].id
          })
          for (var j = 0; j < this.s_temp_list.length; j++) {
            this.s_temp_list[j]['create_by'] = this.solution[i].create_by
            this.s_temp_list[j]['solution_name'] = this.solution[i].solutionName
            this.s_temp_list[j]['solution_status'] = this.solution[i].solution_status
          }
          this.solutionAllShowList = this.solutionAllShowList.concat(this.s_temp_list)
        }
      }
      this.dialogTableAllVisible = true
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
      var list = this.solution.filter(function (x) {
          return x.task_id == scope.row.id
      })
      if(list.length!=0){
        this.$alert('该任务下已有方案，无法更改', '警告！！', {
        confirmButtonText: '确定',
        });

      }
      else{
          this.task = Object.assign({}, scope.row)
          this.dialogType = 'edit'
          this.dialogFormVisible = true
          this.$nextTick(() => {
            this.$refs['Form'].clearValidate()
          })
      }

    },
    handleDelete(scope) {
      var list = this.solution.filter(function (x) {
          return x.task_id == scope.row.id
      })
      if(list.length!=0){
        this.$alert('该任务下已有方案，无法更改', '警告！！', {
        confirmButtonText: '确定',
        });

      }
      else{
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
      }
    },
    changeMeasurement(id){
      this.temp_list = this.t_m_list.filter(function (x) {
          return x.task_type_id == id
        })
      for (var i = 0; i < this.temp_list.length; ++i) {
        for(var j = 0; j < this.measurement.length; ++j) {
          if (this.measurement[j].id == this.temp_list[i].measurement_id) {
            this.temp_list[i]["measurement_name"] = this.measurement[j].name;
            break;
          }
        }
      }
    },
    formatTasktype(row,column){
      for (var i = 0; i < this.tasktype.length; i++) {
        if (this.tasktype[i].id == Number(row.task_type_id)) {
          return this.tasktype[i].tasktype_name;
        }
      }
    },
    formatUser(row, column) {
      for (var i = 0; i < this.user.length; i++) {
        if (this.user[i].id == Number(row.create_by)) {
          return this.user[i].name
        }
      }
    },
    formatDataset(row) {
      for (var i = 0; i < this.dataset.length; i++) {
        if (this.dataset[i].id == Number(row.dataset_id)) {
          return this.dataset[i].dataset_name
        }
      }
    },
    formatMeasurement(row) {
      for (var i = 0; i < this.measurement.length; i++) {
        if (this.measurement[i].id == Number(row.measurement_id)) {
          return this.measurement[i].name
        }
      }
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
              // console.log(this.task)
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
