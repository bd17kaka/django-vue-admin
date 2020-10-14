<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入数据集名称进行搜索"
        style="width: 200px;"
        class=""     
      />
      <el-button type="primary" icon="el-icon-search" @click="handleFilter" >搜索</el-button>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增数据集</el-button>
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

      <el-table-column label="数据集名称" width="150">
        <template slot-scope="scope">{{ scope.row.dataset_name }}</template>
      </el-table-column>
      <el-table-column label="创建日期">
        <template slot-scope="scope">
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="数据集描述">
        <template slot-scope="scope">
          <span>{{ scope.row.description }}</span>
        </template>
      </el-table-column>
      <el-table-column label="数据集地址">
        <template slot-scope="scope">
          <span>{{ scope.row.addr }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="操作" width="150">
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="small"
            icon="el-icon-delete"
            :disabled="!checkPermission(['dataset_delete'])"
            @click="handleDelete(scope)"
            title="删除"
          />
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogFormVisible" title="新增数据集">
      <el-form
        ref="Form"
        :model="dataset"
        label-width="100px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="数据集名称" prop="dataset_name">
          <el-input v-model="dataset.dataset_name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="数据集描述" prop="description">
          <el-input type="textarea" v-model="dataset.description" placeholder="请输入描述" maxlength="2000" show-word-limit/>
        </el-form-item>
        <el-form-item label="上传数据集">
          <el-upload 
            class="upload-demo"
            :action="upUrl"
            :before-upload="beforeUpload"
            :headers="upHeaders"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传zip文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="数据集地址" prop="addr">
          <el-input v-model="dataset.dataset_name" :disabled="true" placeholder="数据集地址">
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
  getDatasetAll,
  createDataset,
  deleteDataset,
  updateDataset
} from '@/api/dataset'
import { upUrl,upHeaders } from '@/api/file'
import { genTree, deepClone } from '@/utils'
import checkPermission from '@/utils/permission'

const defaultM = {
  id: '',
  dataset_name: ''
}
export default {
  data() {
    return {
      dataset: {
        id: '',
        dataset_name: ''
      },
      search: '',
      tableData: [],
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      datasetList: [],
      listLoading: true,
      dialogFormVisible: false,
      dialogType: 'new',
      rule1: {
        dataset_name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
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
      getDatasetAll().then(response => {  
        this.datasetList = response.data
        this.tableData = response.data
        this.listLoading = false
      })
    },
    resetFilter() {
      this.getList()
    },
    handleFilter() {       //搜索
      const newData = this.datasetList.filter(
        data => !this.search || data.dataset_name.toLowerCase().includes(this.search.toLowerCase())
      )
      this.tableData = genTree(newData)
    },

    beforeUpload(file) {                //返回fasle停止上传,检查压缩包名称和格式
      const isZip = file.name.endsWith('.zip');
      if(file.name != this.dataset.dataset_name+'.zip'){
        this.$message.error('文件名称与数据集名不匹配');
        return false;
      }
      if(!isZip){
        this.$message.error('请选择zip文件！');
        return false;
      }
      else return true;
    },
    handleAdd() {              
      this.dataset = Object.assign({}, defaultM)
      this.dialogType = 'new'
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
          await deleteDataset(scope.row.id)
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
            updateDataset(this.dataset.id, this.dataset).then(() => {
              this.getList()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
          } else {
            this.dataset.addr = '/media/' + this.dataset.dataset_name
            createDataset(this.dataset).then(res => {
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
