<template>
  <div class="dashboard-container">
    <div style="text-align:center;">
      <table frame=void align="center" style="font-size: 30px;text-align: center;width: 60%">
        <tr><th>用户总数</th><th>任务总数</th><th>方案总数</th><th>正在运行的方案数</th></tr>
        <tr><td>{{ user }}</td><td>{{ task }}</td><td>{{ solution }}</td><td>{{ solutionRunning }}</td></tr>
        <tr><th>CPU占用</th><th>内存占用</th><th>磁盘占用</th><th>GPU占用</th></tr>
        <tr><td>{{ cpu }}%</td><td>{{ memory }}MB</td><td>{{ disk }}MB</td><td>{{ gpu }}%</td></tr>
      </table>
    </div>
    <br>
    <br>
    <!--    <div class="dashboard-text">姓名: {{ name }}</div>-->
    <!--    <div class="dashboard-text">perms: <span v-for="perm in perms" :key="perm">{{ perm }}</span></div>-->
    <div class="user" style="text-align:center;margin:0 auto;">
      <div id="graph1" style="width: 700px; height: 400px; text-align:center;margin:0 auto;"></div>
    </div>
    <br>
    <div class="task" style="text-align:center;margin:0 auto;">
      <div id="graph2" style="width: 700px; height: 400px; text-align:center;margin:0 auto;"></div>
    </div>
    <br>
    <div class="solution" style="text-align:center;margin:0 auto;">
      <div id="graph3" style="width: 700px; height: 400px; text-align:center;margin:0 auto;"></div>
    </div>
    <br>
    <div class="solutionAll" style="text-align:center;margin:0 auto;">
      <div id="graph4" style="width: 700px; height: 400px; text-align:center;margin:0 auto;"></div>
    </div>
    <br>
    <div class="solutionCount" style="text-align:center;margin:0 auto;">
      <div id="graph5" style="width: 700px; height: 400px; text-align:center;margin:0 auto;"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      user: 78,
      task: 20,
      solution: 178,
      solutionRunning: 30,
      cpu: 60,
      memory: 512,
      disk: 1024,
      gpu: 50
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'perms'
    ])
  },
  created() {
    this.userEcharts()
    this.taskEcharts()
    this.solutionEcharts()
    this.solutionAllEcharts()
    this.solutionCountEcharts()
  },
  methods: {
    userEcharts() {
      let newPromise = new Promise((resolve) => {
        resolve()
      })
      newPromise.then(() => {
        // var axisData = []
        // for( var i=0;i<this.trace_list1.length;i++) {
        //   var size = this.trace_list1[i].size
        //   var time = this.trace_list1[i].time
        //   var newArr = [size, time]
        //   axisData.push(newArr)
        // }
        var myChart = this.$echarts.init(document.getElementById('graph1'))
        var option = {
          title: {
            text: '用户详情'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['新增用户', '活跃用户']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '新增用户',
              type: 'line',
              stack: '总量',
              data: [120, 132, 101, 134, 90, 230, 210]
            },
            {
              name: '活跃用户',
              type: 'line',
              stack: '总量',
              data: [220, 182, 191, 234, 290, 330, 310]
            }
          ]
        }
        myChart.setOption(option)
      })
    },
    taskEcharts() {
      let newPromise = new Promise((resolve) => {
        resolve()
      })
      newPromise.then(() => {
        var myChart = this.$echarts.init(document.getElementById('graph2'))
        var option = {
          title: {
            text: '任务相关'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          legend: {},
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
              axisTick: {
                alignWithLabel: true
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '新增任务数',
              type: 'bar',
              barWidth: '60%',
              data: [10, 52, 200, 334, 390, 330, 220]
            }
          ]
        }
        myChart.setOption(option)
      })
    },
    solutionEcharts() {
      let newPromise = new Promise((resolve) => {
        resolve()
      })
      newPromise.then(() => {
        var myChart = this.$echarts.init(document.getElementById('graph3'))
        var option = {
          title: {
            text: '方案相关'
          },
          tooltip: {
            trigger: 'axis'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          legend: {},
          dataset: {
            source: [
              ['日期', '新增方案', '当天已完成方案'],
              ['周一', 43, 35],
              ['周二', 33, 43],
              ['周三', 46, 65],
              ['周四', 42, 23],
              ['周五', 32, 53],
              ['周六', 52, 46],
              ['周日', 45, 50]
            ]
          },
          xAxis: {type: 'category'},
          yAxis: {},
          series: [
            {type: 'bar'},
            {type: 'bar'}
          ]
        }
        myChart.setOption(option)
      })
    },
    solutionAllEcharts() {
      let newPromise = new Promise((resolve) => {
        resolve()
      })
      newPromise.then(() => {
        var myChart = this.$echarts.init(document.getElementById('graph4'))
        var option = {
          title: {
            text: '方案相关'
          },
          tooltip: {
            trigger: 'axis'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          dataset: {
            source: [
              ['info', '周一', '周二', '周三', '周四', '周五', '周六', '周日'],
              ['已完成方案', 41, 30, 65, 53, 45, 37, 74],
              ['正在运行方案', 86, 92, 85, 83, 45, 76, 90],
              ['待运行方案', 24, 67, 79, 86, 56, 72, 78],
              ['运行错误方案', 5, 14, 7, 18, 13, 15, 13]
            ]
          },
          xAxis: [
            {type: 'category', gridIndex: 0},
            {type: 'category', gridIndex: 1}
          ],
          yAxis: [
            {gridIndex: 0},
            {gridIndex: 1}
          ],
          grid: [
            {bottom: '55%'},
            {top: '55%'}
          ],
          series: [
            // These series are in the first grid.
            {type: 'bar', seriesLayoutBy: 'row'},
            {type: 'bar', seriesLayoutBy: 'row'},
            {type: 'bar', seriesLayoutBy: 'row'},
            {type: 'bar', seriesLayoutBy: 'row'},
            // These series are in the second grid.
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1},
            {type: 'bar', xAxisIndex: 1, yAxisIndex: 1}
          ]
        }
        myChart.setOption(option)
      })
    },
    solutionCountEcharts() {
      let newPromise = new Promise((resolve) => {
        resolve()
      })
      newPromise.then(() => {
        var myChart = this.$echarts.init(document.getElementById('graph5'))
        var option = {
          title: {
            text: '方案统计'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: { },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          series: [
            {
              name: '访问来源',
              type: 'pie',
              radius: '50%',
              data: [
                {value: 1048, name: '已完成方案'},
                {value: 735, name: '正在运行方案'},
                {value: 580, name: '待运行方案'},
                {value: 44, name: '运行错误方案'},
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        myChart.setOption(option)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
    text-align: center;
  }
}
</style>
