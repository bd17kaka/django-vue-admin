<template>
  <div class="app-container">
    <div class="tbody">
      <el-steps :active="active" finish-status="success">
        <el-step title="运行时日志解析"></el-step>
        <el-step title="运行时日志表征提取"></el-step>
        <el-step title="分类器静态结构"></el-step>
        <el-step title="分类器动态训练过程"></el-step>
        <el-step title="结果展示"></el-step>
      </el-steps>
      <el-divider></el-divider>
      <div v-if="active==0">
        <el-button type="primary" plain @click="select_trace()">选择日志</el-button>
      </div>
      <!-- <div v-if="active==1">
        <el-button type="primary" plain @click="remake_trace()">开始重构</el-button>
      </div> -->
      <div v-if="active==1">
        <el-button type="primary" plain @click="generative_representation()">运行时日志表征提取</el-button>
        <el-button type="primary" plain @click="confirm3_1()">查看表征生成结果</el-button>
      </div>
      <div v-if="active==2">
        <el-button type="primary" plain @click="show_classifier()">查看分类器静态结构</el-button>
      </div>
      <div v-if="active==3">
        <el-button type="primary" plain @click="run_classifier()">运行分类器</el-button>
      </div>
      <div v-if="active==4">
        <el-button v-loading="loading6" element-loading-text="正在生成结果" type="primary" plain @click="show()">查看结果</el-button>
        
      </div>
      <el-divider></el-divider>
      <div align=right>
      <el-button v-if="active>0" style="margin-top: 12px;" @click="pre">上一步</el-button>
      <el-button v-if="active<4" style="margin-top: 12px;" @click="next">下一步</el-button>
      </div>
      

      <!--   步骤一   -->
      <el-dialog v-loading="loading1" element-loading-text="解析运行时日志中" :visible.sync="dialogVisible1" title="请选择运行时日志">
        <el-form
          ref="Form1"
          :model="trace"
          label-width="100px"
          label-position="right"
          :rules="rule1"
        >
          <el-form-item label="运行时日志" prop="trace_name">
            <el-radio-group v-model="trace.trace_name">
              <el-radio label="Memo">简单运行时日志</el-radio>
              <el-radio label="Calendar">复杂运行时日志</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm1('Form1')">开始解析</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible1_1" title="解析日志用时">
      <el-table :data="trace_list1" height="350" border>
        <el-table-column property="name" label="日志名称"></el-table-column>
        <el-table-column property="time" label="解析用时"></el-table-column>
      </el-table>
        <br>
        解析日志用时：{{time}}秒                        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        总计运行时日志数目：{{trace_list1.length}}      &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        平均解析用时：{{(time/trace_list1.length).toFixed(6)}}秒
      </el-dialog>

      <!--   步骤二   -->
      <el-dialog v-loading="loading2" element-loading-text="重构运行时日志中" :visible.sync="dialogVisible2" title="重构日志用时">
        重构日志用时： xx秒
      </el-dialog>

      <!--   步骤三   -->
      <el-dialog v-loading="loading3" element-loading-text="提取日志表征中" :visible.sync="dialogVisible3" title="请选择一种运行时日志表征提取">
        <el-form
          ref="Form3"
          :model="representation"
          label-width="100px"
          label-position="right"
          :rules="rule2"
        >
          <el-form-item label="表征类型" prop="representation_generator">
            <el-radio-group v-model="representation.representation_generator">
              <el-radio label="LEVEL_HISTO">LEVEL_HISTO</el-radio>
              <el-radio label="MCT_MTS">MCT_MTS</el-radio>
              <el-radio label="MCT_SEMANTIC_MTS">MCT_SEMANTIC_MTS</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="APP类型" prop="category_name">
            <el-radio-group v-model="representation.category_name">
              <el-radio label="Memo">Memo</el-radio>
              <el-radio label="Calendar">Calendar</el-radio>
              <el-radio label="Photography">Photography</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm3('Form3')">生成表征</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible3_1" title="生成表征用时">
        正在生成表征中，请等待
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible3_2" title="生成表征用时">
        生成表征用时：{{rep_time}}秒
      </el-dialog>
      <!--   步骤四   -->
      <el-dialog v-loading="loading4" element-loading-text="正在生成分类器静态结构" :visible.sync="dialogVisible4" title="查看分类器静态结构">
        <el-form
          ref="Form4"
          :model="classifier"
          label-width="100px"
          label-position="right"
          :rules="rule3"
        >
          <el-form-item label="分类器名称" prop="classifier_name">
            <el-radio-group v-model="classifier.classifier_name">
              <el-radio label="MLP">MLP</el-radio>
              <el-radio label="LSTM">LSTM</el-radio>
              <el-radio label="FCN">FCN</el-radio>
              <el-radio label="ResNet">ResNet</el-radio>
            </el-radio-group>
          </el-form-item>
          <!-- <el-form-item label="APP名称" prop="category_name">
            <el-radio-group v-model="classifier.category_name">
              <el-radio label="Memo">Memo</el-radio>
              <el-radio label="Calendar">Calendar</el-radio>
              <el-radio label="Photography">Photography</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="表征名称" prop="representation_generator">
            <el-radio-group v-model="classifier.representation_generator">
              <el-radio label="LEVEL_HISTO">LEVEL_HISTO</el-radio>
              <el-radio label="MCT_MTS">MCT_MTS</el-radio>
              <el-radio label="MCT_SEMANTIC_MTS">MCT_SEMANTIC_MTS</el-radio>
            </el-radio-group>
          </el-form-item> -->
          <el-button type="primary" @click="confirm4('Form4')">生成分类器静态结构</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible4_1" title="分类器静态结构生成完毕">
        <a :href="'http://localhost:6006/#graphs'" target="_blank"><el-button type="primary" >查看分类器结构详情</el-button></a>
      </el-dialog>

      <!--   步骤五   -->
      <el-dialog :visible.sync="dialogVisible5" title="运行分类器">
        <el-form
          ref="Form5"
          :model="training"
          label-width="100px"
          label-position="right"
          :rules="rule3"
        >
          <el-form-item label="分类器名称" prop="classifier_name">
            <el-radio-group v-model="training.classifier_name">
              <el-radio label="MLP">MLP</el-radio>
              <el-radio label="LSTM">LSTM</el-radio>
              <el-radio label="FCN">FCN</el-radio>
              <el-radio label="ResNet">ResNet</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="APP名称" prop="category_name">
            <el-radio-group v-model="training.category_name">
              <el-radio label="Memo">Memo</el-radio>
              <el-radio label="Calendar">Calendar</el-radio>
              <el-radio label="Photography">Photography</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="表征名称" prop="representation_generator">
            <el-radio-group v-model="training.representation_generator">
              <el-radio label="LEVEL_HISTO">LEVEL_HISTO</el-radio>
              <el-radio label="MCT_MTS">MCT_MTS</el-radio>
              <el-radio label="MCT_SEMANTIC_MTS">MCT_SEMANTIC_MTS</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm5('Form5')">运行分类器</el-button>
        </el-form>
      </el-dialog>

        <!-- 步骤六   -->
      <el-dialog :visible.sync="dialogVisible6_1" title="查看结果">
       分类器运行中，请等待
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible6_2" title="查看结果">
       训练分类器用时：{{run_time}}秒<br><br> 
       <a :href="'http://localhost:6006'" target="_blank"><el-button type="primary" >查看详细训练过程</el-button></a>
       <div style="text-align:center"><font size="5">实验结果</font></div>
       <div style="text-align:center">
         <img src="http://localhost:8000/media/result.png">
       </div>
      </el-dialog>
    </div>
  </div>
