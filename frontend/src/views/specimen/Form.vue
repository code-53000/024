<template>
  <div class="specimen-form">
    <el-card class="form-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button :icon="ArrowLeft" @click="goBack" circle />
            <h2 class="form-title">{{ isEdit ? '编辑标本' : '新增标本' }}</h2>
          </div>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        label-position="right"
      >
        <el-divider content-position="left">基本信息</el-divider>
        
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="标本编号" prop="specimen_no">
              <el-input v-model="formData.specimen_no" placeholder="可不填，系统自动生成" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="标本名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入标本名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="矿物类型" prop="mineral_type">
              <el-select
                v-model="formData.mineral_type"
                placeholder="请选择或输入矿物类型"
                filterable
                allow-create
                default-first-option
                style="width: 100%"
              >
                <el-option
                  v-for="type in mineralTypes"
                  :key="type"
                  :label="type"
                  :value="type"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="变种">
              <el-input v-model="formData.variety" placeholder="如：紫水晶、烟晶等" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">物理性质</el-divider>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="晶系">
              <el-select v-model="formData.crystal_system" placeholder="请选择晶系" style="width: 100%">
                <el-option
                  v-for="system in crystalSystems"
                  :key="system.value"
                  :label="system.label"
                  :value="system.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="晶体形态">
              <el-input v-model="formData.crystal_form" placeholder="如：立方体、八面体等" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="8">
            <el-form-item label="颜色">
              <el-input v-model="formData.color" placeholder="请输入颜色" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="光泽">
              <el-input v-model="formData.luster" placeholder="如：玻璃光泽、金属光泽等" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="透明度">
              <el-input v-model="formData.transparency" placeholder="如：透明、半透明等" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="8">
            <el-form-item label="摩氏硬度">
              <el-input-number
                v-model="formData.mohs_hardness_min"
                :min="0"
                :max="10"
                :step="0.5"
                placeholder="最小"
                style="width: 100%"
              />
              <span style="display: inline-block; text-align: center; width: 30px">-</span>
              <el-input-number
                v-model="formData.mohs_hardness_max"
                :min="0"
                :max="10"
                :step="0.5"
                placeholder="最大"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="比重">
              <el-input-number
                v-model="formData.specific_gravity_min"
                :min="0"
                :step="0.1"
                placeholder="最小"
                style="width: 100%"
              />
              <span style="display: inline-block; text-align: center; width: 30px">-</span>
              <el-input-number
                v-model="formData.specific_gravity_max"
                :min="0"
                :step="0.1"
                placeholder="最大"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="条痕">
              <el-input v-model="formData.streak" placeholder="请输入条痕颜色" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="8">
            <el-form-item label="解理">
              <el-input v-model="formData.cleavage" placeholder="请输入解理描述" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="断口">
              <el-input v-model="formData.fracture" placeholder="请输入断口描述" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="尺寸">
              <el-input v-model="formData.size" placeholder="如：3x2x1 cm" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="重量">
              <el-input-number
                v-model="formData.weight"
                :min="0"
                :step="0.1"
                placeholder="请输入重量"
                style="width: 70%"
              />
              <el-select v-model="formData.weight_unit" style="width: 28%; margin-left: 2%">
                <el-option label="克 (g)" value="g" />
                <el-option label="千克 (kg)" value="kg" />
                <el-option label="克拉 (ct)" value="ct" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="鉴定状态" v-if="isEdit">
              <el-select v-model="formData.identification_status" style="width: 100%">
                <el-option label="待鉴定" value="pending" />
                <el-option label="已确认" value="confirmed" />
                <el-option label="有争议" value="disputed" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">产地信息</el-divider>

        <el-row :gutter="24">
          <el-col :span="8">
            <el-form-item label="国家">
              <el-input v-model="formData.country" placeholder="请输入国家" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="省份">
              <el-select
                v-model="formData.province"
                placeholder="请选择或输入省份"
                filterable
                allow-create
                default-first-option
                style="width: 100%"
              >
                <el-option
                  v-for="province in provinces"
                  :key="province"
                  :label="province"
                  :value="province"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="具体产地">
              <el-select
                v-model="formData.locality"
                placeholder="请选择或输入产地"
                filterable
                allow-create
                default-first-option
                style="width: 100%"
              >
                <el-option
                  v-for="locality in localities"
                  :key="locality"
                  :label="locality"
                  :value="locality"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">获取信息</el-divider>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="获取方式">
              <el-select v-model="formData.acquisition_method" placeholder="请选择获取方式" style="width: 100%">
                <el-option
                  v-for="method in acquisitionMethods"
                  :key="method.value"
                  :label="method.label"
                  :value="method.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="获取日期">
              <el-date-picker
                v-model="formData.acquisition_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="价格">
              <el-input-number
                v-model="formData.price"
                :min="0"
                :step="0.01"
                placeholder="请输入价格"
                style="width: 70%"
              />
              <el-select v-model="formData.currency" style="width: 28%; margin-left: 2%">
                <el-option label="人民币 (CNY)" value="CNY" />
                <el-option label="美元 (USD)" value="USD" />
                <el-option label="欧元 (EUR)" value="EUR" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="来源/商家">
              <el-input v-model="formData.dealer" placeholder="请输入商家或来源" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">其他信息</el-divider>

        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入标本的详细描述"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="formData.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入其他备注信息"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :icon="Check" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '提交' }}
          </el-button>
          <el-button :icon="Close" @click="goBack">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  getSpecimenById,
  createSpecimen,
  updateSpecimen,
  getMineralTypes,
  getProvinces,
  getLocalities
} from '@/api/specimen'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)
const mineralTypes = ref([])
const provinces = ref([])
const localities = ref([])

