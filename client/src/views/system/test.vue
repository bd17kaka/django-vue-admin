<template>
  <div class="app-container">
    <div class="tbody">
      <el-steps :active="active" finish-status="success">
        <el-step title="运行时日志解析"></el-step>
        <el-step title="运行时日志重构"></el-step>
        <el-step title="运行时日志表征提取"></el-step>
        <el-step title="分类器静态结构"></el-step>
        <el-step title="分类器动态训练过程"></el-step>
        <el-step title="结果展示"></el-step>
      </el-steps>
      <el-divider></el-divider>
      <div v-if="active==1">
        <el-button type="primary" plain @click="select_trace()">选择日志</el-button>
      </div>
      <div v-if="active==2">
        <el-button type="primary" plain @click="remake_trace()">开始重构</el-button>
      </div>
      <div v-if="active==3">
        <el-button type="primary" plain @click="generative_representation()">运行日志表征提取</el-button>
      </div>
      <div v-if="active==4">
        <el-button type="primary" plain @click="show_classifier()">查看分类器</el-button>
      </div>
      <div v-if="active==5">
        <el-button type="primary" plain @click="run_classifier()">运行分类器</el-button>
      </div>
      <div v-if="active==6">
        <el-button type="primary" plain @click="show_result()">查看实验结果</el-button>
      </div>
      <el-divider></el-divider>
      <el-button v-if="active<6" style="margin-top: 12px;" @click="next">下一步</el-button>
      <el-button v-if="active>1" style="margin-top: 12px;" @click="pre">上一步</el-button>

      <!--   步骤一   -->
      <el-dialog :visible.sync="dialogVisible1" title="请选择运行时日志">
        <el-form
          ref="Form1"
          :model="trace"
          label-width="80px"
          label-position="right"
          :rules="rule1"
        >
          <el-form-item label="运行时日志" prop="trace_name">
            <el-radio-group v-model="trace.trace_name">
              <el-radio label="简单运行时日志"></el-radio>
              <el-radio label="复杂运行时日志"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm1('Form1')">开始解析</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible1_1" title="解析日志用时">
        解析日志用时： xx秒
      </el-dialog>

      <!--   步骤二   -->
      <el-dialog :visible.sync="dialogVisible2" title="重构日志用时">
        重构日志用时： xx秒
      </el-dialog>

      <!--   步骤三   -->
      <el-dialog :visible.sync="dialogVisible3" title="请选择一种运行时日志表征提取">
        <el-form
          ref="Form3"
          :model="representation"
          label-width="80px"
          label-position="right"
          :rules="rule2"
        >
          <el-form-item label="表征" prop="representation_name">
            <el-radio-group v-model="representation.representation_name">
              <el-radio label="时序表征"></el-radio>
              <el-radio label="语义表征"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm3('Form3')">生成表征</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible3_1" title="生成表征用时">
        生成表征用时： xx秒
      </el-dialog>

      <!--   步骤四   -->
      <el-dialog :visible.sync="dialogVisible4" title="请选择一种分类器">
        <el-form
          ref="Form4"
          :model="classifier1"
          label-width="80px"
          label-position="right"
          :rules="rule3"
        >
          <el-form-item label="分类器" prop="classifier_name">
            <el-radio-group v-model="classifier1.classifier_name">
              <el-radio label="分类器1"></el-radio>
              <el-radio label="分类器2"></el-radio>
              <el-radio label="分类器3"></el-radio>
              <el-radio label="分类器4"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm4('Form4')">查看分类器结构详情</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible4_1" title="查看分类器结构详情用时">
        查看分类器结构详情用时： xx秒
      </el-dialog>

      <!--   步骤五   -->
      <el-dialog :visible.sync="dialogVisible5" title="分类器动态训练">
        <el-form
          ref="Form5"
          :model="classifier2"
          label-width="80px"
          label-position="right"
          :rules="rule4"
        >
          <el-form-item label="分类器" prop="classifier_name">
            <el-radio-group v-model="classifier2.classifier_name">
              <el-radio label="分类器1"></el-radio>
              <el-radio label="分类器2"></el-radio>
              <el-radio label="分类器3"></el-radio>
              <el-radio label="分类器4"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="程序类别" prop="class_of_procedure">
            <el-radio-group v-model="classifier2.class_of_procedure">
              <el-radio label="程序类别1"></el-radio>
              <el-radio label="程序类别2"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="表征生成策略" prop="representation_name">
            <el-radio-group v-model="classifier2.representation_name">
              <el-radio label="时序表征"></el-radio>
              <el-radio label="语义表征"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm5('Form5')">查看过程详情</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible5_1" title="查看过程详情用时">
        查看过程详情用时： xx秒
      </el-dialog>

      <!--   步骤六   -->
      <el-dialog :visible.sync="dialogVisible6" title="分类器动态训练">
        <el-form
          ref="Form6"
          :model="classifier2"
          label-width="80px"
          label-position="right"
          :rules="rule4"
        >
          <el-form-item label="分类器" prop="classifier_name">
            <el-radio-group v-model="classifier2.classifier_name">
              <el-radio label="分类器1"></el-radio>
              <el-radio label="分类器2"></el-radio>
              <el-radio label="分类器3"></el-radio>
              <el-radio label="分类器4"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="程序类别" prop="class_of_procedure">
            <el-radio-group v-model="classifier2.class_of_procedure">
              <el-radio label="程序类别1"></el-radio>
              <el-radio label="程序类别2"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="表征生成策略" prop="representation_name">
            <el-radio-group v-model="classifier2.representation_name">
              <el-radio label="时序表征"></el-radio>
              <el-radio label="语义表征"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-button type="primary" @click="confirm6('Form6')">查看实验详情</el-button>
        </el-form>
      </el-dialog>
      <el-dialog :visible.sync="dialogVisible6_1" title="查看实验详情用时">
        查看实验详情用时： xx秒
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
export default {
  data() {
    return {
      active: 1,
      trace: {
        trace_name: ''
      },
      representation: {
        representation_name: ''
      },
      classifier1: {
        classifier_name: ''
      },
      classifier2: {
        classifier_name: '',
        class_of_procedure: '',
        representation_name: ''
      },
      dialogVisible1: false,
      dialogVisible2: false,
      dialogVisible3: false,
      dialogVisible4: false,
      dialogVisible5: false,
      dialogVisible6: false,
      dialogVisible1_1: false,
      dialogVisible3_1: false,
      dialogVisible4_1: false,
      dialogVisible5_1: false,
      dialogVisible6_1: false,
      rule1: { trace_name: [{ required: true, message: '请选择日志', trigger: 'blur' }] },
      rule2: { representation_name: [{ required: true, message: '请选择表征', trigger: 'blur' }] },
      rule3: { classifier_name: [{ required: true, message: '请选择分类器', trigger: 'blur' }] },
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
          this.dialogVisible1_1 = true
        }
      })
    },
    async confirm3(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.dialogVisible3_1 = true
        }
      })
    },
    async confirm4(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.dialogVisible4_1 = true
        }
      })
    },
    async confirm5(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.dialogVisible5_1 = true
        }
      })
    },
    async confirm6(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          this.dialogVisible6_1 = true
        }
      })
    },
    next() {
      if (this.active++ > 5) this.active = 1
    },
    pre() {
      if (this.active-- < 2) this.active = 1
    }
  }
}
</script>