</template>
<style>
.tbody{
    width:80%;
    margin-left:10%;
    margin-top: 2%;
}
</style>
<script>
import { 
        getTracename, 
        getRepresentation,
        getRepresentationResult,
        getClassifier,
        getTraining,
        getResult
       } 
        from "@/api/test"

export default {
  data() {
    return {
      timer: '',
      active: 0,
      loading1: false,
      loading2: false,
      loading3: false,
      loading4: false,
      loading5: false,
      loading6: false,
      trace_list1: [],
      time: '',
      rep_time: '',
      trace: {
        trace_name: ''
      },
      representation: {
        representation_generator: '',
        category_name: ''
      },
      classifier: {
        classifier_name: '',
        category_name: '',
        representation_generator: ''
      },
      training: {
        classifier_name: '',
        category_name: '',
        representation_generator: ''
      },
      flag: '',
      done: '',
      run_time: '',
      acc: '',
      dialogVisible1: false,
      dialogVisible2: false,
      dialogVisible3: false,
      dialogVisible4: false,
      dialogVisible5: false,
      dialogVisible6: false,
      dialogVisible1_1: false,
      dialogVisible3_1: false,
      dialogVisible3_2: false,
      dialogVisible4_1: false,
      dialogVisible5_1: false,
      dialogVisible6_1: false,
      dialogVisible6_2: false,
      rule1: { trace_name: [{ required: true, message: '请选择日志', trigger: 'blur' }] },
      rule2: { representation_name: [{ required: true, message: '请选择表征', trigger: 'blur' }] },
      rule3: { 
        classifier_name: [{ required: true, message: '请选择分类器', trigger: 'blur' }],
        category_name: [{ required: true, message: '请选择APP名称', trigger: 'blur' }],
        representation_generator: [{ required: true, message: '请选择表征', trigger: 'blur' }]
      },
      rule4: {
        classifier_name: [{ required: true, message: '请选择分类器', trigger: 'blur' }],
        class_of_procedure: [{ required: true, message: '请选择程序类别', trigger: 'blur' }],
        representation_name: [{ required: true, message: '请选择表征', trigger: 'blur' }]
      }
    }
  },
  methods: {
    select_trace() {
      this.dialogVisible1 = true
    },
    remake_trace() {
      this.dialogVisible2 = true
    },
    generative_representation() {
      this.dialogVisible3 = true
    },
    show_classifier() {
      this.dialogVisible4 = true
    },
    run_classifier() {
      this.dialogVisible5 = true
    },
    show_result() {
      this.dialogVisible6 = true
    },
    async confirm1(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.loading1 = true
          getTracename(this.trace).then(res => {
            this.time = res.data.data['time']
            this.loading1 = false
            this.trace_list1 = res.data.data.trace_list
            this.dialogVisible1_1 = true
          })
        }
      })
    },
    async confirm3(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          getRepresentation(this.representation).then(res => {
            // this.active = 2
            this.dialogVisible3 = false
            // this.dialogVisible3_1 = true
          })
        }
      })
    },
    async confirm3_1() {
      getRepresentationResult().then(res => {
          this.flag = res.data.data.done
          if(this.flag == 0) {
            this.dialogVisible3_1 = true
          }
          else {
            this.dialogVisible3_2 = true
            this.rep_time = res.data.data.time
          }
        })
    },
    async confirm4(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.loading4 = true
          getClassifier(this.classifier).then(res => {
            this.loading4 = false
            this.dialogVisible4_1 = true
          })
        }
      })
    },
    async confirm5(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          getTraining(this.training).then(res => {
            this.active = 4
            this.dialogVisible5 = false
          })
        }
      })
    },
    async confirm6() {
      this.loading6 = true
      getResult(this.training).then(res => {
          // console.log(res.data)
          this.done = res.data.data.done
          if(this.done == 0) {
            // this.loading6 = false
            // this.dialogVisible6_1 = true
          }
          else {
            this.run_time = res.data.data.time
            this.loading6 = false
            this.dialogVisible6_2 = true
            clearInterval(this.timer)
          }
          // console.log(this.done)
          // console.log(this.acc)
        })
    },
    next() {
      if (this.active++ > 3) this.active = 0
    },
    pre() {
      if (this.active-- < 1) this.active = 0
    },
    show() {
      this.timer = setInterval(this.confirm6,1000);
    }  
  },
  
}
</script>
