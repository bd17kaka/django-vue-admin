<template>
  <div class="app-container">
    <div style="margin-top:10px">
      <el-input
        v-model="search"
        placeholder="输入Channel名称进行搜索"
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
      <el-table-column align="center" label="Channel名称" width="220">
        <template slot-scope="scope">{{ scope.row.channel_id }}</template>
      </el-table-column>
      <el-table-column align="center" label="区块高度" width="220">
        <template slot-scope="scope">{{ scope.row.height }}</template>
      </el-table-column>
      <el-table-column align="center" label="当前区块哈希" width="500">
        <template slot-scope="scope">{{ scope.row.currentBlockHash }}</template>
      </el-table-column>
     
      <el-table-column align="center" label="操作">
        <template slot-scope="scope">
          <el-button type="primary" size="small" icon="el-icon-d-arrow-right" @click="viewData(scope)" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { genTree, deepClone } from '@/utils'
import {
  getChannelAll,
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
    this.getChannelAll()
  },
  methods: {
    handleFilter() {
      const newData = this.channelList.filter(
        data =>
          !this.search ||
          data.channel_id.toLowerCase().includes(this.search.toLowerCase())
      )
      // this.tableData = genTree(newData)
      this.tableData = newData
    },
    async getChannelAll() {
      this.listLoading = true
      const res = await getChannelAll()
      this.tableData = res.data
      this.channelList = res.data
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
