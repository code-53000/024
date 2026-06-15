<template>
  <div class="identification-list">
    <el-card class="list-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="card-title">待鉴定标本列表</span>
          <div class="card-actions">
            <el-tag type="warning" effect="dark">
              共 {{ pendingCount }} 件待鉴定
            </el-tag>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="specimens"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="specimen_no" label="编号" width="120" />
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="mineral_type" label="矿物类型" width="120" />
        <el-table-column label="产地" min-width="180">
          <template #default="{ row }">
            <span v-if="row.locality || row.province || row.country">
              {{ [row.country, row.province, row.locality].filter(Boolean).join(' / ') }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="当前状态" width="100">
          <template #default="{ row }">
            <StatusTag :status="row.identification_status" />
          </template>
        </el-table-column>
        <el-table-column label="收藏者" width="140">
          <template #default="{ row }">
            {{ row.owner?.full_name || row.owner?.username || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">
              查看详情
            </el-button>
            <el-button type="success" link @click="handleIdentify(row)">
              鉴定
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="specimens.length === 0 && !loading" class="empty-container">
        <el-empty description="暂无待鉴定标本" :image-size="100" />
      </div>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="identifyDialogVisible"
      title="标本鉴定"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="identifyForm"
        :model="identifyFormData"
        :rules="identifyRules"
        label-width="100px"
      >
        <el-form-item label="标本名称">
          <el-input :model-value="currentSpecimen?.name" disabled />
        </el-form-item>
        <el-form-item label="当前状态">
          <StatusTag :status="currentSpecimen?.identification_status" />
        </el-form-item>
        <el-form-item label="鉴定结果" prop="new_status">
          <el-select v-model="identifyFormData.new_status" placeholder="请选择鉴定结果" style="width: 100%">
            <el-option
              v-for="status in allowedTransitions"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="鉴定备注" prop="notes">
          <el-input
            v-model="identifyFormData.notes"
            type="textarea"
            :rows="4"
            placeholder="请输入鉴定备注说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="identifyDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmitIdentify">
          提交鉴定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPendingIdentifications, createIdentification } from '@/api/identification'
import StatusTag from '@/components/StatusTag.vue'

const router = useRouter()

const loading = ref(false)
const submitting = ref(false)
const specimens = ref([])
const pendingCount = ref(0)
const identifyDialogVisible = ref(false)
const identifyForm = ref(null)
const currentSpecimen = ref(null)

const statusOptions = [
  { value: 'pending', label: '待鉴定' },
  { value: 'confirmed', label: '已确认' },
  { value: 'disputed', label: '有争议' }
]

const allowedTransitions = [
  { value: 'confirmed', label: '确认' },
  { value: 'disputed', label: '标记为有争议' }
]

const identifyFormData = reactive({
  specimen_id: null,
  new_status: '',
  notes: ''
})

const identifyRules = {
  new_status: [
    { required: true, message: '请选择鉴定结果', trigger: 'change' }
  ],
  notes: [
    { max: 1000, message: '备注长度不能超过 1000 个字符', trigger: 'blur' }
  ]
}

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const loadSpecimens = async () => {
  loading.value = true
  try {
    const response = await getPendingIdentifications({
      page: pagination.page,
      page_size: pagination.page_size
    })
    specimens.value = response.data
    pendingCount.value = response.data.length
  } catch (error) {
    console.error('加载待鉴定列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  loadSpecimens()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadSpecimens()
}

const goToDetail = (id) => {
  router.push(`/specimens/${id}`)
}

const handleIdentify = (row) => {
  currentSpecimen.value = row
  identifyFormData.specimen_id = row.id
  identifyFormData.new_status = ''
  identifyFormData.notes = ''
  identifyDialogVisible.value = true
}

const handleSubmitIdentify = async () => {
  if (!identifyForm.value) return

  try {
    await identifyForm.value.validate()
    submitting.value = true

    await createIdentification({
      specimen_id: identifyFormData.specimen_id,
      new_status: identifyFormData.new_status,
      notes: identifyFormData.notes
    })

    ElMessage.success('鉴定提交成功')
    identifyDialogVisible.value = false
    loadSpecimens()
  } catch (error) {
    console.error('提交鉴定失败:', error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadSpecimens()
})
</script>

<style scoped>
.identification-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.empty-container {
  padding: 60px 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.text-muted {
  color: #c0c4cc;
}
</style>
