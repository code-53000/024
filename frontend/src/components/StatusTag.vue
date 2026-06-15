<template>
  <el-tag :type="tagType" :effect="effect">
    {{ statusText }}
  </el-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  effect: {
    type: String,
    default: 'light'
  }
})

const statusMap = {
  pending: { text: '待鉴定', type: 'warning' },
  confirmed: { text: '已确认', type: 'success' },
  disputed: { text: '有争议', type: 'danger' }
}

const statusText = computed(() => {
  return statusMap[props.status]?.text || props.status
})

const tagType = computed(() => {
  return statusMap[props.status]?.type || 'info'
})
</script>
