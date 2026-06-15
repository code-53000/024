<template>
  <div class="specimen-list">
    <el-card class="filter-card" shadow="hover">
      <el-form :model="filterForm" inline>
        <el-form-item label="关键词">
          <el-input
            v-model="filterForm.keyword"
            placeholder="名称、编号、产地"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="矿物类型">
          <el-select
            v-model="filterForm.mineral_type"
            placeholder="请选择"
            clearable
            style="width: 160px"
          >
            <el-option
              v-for="type in mineralTypes"
              :key="type"
              :label="type"
              :value="type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="晶系">
          <el-select
            v-model="filterForm.crystal_system"
            placeholder="请选择"
            clearable
            style="width: 140px"
          >
            <el-option
              v-for="system in crystalSystems"
              :key="system.value"
              :label="system.label"
              :value="system.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="省份">
          <el-select
            v-model="filterForm.province"
            placeholder="请选择"
            clearable
            style="width: 140px"
            filterable
          >
            <el-option
              v-for="province in provinces"
              :key="province"
              :label="province"
              :value="province"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="鉴定状态">
          <el-select
            v-model="filterForm.identification_status"
            placeholder="请选择"
            clearable
            style="width: 120px"
          >
            <el-option label="待鉴定" value="pending" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="有争议" value="disputed" />
          </el-select>
        </el-form-item>
        <el-form-item label="获取方式">
          <el-select
            v-model="filterForm.acquisition_method"
            placeholder="请选择"
            clearable
            style="width: 120px"
          >
            <el-option
              v-for="method in acquisitionMethods"
              :key="method.value"
              :label="method.label"
              :value="method.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">
            搜索
          </el-button>
          <el-button :icon="Refresh" @click="handleReset">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="list-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="card-title">标本列表</span>
          <div class="card-actions">
            <el-button type="primary" :icon="Add" @click="goToCreate">
              新增标本
            </el-button>
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
        <el-table-column prop="crystal_system" label="晶系" width="100">
          <template #default="{ row }">
            {{ getCrystalSystemLabel(row.crystal_system) }}
          </template>
        </el-table-column>
        <el-table-column label="鉴定状态" width="100">
          <template #default="{ row }">
            <StatusTag :status="row.identification_status" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToDetail(row.id)">
              详情
            </el-button>
            <el-button type="primary" link @click="goToEdit(row.id)">
              编辑
            </el-button>
            <el-button type="danger" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getSpecimens,
  getMineralTypes,
  getProvinces,
  deleteSpecimen
} from '@/api/specimen'
import StatusTag from '@/components/StatusTag.vue'

const router = useRouter()

const loading = ref(false)
const specimens = ref([])
const mineralTypes = ref([])
const provinces = ref([])

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

const filterForm = reactive({
  keyword: '',
  mineral_type: '',
  crystal_system: '',
  province: '',
  identification_status: '',
  acquisition_method: ''
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const getCrystalSystemLabel = (value) => {
  const system = crystalSystems.find(s => s.value === value)
  return system?.label || value || '-'
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const loadDictionary = async () => {
  try {
    const [typesRes, provincesRes] = await Promise.all([
      getMineralTypes(),
      getProvinces()
    ])
    mineralTypes.value = typesRes.data
    provinces.value = provincesRes.data
  } catch (error) {
    console.error('加载字典数据失败:', error)
  }
}

const loadSpecimens = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...filterForm
    }
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })
    
    const response = await getSpecimens(params)
    specimens.value = response.data.items
    pagination.total = response.data.total
  } catch (error) {
    console.error('加载标本列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadSpecimens()
}

const handleReset = () => {
  Object.assign(filterForm, {
    keyword: '',
    mineral_type: '',
    crystal_system: '',
    province: '',
    identification_status: '',
    acquisition_method: ''
  })
  pagination.page = 1
  loadSpecimens()
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

const goToCreate = () => {
  router.push('/specimens/create')
}

const goToDetail = (id) => {
  router.push(`/specimens/${id}`)
}

const goToEdit = (id) => {
  router.push(`/specimens/${id}/edit`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除标本"${row.name}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteSpecimen(row.id)
    ElMessage.success('删除成功')
    loadSpecimens()
  } catch {
  }
}

onMounted(() => {
  loadDictionary()
  loadSpecimens()
})
</script>

<style scoped>
.specimen-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-card {
  border-radius: 12px;
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

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.text-muted {
  color: #c0c4cc;
}
</style>
