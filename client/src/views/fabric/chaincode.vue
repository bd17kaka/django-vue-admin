<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入合约名称进行搜索"
        style="width: 200px;"
        class="filter-item"
        @keyup.native="handleFilter"
      />
    </div>
    <el-table
      v-loading="listLoading"
      :data="tableData"
      stripe
      style="width: 100%;margin-top:10px;"
      border
    >
      <el-table-column align="center" label="合约名称" width="220">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column align="center" label="合约路径" width="500">
        <template slot-scope="scope">{{ scope.row.path }}</template>
      </el-table-column>
      <el-table-column align="center" label="合约版本" width="220">
        <template slot-scope="scope">{{ scope.row.version }}</template>
      </el-table-column>
     
      <el-table-column align="center" label="操作">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { genTree, deepClone } from '@/utils'
import {
  getChaincodeAll,
} from '@/api/fabric'

export default {
  data() {
    return {
      search: '',
      tableData: [],
      dialogVisible: false,
      dialogType: 'new',
      listLoading: true,
    }
  },
  computed: {},
  created() {
    this.getChaincodeAll()
  },
  methods: {
    handleFilter() {
      const newData = this.chaincodeList.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase())
      )
      // this.tableData = genTree(newData)
      this.tableData = newData
    },
    async getChaincodeAll() {
      this.listLoading = true
      const res = await getChaincodeAll()
      this.tableData = res.data
      this.chaincodeList = res.data
      this.listLoading = false
    },
    viewData(scope) {
    },
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
