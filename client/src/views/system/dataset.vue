    <template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input v-model="listQuery.search" placeholder="请输入数据集名称"
        style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter"/>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-refresh-left" @click="resetFilter">刷新重置</el-button>

      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增数据集</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="datasetList.results"
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
        <template slot-scope="scope">
          <el-link
            type="primary"
            :href="downloadurl+'/media/dataset/dataset/'+scope.row.dataset_name+'.zip'"
            target="_blank">
            {{ scope.row.dataset_name }}
          </el-link>
        </template>
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

      <el-table-column align="center" label="操作" width="200">
        <template slot-scope="scope">
          <el-button
            type="info"
            size="small"
            icon="el-icon-view"
            :disabled="!checkPermission(['dataset_query'])"
            @click="handleShow(scope)"
            title="查看详细信息"
          />
          <el-button
            type="primary"
            size="small"
            icon="el-icon-edit"
            :disabled="!checkPermission(['dataset_update'])"
            @click="handleEdit(scope)"
            title="修改"
          />
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

    <el-dialog :visible.sync="dialogTableVisible" title="数据集详细信息" width="80%">
        <el-table :data="datasetshowList" border>
            <el-table-column property="dataset_name" label="数据集名称"></el-table-column>
            <el-table-column property="create_time" label="创建日期"></el-table-column>
            <el-table-column property="update_time" label="修改日期"></el-table-column>
            <el-table-column property="description" label="数据集描述"></el-table-column>
            <el-table-column property="addr" label="数据集地址"></el-table-column>
        </el-table>
    </el-dialog>

    <el-dialog :visible.sync="dialogFormVisible" :title="dialogType==='edit'?'编辑数据集':'新增数据集'">
      <el-form
        ref="Form"
        :model="dataset"
        label-width="100px"
        label-position="right"
        :rules="rule1"
      >
        <el-form-item label="上传数据集">
          <el-upload
            ref="upload"
            class="upload-demo"
            :action="upUrl"
            :before-upload="beforeUpload"
            :headers="upHeaders"
            :on-success="UploadSuccess"
          >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传zip文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item label="数据集名称" prop="dataset_name">
          <el-input v-model="dataset.dataset_name" :disabled="true" placeholder="数据集名称" />
        </el-form-item>
        <el-form-item label="数据集描述" prop="description">
          <el-input type="textarea" v-model="dataset.description" placeholder="请输入描述" maxlength="2000" show-word-limit/>
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

    <pagination
      v-show="datasetList.count>0"
      :total="datasetList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
  </div>
</template>

<script>
import {
  createDataset,
  deleteDataset,
  updateDataset
} from '@/api/dataset'
import { getDatasetList } from "@/api/dataset"
import { upUrl,upHeaders } from '@/api/file'
import { genTree, deepClone } from '@/utils'
import Pagination from "@/components/Pagination"
import checkPermission from '@/utils/permission'

const defaultM = {
  id: '',
  dataset_name: ''
}
export default {
  components: { Pagination },
  data() {
    return {
      dataset: {
        id: '',
        dataset_name: ''
      },
      search: '',
      tableData: [],
      datasetshowList: [{
        id: '',
        dataset_name: '',
        create_time: '',
        update_time: '',
        description: '',
        addr: ''
      }],
      downloadurl: process.env.VUE_APP_BASE_API,
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      datasetList: {count:0},
      listQuery: {
        page: 1,
        page_size: 20
      },
      listLoading: true,
      dialogTableVisible: false,
      dialogFormVisible: false,
      dialogType: 'new',
      rule1: {
        dataset_name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
      }
    }
  },
  computed: {},
  created() {
    this.getList();
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true;
      getDatasetList(this.listQuery).then(response => {
        if (response.data) {
          this.datasetList = response.data
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

    UploadSuccess(res,file) {
      var str=res.data.name;
      this.dataset.dataset_name=str.substr(0,str.length -4);
    },
    beforeUpload(file) {                //返回fasle停止上传,检查压缩包名称和格式
      const isZip = file.name.endsWith('.zip');
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
    handleShow(scope) {
      this.datasetshowList[0].id = scope.row.id
      this.datasetshowList[0].dataset_name = scope.row.dataset_name
      this.datasetshowList[0].create_time = scope.row.create_time
      this.datasetshowList[0].update_time = scope.row.update_time
      this.datasetshowList[0].description = scope.row.description
      this.datasetshowList[0].addr = scope.row.addr
      this.dialogTableVisible = true
    },
    handleEdit(scope) {
      this.dataset = Object.assign({}, scope.row)
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
              this.$refs.upload.clearFiles()
              this.dialogFormVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success',
              })
            })
            this.$refs.upload.clearFiles()
          } else {
            this.dataset.addr = '/media/' + this.dataset.dataset_name
            createDataset(this.dataset).then(res => {
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
