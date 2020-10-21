<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入App名称进行搜索"
        style="width: 200px;"
        class="filter-item"
        @keyup.native="handleFilter"
      />
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
      <el-button type="primary" icon="el-icon-delete-solid" @click="handleDeleteLog">清除30天日志</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="tableData"
      stripe
      style="width: 100%;margin-top:10px;"
      border
    >
      <!-- <el-table-column align="center" label="Role Key" width="220">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>-->
      <el-table-column align="center" label="App名称" width="220">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column align="header-center" label="App描述">
        <template slot-scope="scope">{{ scope.row.description }}</template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEdit(scope)" />
          <el-button type="danger" size="small" icon="el-icon-delete" @click="handleDelete(scope)" />
          <el-button type="primary" size="small" icon="el-icon-d-arrow-right" @click="access(scope)" />
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑App':'新增App'">
      <el-form :model="role" label-width="80px" label-position="left">
        <el-form-item label="名称">
          <el-input v-model="app.name" placeholder="名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="app.description"
            :autosize="{ minRows: 2, maxRows: 4}"
            type="textarea"
            placeholder="描述"
          />
        </el-form-item>
        <el-form-item label="Url">
          <el-input v-model="app.url" placeholder="Url" />
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="confirmApp">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { genTree, deepClone } from '@/utils'
import {
  getAppAll,
  updateApp,
  createApp,
  deleteApp,
  deleteLog
} from '@/api/app'

const defaultApp = {
  id: '',
  name: '',
  description: '',
  url: ''
}

export default {
  data() {
    return {
      search: '',
      app: Object.assign({}, defaultApp),
      tableData: [],
      dialogVisible: false,
      dialogType: 'new',
      listLoading: true,
    }
  },
  computed: {},
  created() {
    this.getAppAll()
  },
  methods: {
    handleFilter() {
      const newData = this.appsList.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase())
      )
      this.tableData = genTree(newData)
    },
    async getAppAll() {
      this.listLoading = true
      const res = await getAppAll()
      this.tableData = res.data
      this.appsList = res.data
      this.listLoading = false
    },
    access(scope) {
      const app = deepClone(scope.row)
      window.open(app.url, "_blank");
    },
    handleAdd() {
      this.app = Object.assign({}, defaultApp)
      if (this.$refs.tree) {
        this.$refs.tree.setCheckedNodes([])
      }
      this.dialogType = 'new'
      this.dialogVisible = true
    },
    handleEdit(scope) {
      this.dialogType = 'edit'
      this.dialogVisible = true
      this.app = deepClone(scope.row)
    },
    handleDelete({ $index, row }) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
      .then(async() => {
        await deleteApp(row.id)
        this.tableData.splice($index, 1)
        this.$message({
          type: 'success',
          message: '成功删除!'
        })
      })
      .catch(err => {
        console.error(err)
      })
    },
    handleDeleteLog() {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
      .then(async() => {
        await deleteLog()
        this.$message({
          type: 'success',
          message: '删除任务提交成功!'
        })
      })
      .catch(err => {
        console.error(err)
      })
    },
    async confirmApp() {
      const isEdit = this.dialogType === 'edit'

      if (isEdit) {
        await updateApp(this.app.id, this.app)
        for (let index = 0; index < this.tableData.length; index++) {
          if (this.tableData[index].id === this.app.id) {
            this.tableData.splice(index, 1, Object.assign({}, this.app))
            break
          }
        }
      } else {
        await createApp(this.app)
        this.getAppAll()
      }

      const { description, name } = this.app
      this.dialogVisible = false
      this.$notify({
        title: '成功',
        dangerouslyUseHTMLString: true,
        message: `
            <div>App名称: ${name}</div>
            <div>App描述: ${description}</div>
          `,
        type: 'success'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  .roles-table {
    margin-top: 30px;
  }
  .permission-tree {
    margin-bottom: 30px;
  }
}
</style>
