<template>
  <div class="photo-upload">
    <el-upload
      :action="uploadUrl"
      :headers="headers"
      multiple
      :auto-upload="false"
      :on-change="handleChange"
      :on-remove="handleRemove"
      :file-list="fileList"
      accept="image/*"
      drag
      :disabled="uploading"
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">
        将图片拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持 jpg/png/gif 格式，单张图片不超过 10MB
        </div>
      </template>
    </el-upload>

    <div v-if="previewList.length > 0" class="preview-list">
      <div
        v-for="(file, index) in previewList"
        :key="index"
        class="preview-item"
      >
        <img :src="file.url" :alt="file.name" />
        <div class="preview-actions">
          <el-button
            size="small"
            type="primary"
            :icon="Star"
            @click="setPrimary(index)"
            :disabled="primaryIndex === index"
          >
            设为封面
          </el-button>
          <el-button
            size="small"
            type="danger"
            :icon="Delete"
            @click="removePreview(index)"
          >
            删除
          </el-button>
        </div>
        <div v-if="primaryIndex === index" class="primary-badge">
          <el-icon><Star /></el-icon>
          封面
        </div>
      </div>
    </div>

    <div class="upload-actions">
      <el-button
        type="primary"
        :icon="Upload"
        :loading="uploading"
        :disabled="previewList.length === 0"
        @click="handleUpload"
      >
        {{ uploading ? '上传中...' : '开始上传' }}
      </el-button>
      <el-button
        :icon="RefreshRight"
        :disabled="previewList.length === 0 || uploading"
        @click="clearAll"
      >
        清空
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { bulkUploadPhotos, setPrimaryPhoto } from '@/api/photo'

const props = defineProps({
  specimenId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['upload-success'])

const userStore = useUserStore()
const fileList = ref([])
const previewList = ref([])
const uploading = ref(false)
const primaryIndex = ref(0)

const uploadUrl = computed(() => {
  return `/api/v1/photos/specimen/${props.specimenId}/bulk`
})

const headers = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

const handleChange = (file, files) => {
  if (file.raw) {
    const isImage = file.raw.type.startsWith('image/')
    const isLt10M = file.raw.size / 1024 / 1024 < 10

    if (!isImage) {
      ElMessage.error('只能上传图片文件!')
      return
    }
    if (!isLt10M) {
      ElMessage.error('图片大小不能超过 10MB!')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      previewList.value.push({
        name: file.name,
        url: e.target.result,
        raw: file.raw
      })
    }
    reader.readAsDataURL(file.raw)
  }
}

const handleRemove = (file, files) => {
  const index = previewList.value.findIndex(p => p.name === file.name)
  if (index > -1) {
    previewList.value.splice(index, 1)
    if (primaryIndex.value >= previewList.value.length) {
      primaryIndex.value = Math.max(0, previewList.value.length - 1)
    }
  }
}

const removePreview = (index) => {
  previewList.value.splice(index, 1)
  fileList.value = fileList.value.filter((_, i) => i !== index)
  if (primaryIndex.value >= previewList.value.length) {
    primaryIndex.value = Math.max(0, previewList.value.length - 1)
  }
}

const setPrimary = (index) => {
  primaryIndex.value = index
}

const handleUpload = async () => {
  if (previewList.value.length === 0) {
    ElMessage.warning('请先选择要上传的图片')
    return
  }

  uploading.value = true
  try {
    const files = previewList.value.map(p => p.raw)
    const response = await bulkUploadPhotos(props.specimenId, files)

    if (primaryIndex.value < response.data.uploaded.length) {
      const primaryPhoto = response.data.uploaded[primaryIndex.value]
      await setPrimaryPhoto(primaryPhoto.id)
    }

    ElMessage.success(`成功上传 ${response.data.uploaded.length} 张图片`)
    emit('upload-success', response.data.uploaded)
    clearAll()
  } catch (error) {
    console.error('上传失败:', error)
  } finally {
    uploading.value = false
  }
}

const clearAll = () => {
  fileList.value = []
  previewList.value = []
  primaryIndex.value = 0
}
</script>

<style scoped>
.photo-upload {
  width: 100%;
}

.preview-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
  margin: 16px 0;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #ebeef5;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 4px;
  padding: 8px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  opacity: 0;
  transition: opacity 0.2s;
}

.preview-item:hover .preview-actions {
  opacity: 1;
}

.primary-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: #409eff;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.upload-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}
</style>
