<template>
  <el-card class="specimen-card" shadow="hover" @click="handleClick">
    <div class="card-image">
      <img v-if="primaryPhoto" :src="primaryPhoto.url" :alt="specimen.name" />
      <div v-else class="image-placeholder">
        <el-icon :size="48"><Picture /></el-icon>
      </div>
      <div class="card-status">
        <StatusTag :status="specimen.identification_status" />
      </div>
    </div>
    <div class="card-content">
      <h3 class="specimen-name">{{ specimen.name }}</h3>
      <p class="specimen-no">编号: {{ specimen.specimen_no }}</p>
      <p class="specimen-type">
        <el-icon><Gem /></el-icon>
        {{ specimen.mineral_type }}
        <span v-if="specimen.variety"> ({{ specimen.variety }})</span>
      </p>
      <p class="specimen-locality" v-if="specimen.locality">
        <el-icon><Location /></el-icon>
        {{ specimen.locality }}
      </p>
      <div class="card-footer">
        <span class="specimen-date">
          {{ formatDate(specimen.created_at) }}
        </span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import StatusTag from './StatusTag.vue'

const props = defineProps({
  specimen: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const primaryPhoto = computed(() => {
  if (props.specimen.photos && props.specimen.photos.length > 0) {
    return props.specimen.photos.find(p => p.is_primary) || props.specimen.photos[0]
  }
  return null
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const handleClick = () => {
  router.push(`/specimens/${props.specimen.id}`)
}
</script>

<style scoped>
.specimen-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.specimen-card:hover {
  transform: translateY(-4px);
}

.card-image {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 12px;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  color: #999;
}

.card-status {
  position: absolute;
  top: 8px;
  right: 8px;
}

.card-content {
  padding: 0 4px;
}

.specimen-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.specimen-no {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #909399;
}

.specimen-type,
.specimen-locality {
  margin: 0 0 6px 0;
  font-size: 13px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-footer {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid #ebeef5;
}

.specimen-date {
  font-size: 12px;
  color: #c0c4cc;
}
</style>
