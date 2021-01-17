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
        <el-table-column prop="create_by" label="用户名" :formatter="formatUser"></el-table-column>
        <el-table-column property="solutionName" label="方案名称"></el-table-column>
        <el-table-column prop="task_id" label="任务名称" :formatter="formatTask"></el-table-column>
        <el-table-column prop="dataset_id" label="数据集" :formatter="formatDataset"></el-table-column>
        <el-table-column prop="measurement_id" label="评价指标" :formatter="formatMeasurement"></el-table-column>
        <el-table-column property="solution_result" label="方案结果"></el-table-column>
        <el-table-column property="solution_status" :formatter="stateFormat" label="方案状态"></el-table-column>
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
        <el-form-item label="任务名称" prop="task_id">
          <el-select v-model="solution.task_id" @change="changeDatasetMeasurement(solution.task_id)" placeholder="请选择任务名称" style="width:100%">
            <el-option
              v-for="item in taskList"
              :key="item.id"
              :label="item.task_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据集" prop="dataset_id">
          <el-select v-model="solution.dataset_id" multiple placeholder="请选择数据集" style="width:100%">
            <el-option
              v-for="item in temp_list1"
              :key="item.dataset_id"
              :label="item.dataset_name"
              :value="item.dataset_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评价指标" prop="measurement_id">
          <el-select v-model="solution.measurement_id" multiple placeholder="请选择评价指标" style="width:100%">
            <el-option
              v-for="item in temp_list2"
              :key="item.measurement_id"
              :label="item.measurement_name"
              :value="item.measurement_id"
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
  createSolution,
  deleteSolution,
  updateSolution,
  getSolutionResultAll
} from '@/api/solution'
import { genTree } from '@/utils'
import checkPermission from '@/utils/permission'
import { getTaskAll, getDatasetMeasurementAll} from '@/api/task'
import { upHeaders, upUrl } from '@/api/file'
import Pagination from '@/components/Pagination'
import { getInfo, getUserAll } from '@/api/user'
import {getDatasetAll} from '@/api/dataset'
import {getMeasurementAll} from '@/api/measurement'

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
        task_id: '',
        dataset_id: '',
        measurement_id: ''
      },
      search: '',
      tableData: [],
      solutionList: { count: 0 },
      solutionShowList: [],
      listQuery: {
        page: 1,
        page_size: 20
      },
      taskList: [],
      user: [],
      datasetList: [],
      measurementList: [],
      s_r_list: [],
      t_d_m_list: [],
      temp_list1: [],
      temp_list2: [],
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
  stateFormat: {},
  created() {
    this.getTaskAll()
    this.getUserAll()
    this.getDatasetMeasurementAll()
    this.getDatasetAll()
    this.getMeasurementAll()
    this.getSolutionResultAll()
    this.getList()
  },
  methods: {
    checkPermission,
    UploadSuccess(res, file) {
      var str = res.data.name
      this.solution.solutionName = str.substr(0, str.length - 4)
    },
    beforeUpload(file) {
      const isZip = file.name.endsWith('.zip')
      if (!isZip) {
        this.$message.error('请选择zip文件！')
        return false
      } else return true
    },
    getTaskAll() {
      getTaskAll().then(response => {
        this.taskList = genTree(response.data.results)
      })
    },
    getDatasetAll() {
      getDatasetAll().then(response => {
        this.datasetList = genTree(response.data.results)
      })
    },
    getMeasurementAll() {
      getMeasurementAll().then(response => {
        this.measurementList = genTree(response.data)
      })
    },
    getUserAll() {
      getUserAll().then(response => {
        this.user = genTree(response.data.results)
      })
    },
    getDatasetMeasurementAll() {
      getDatasetMeasurementAll().then(response => {
        this.t_d_m_list = genTree(response.data.results);
      });
    },
    getSolutionResultAll() {
      getSolutionResultAll().then(response => {
        this.s_r_list = genTree(response.data.results)
      })
    },
    getList() {
      this.listLoading = true
      getSolutionList(this.listQuery).then(response => {
        if (response.data) {
          this.solutionList = response.data
        }
        for (var i = 0; i < this.solutionList.results.length; i++) {
          for (var j = 0; j < this.taskList.length; j++) {
            if (this.taskList[j].id == this.solutionList.results[i].task_id) {
              this.solutionList.results[i]['taskName'] = this.taskList[j].task_name
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
    handleShow(scope) {
      this.solutionShowList = this.s_r_list.filter(x => {
        return x.solution_id == scope.row.id
      })
      for (var i = 0; i < this.solutionShowList.length; i++) {
        this.solutionShowList[i]['solutionName'] = scope.row.solutionName
        this.solutionShowList[i]['task_id'] = scope.row.task_id
        this.solutionShowList[i]['create_by'] = scope.row.create_by
        this.solutionShowList[i]['solution_status'] = scope.row.solution_status
      }
      this.dialogTableVisible = true
    },
    handleAdd() {
      // getInfo().then(response => {
      //   this.solution.userId = response.data.id
      // })
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
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteSolution(scope.row.id)
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
    formatUser(row, column) {
      for (var i = 0; i < this.user.length; i++) {
        if (this.user[i].id == Number(row.create_by)) {
          return this.user[i].name
        }
      }
    },
    formatTask(row, column) {
      for (var i = 0; i < this.taskList.length; i++) {
        if (this.taskList[i].id == Number(row.task_id)) {
          return this.taskList[i].task_name
        }
      }
    },
    formatDataset(row) {
      for (var i = 0; i < this.datasetList.length; i++) {
        if (this.datasetList[i].id == Number(row.dataset_id)) {
          return this.datasetList[i].dataset_name
        }
      }
    },
    formatMeasurement(row) {
      for (var i = 0; i < this.measurementList.length; i++) {
        if (this.measurementList[i].id == Number(row.measurement_id)) {
          return this.measurementList[i].name
        }
      }
    },
    changeDatasetMeasurement(id) {
      this.temp_list1 = []
      this.temp_list2 = []
      this.temp_list1 = this.t_d_m_list.filter(function(x) {
        return x.task_id == id
      })
      this.temp_list2 = this.t_d_m_list.filter(function(x) {
        return x.task_id == id
      })
      for (var i = 0; i < this.temp_list1.length; ++i) {
        for (var j = 0; j < this.datasetList.length; ++j) {
          if (this.datasetList[j].id == this.temp_list1[i].dataset_id) {
            this.temp_list1[i]['dataset_name'] = this.datasetList[j].dataset_name
            break
          }
        }
      }
      for (var i = 0; i < this.temp_list1.length; ++i) {
        for (var j = i+1; j < this.temp_list1.length; ++j) {
          if (this.temp_list1[j].dataset_id == this.temp_list1[i].dataset_id) {
            this.temp_list1.splice(j, 1)
          }
        }
      }
      for (var i = 0; i < this.temp_list2.length; ++i) {
        for(var j = 0; j < this.measurementList.length; ++j) {
          if (this.measurementList[j].id == this.temp_list2[i].measurement_id) {
            this.temp_list2[i]['measurement_name'] = this.measurementList[j].name
            break
          }
        }
      }
      for (var i = 0; i < this.temp_list2.length; ++i) {
        for (var j = i + 1; j < this.temp_list2.length; ++j) {
          if (this.temp_list2[j].measurement_id == this.temp_list2[i].measurement_id) {
            this.temp_list2.splice(j, 1)
          }
        }
      }
    },
    async confirm(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          const isEdit = this.dialogType === 'edit'
          if (isEdit) {
            updateSolution(this.solution.solutionId, this.solution).then(() => {
              this.getList()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success'
              })
            })
          } else {
            createSolution(this.solution).then(res => {
              this.getList()
              this.$refs.upload.clearFiles()
              this.dialogFormVisible = false
              this.$message({
                message: '新增成功',
                type: 'success'
              })
            })
          }
        } else {
          return false
        }
      })
    },
    stateFormat(row, column) {
      return row.solution_status === 0 ? '未运行' : row.solution_status === 1 ? '运行中' : '运行完毕'
    }
  }
}
</script>