const isEdit = computed(() => !!route.params.id)

const crystalSystems = [
  { value: 'isometric', label: '等轴晶系' },
  { value: 'tetragonal', label: '四方晶系' },
  { value: 'orthorhombic', label: '斜方晶系' },
  { value: 'hexagonal', label: '六方晶系' },
  { value: 'trigonal', label: '三方晶系' },
  { value: 'monoclinic', label: '单斜晶系' },
  { value: 'triclinic', label: '三斜晶系' },
  { value: 'amorphous', label: '非晶质' }
]

const acquisitionMethods = [
  { value: 'purchase', label: '购买' },
  { value: 'mining', label: '采集' },
  { value: 'gift', label: '赠送' },
  { value: 'trade', label: '交换' },
  { value: 'excavation', label: '发掘' },
  { value: 'other', label: '其他' }
]

const formData = reactive({
  specimen_no: '',
  name: '',
  mineral_type: '',
  variety: '',
  locality: '',
  province: '',
  country: '',
  mohs_hardness_min: null,
  mohs_hardness_max: null,
  crystal_system: '',
  crystal_form: '',
  color: '',
  luster: '',
  transparency: '',
  cleavage: '',
  fracture: '',
  streak: '',
  specific_gravity_min: null,
  specific_gravity_max: null,
  size: '',
  weight: null,
  weight_unit: 'g',
  acquisition_method: '',
  acquisition_date: '',
  price: null,
  currency: 'CNY',
  dealer: '',
  description: '',
  notes: '',
  identification_status: 'pending'
})

const formRules = {
  name: [
    { required: true, message: '请输入标本名称', trigger: 'blur' },
    { max: 200, message: '名称长度不能超过 200 个字符', trigger: 'blur' }
  ],
  mineral_type: [
    { required: true, message: '请选择或输入矿物类型', trigger: 'change' },
    { max: 100, message: '矿物类型长度不能超过 100 个字符', trigger: 'blur' }
  ]
}

const loadDictionary = async () => {
  try {
    const [typesRes, provincesRes, localitiesRes] = await Promise.all([
      getMineralTypes(),
      getProvinces(),
      getLocalities()
    ])
    mineralTypes.value = typesRes.data
    provinces.value = provincesRes.data
    localities.value = localitiesRes.data
  } catch (error) {
    console.error('加载字典数据失败:', error)
  }
}

const loadSpecimen = async () => {
  if (!isEdit.value) return

  try {
    const response = await getSpecimenById(route.params.id)
    Object.assign(formData, response.data)
    if (formData.acquisition_date) {
      formData.acquisition_date = formData.acquisition_date.substring(0, 10)
    }
  } catch (error) {
    console.error('加载标本数据失败:', error)
    ElMessage.error('加载标本数据失败')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    const submitData = { ...formData }
    
    Object.keys(submitData).forEach(key => {
      if (submitData[key] === '' || submitData[key] === null || submitData[key] === undefined) {
        if (key !== 'weight_unit' && key !== 'currency' && key !== 'identification_status') {
          delete submitData[key]
        }
      }
    })

    if (isEdit.value) {
      delete submitData.specimen_no
      await updateSpecimen(route.params.id, submitData)
      ElMessage.success('修改成功')
    } else {
      const response = await createSpecimen(submitData)
      ElMessage.success('创建成功')
      router.push(`/specimens/${response.data.id}`)
      return
    }

    router.push(`/specimens/${route.params.id}`)
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadDictionary()
  loadSpecimen()
})
</script>

<style scoped>
.specimen-form {
  max-width: 1000px;
  margin: 0 auto;
}

.form-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.form-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.el-form-item--small .el-form-item__label {
  font-size: 13px;
}
</style>
