<template>
  <div class="specimen-detail" v-loading="loading">
    <el-card v-if="specimen" class="detail-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <h2 class="specimen-title">{{ specimen.name }}</h2>
            <StatusTag :status="specimen.identification_status" />
          </div>
          <div class="header-right">
            <el-button :icon="ArrowLeft" @click="goBack">
              返回列表
            </el-button>
            <el-button type="primary" :icon="Edit" @click="goToEdit">
              编辑
            </el-button>
          </div>
        </div>
      </template>

      <div class="detail-content">
        <div class="detail-gallery">
          <div v-if="photos.length > 0" class="gallery-main">
            <img :src="currentPhoto.url" :alt="currentPhoto.caption || specimen.name" />
          </div>
          <div v-else class="gallery-placeholder">
            <el-icon :size="64"><Picture /></el-icon>
            <p>暂无照片</p>
          </div>
          
          <div v-if="photos.length > 1" class="gallery-thumbs">
            <div
              v-for="(photo, index) in photos"
              :key="photo.id"
              class="thumb-item"
              :class="{ active: currentPhotoIndex === index }"
              @click="currentPhotoIndex = index"
            >
              <img :src="photo.url" :alt="photo.caption" />
              <div v-if="photo.is_primary" class="thumb-badge">
                <el-icon><Star /></el-icon>
              </div>
            </div>
          </div>

          <el-divider />
          
          <PhotoUpload
            v-if="showUpload"
            :specimen-id="specimen.id"
            @upload-success="handleUploadSuccess"
          />
          <el-button
            v-else
            type="primary"
            :icon="Upload"
            @click="showUpload = true"
            style="width: 100%"
          >
            上传照片
          </el-button>
        </div>

        <div class="detail-info">
          <el-descriptions :column="2" border size="default">
            <el-descriptions-item label="标本编号">
              {{ specimen.specimen_no }}
            </el-descriptions-item>
            <el-descriptions-item label="矿物类型">
              {{ specimen.mineral_type }}
              <span v-if="specimen.variety"> ({{ specimen.variety }})</span>
            </el-descriptions-item>
            <el-descriptions-item label="晶系">
              {{ getCrystalSystemLabel(specimen.crystal_system) }}
            </el-descriptions-item>
            <el-descriptions-item label="晶体形态">
              {{ specimen.crystal_form || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="颜色">
              {{ specimen.color || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="光泽">
              {{ specimen.luster || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="透明度">
              {{ specimen.transparency || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="摩氏硬度">
              <span v-if="specimen.mohs_hardness_min || specimen.mohs_hardness_max">
                {{ specimen.mohs_hardness_min || '?' }}
                <span v-if="specimen.mohs_hardness_max && specimen.mohs_hardness_max !== specimen.mohs_hardness_min">
                  - {{ specimen.mohs_hardness_max }}
                </span>
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="比重">
              <span v-if="specimen.specific_gravity_min || specimen.specific_gravity_max">
                {{ specimen.specific_gravity_min || '?' }}
                <span v-if="specimen.specific_gravity_max && specimen.specific_gravity_max !== specimen.specific_gravity_min">
                  - {{ specimen.specific_gravity_max }}
                </span>
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="尺寸">
              {{ specimen.size || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="重量">
              <span v-if="specimen.weight">
                {{ specimen.weight }} {{ specimen.weight_unit || 'g' }}
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="解理">
              {{ specimen.cleavage || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="断口">
              {{ specimen.fracture || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="条痕">
              {{ specimen.streak || '-' }}
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">产地信息</el-divider>
          <el-descriptions :column="2" border size="default">
            <el-descriptions-item label="国家">
              {{ specimen.country || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="省份">
              {{ specimen.province || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="具体产地" :span="2">
              {{ specimen.locality || '-' }}
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">获取信息</el-divider>
          <el-descriptions :column="2" border size="default">
            <el-descriptions-item label="获取方式">
              {{ getAcquisitionMethodLabel(specimen.acquisition_method) }}
            </el-descriptions-item>
            <el-descriptions-item label="获取日期">
              {{ formatDate(specimen.acquisition_date) }}
            </el-descriptions-item>
            <el-descriptions-item label="价格">
              <span v-if="specimen.price">
                {{ specimen.price }} {{ specimen.currency || 'CNY' }}
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="来源">
              {{ specimen.dealer || '-' }}
            </el-descriptions-item>
          </el-descriptions>

          <el-divider content-position="left">其他信息</el-divider>
          <el-descriptions :column="1" border size="default">
            <el-descriptions-item label="描述">
              {{ specimen.description || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="备注">
              {{ specimen.notes || '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-card>

    <el-card v-if="specimen" class="identification-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="card-title">鉴定记录</span>
        </div>
      </template>
      
      <el-timeline v-if="identifications.length > 0">
        <el-timeline-item
          v-for="item in identifications"
          :key="item.id"
          :timestamp="formatDateTime(item.created_at)"
          placement="top"
        >
          <el-card shadow="never">
            <div class="identification-header">
              <StatusTag :status="item.new_status" />
              <span class="identifier">鉴定人: {{ item.identifier?.full_name || item.identifier?.username }}</span>
            </div>
            <p class="identification-notes">{{ item.notes || '暂无备注' }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      <el-empty v-else description="暂无鉴定记录" :image-size="80" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSpecimenById } from '@/api/specimen'
import { getSpecimenPhotos } from '@/api/photo'
import { getSpecimenIdentifications } from '@/api/identification'
import StatusTag from '@/components/StatusTag.vue'
import PhotoUpload from '@/components/PhotoUpload.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const specimen = ref(null)
const photos = ref([])
const identifications = ref([])
const currentPhotoIndex = ref(0)
const showUpload = ref(false)

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

const currentPhoto = computed(() => {
  return photos.value[currentPhotoIndex.value] || { url: '' }
})

const getCrystalSystemLabel = (value) => {
  const system = crystalSystems.find(s => s.value === value)
  return system?.label || value || '-'
}

const getAcquisitionMethodLabel = (value) => {
  const method = acquisitionMethods.find(m => m.value === value)
  return method?.label || value || '-'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const loadDetail = async () => {
  const id = route.params.id
  if (!id) return

  loading.value = true
  try {
    const [specimenRes, photosRes, identRes] = await Promise.all([
      getSpecimenById(id),
      getSpecimenPhotos(id),
      getSpecimenIdentifications(id)
    ])
    specimen.value = specimenRes.data
    photos.value = photosRes.data
    identifications.value = identRes.data
    
    const primaryIndex = photos.value.findIndex(p => p.is_primary)
    currentPhotoIndex.value = primaryIndex >= 0 ? primaryIndex : 0
  } catch (error) {
    console.error('加载详情失败:', error)
  } finally {
    loading.value = false
  }
}

const handleUploadSuccess = (newPhotos) => {
  photos.value = [...photos.value, ...newPhotos]
  showUpload.value = false
}

const goBack = () => {
  router.push('/specimens')
}

const goToEdit = () => {
  router.push(`/specimens/${specimen.value.id}/edit`)
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.specimen-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-card,
.identification-card {
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

.specimen-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.detail-content {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
}

.detail-gallery {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gallery-main {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f5f5;
}

.gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-placeholder {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
  gap: 8px;
}

.gallery-thumbs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.thumb-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumb-item.active {
  border-color: #409eff;
}

.thumb-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #409eff;
  color: white;
  padding: 2px;
  border-radius: 4px;
  font-size: 12px;
}

.identification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.identifier {
  font-size: 12px;
  color: #909399;
}

.identification-notes {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

@media (max-width: 992px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
}
</style>
