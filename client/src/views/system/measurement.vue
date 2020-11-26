<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入评价指标名称进行搜索"
        style="width: 200px;"
        class="filter-item"
        @keyup.native="handleFilter"
      />
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增评价指标</el-button>
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

      <el-table-column label="评价指标名称" width="150">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column label="创建日期">
        <template slot-scope="scope">
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="评价指标描述">
        <template slot-scope="scope">
          <span>{{ scope.row.description }}</span>
        </template>
      </el-table-column>
      <el-table-column label="评价指标地址">
        <template slot-scope="scope">
          <span>{{ scope.row.addr }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="150">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            icon="el-icon-edit"
            :disabled="!checkPermission(['measurement_update'])"
            @click="handleEdit(scope)"
          />
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            :disabled="!checkPermission(['measurement_delete'])"
            @click="handleDelete(scope)"
            title="删除"
          />
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogTableVisible" title="修改评价指标">
      <el-form
        ref="Table"
        :model="measurement"
        label-width="100px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="评价指标名称" prop="name">
          <el-input v-model="measurement.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="评价指标描述" prop="description">
          <el-input type="textarea" v-model="measurement.description" placeholder="请输入描述" maxlength="500" show-word-limit/>
        </el-form-item>
        <el-form-item label="上传评价指标">
          <el-upload
            ref="upload"
            class="upload-demo"
            :action="upUrl"
            :before-upload="beforeUpload"
            :headers="upHeaders"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传py文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="评价指标地址" prop="">
          <el-input v-model="measurement.name" :disabled="true" placeholder="评价指标地址">
            <template slot="prepend">/media/</template>
          </el-input>
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogTableVisible=false">取消</el-button>
        <el-button type="primary" @click="confirm('Table')">确认</el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="dialogFormVisible" title="新增评价指标">
      <el-form
        ref="Form"
        :model="measurement"
        label-width="100px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="评价指标名称" prop="name">
          <el-input v-model="measurement.name" :disabled="true" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="评价指标描述" prop="description">
          <el-input type="textarea" v-model="measurement.description" placeholder="请输入描述" maxlength="500" show-word-limit/>
        </el-form-item>
        <el-form-item label="上传评价指标">
          <el-upload
            ref="upload"
            class="upload-demo"
            :action="upUrl"
            :before-upload="beforeUpload"
            :headers="upHeaders"
            :on-success="UploadSuccess"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传py文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="评价指标地址" prop="">
          <el-input v-model="measurement.name" :disabled="true" placeholder="评价指标地址">
            <template slot="prepend">/media/</template>
          </el-input>
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
  getMeasurementAll,
  createMeasurement,
  deleteMeasurement,
  // deleteMeasurementFile,
  updateMeasurement
} from '@/api/measurement'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'
import {getTaskAll} from '@/api/task';
import {upHeaders, upUrl} from '@/api/file';

const defaultM = {
  id: '',
  name: ''
}
export default {
  data() {
    return {
      measurement: {
        id: '',
        name: ''
      },
      search: '',
      tableData: [],
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      measurementList: [],
      listLoading: true,
      dialogFormVisible: false,
      dialogTableVisible: false,
      dialogType: 'new',
      rule1: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
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
      getMeasurementAll().then(response => {
        this.measurementList = response.data
        this.tableData = response.data
        this.listLoading = false
      })
    },
    resetFilter() {
      this.getList()
    },
    handleFilter() {
      const newData = this.measurementList.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase())
      )
      this.tableData = genTree(newData)
    },
    handleAdd() {
      this.measurement = Object.assign({}, defaultM)
      this.dialogType = 'new'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {
      this.measurement = Object.assign({}, scope.row) // copy obj
      this.dialogType = 'edit'
      this.dialogTableVisible = true
      this.$nextTick(() => {
        this.$refs['Table'].clearValidate()
      })
    },
    handleDelete(scope) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteMeasurement(scope.row.id)
          // await deleteMeasurementFile(scope.row.id)
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
    beforeUpload(file) {
      const isPy = file.name.endsWith('.py');
      // if(file.name != this.measurement.name+'.py'){
      //   this.$message.error('文件名称与评价指标名不匹配');
      //   return false;
      // }
      if(!isPy){
        this.$message.error('请选择py文件！');
        return false;
      }
      else return true;
    },
    UploadSuccess(res,file) {
      var str=res.data.name;
      this.measurement.name=str.substr(0,str.length -3);
    },
    async confirm(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          const isEdit = this.dialogType === 'edit'
          if (isEdit) {
            updateMeasurement(this.measurement.id, this.measurement).then(() => {
              this.getList()
              this.$refs.upload.clearFiles()
              this.dialogTableVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
            this.$refs.upload.clearFiles()
          } else {
            this.measurement.addr = '/media/' + this.measurement.name
            createMeasurement(this.measurement).then(res => {
              // this.measurement = res.data
              // this.tableData.unshift(this.measurement)
              this.getList()
              this.$refs.upload.clearFiles();
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
