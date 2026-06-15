<template>
  <div class="dashboard">
    <div class="stats-cards">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon icon-blue">
            <el-icon :size="32"><Collection /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">标本总数</p>
            <p class="stat-value">{{ stats?.total_specimens || 0 }}</p>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon icon-green">
            <el-icon :size="32"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">已确认</p>
            <p class="stat-value">{{ stats?.confirmed_specimens || 0 }}</p>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon icon-orange">
            <el-icon :size="32"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">待鉴定</p>
            <p class="stat-value">{{ stats?.pending_specimens || 0 }}</p>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon icon-purple">
            <el-icon :size="32"><Picture /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">照片总数</p>
            <p class="stat-value">{{ stats?.total_photos || 0 }}</p>
          </div>
        </div>
      </el-card>
    </div>

    <div class="dashboard-content">
      <el-card class="recent-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">最近添加的标本</span>
            <el-button type="primary" link @click="goToSpecimens">
              查看全部
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </template>

        <div v-if="loading" class="loading-container">
          <el-icon class="loading-icon" :size="32"><Loading /></el-icon>
          <p>加载中...</p>
        </div>

        <div v-else-if="recentSpecimens.length === 0" class="empty-container">
          <el-empty description="暂无标本数据" :image-size="100">
            <el-button type="primary" @click="goToCreate">
              添加第一个标本
            </el-button>
          </el-empty>
        </div>

        <div v-else class="specimens-grid">
          <SpecimenCard
            v-for="specimen in recentSpecimens"
            :key="specimen.id"
            :specimen="specimen"
          />
        </div>
      </el-card>

      <el-card class="stats-chart-card" shadow="hover">
        <template #header>
          <span class="card-title">矿物类型分布</span>
        </template>
        <div ref="mineralChartRef" class="chart-container"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { getOverallStats } from '@/api/stats'
import { getSpecimens } from '@/api/specimen'
import SpecimenCard from '@/components/SpecimenCard.vue'

const router = useRouter()
const stats = ref(null)
const recentSpecimens = ref([])
const loading = ref(true)
const mineralChartRef = ref(null)
let mineralChart = null

const loadStats = async () => {
  try {
    const response = await getOverallStats()
    stats.value = response.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentSpecimens = async () => {
  try {
    const response = await getSpecimens({ page: 1, page_size: 6 })
    recentSpecimens.value = response.data.items
  } catch (error) {
    console.error('加载最近标本失败:', error)
  } finally {
    loading.value = false
  }
}

const initMineralChart = () => {
  if (!mineralChartRef.value || !stats.value?.mineral_type_distribution) return

  mineralChart = echarts.init(mineralChartRef.value)
  
  const data = stats.value.mineral_type_distribution
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          value: item.count,
          name: item.mineral_type
        }))
      }
    ]
  }

  mineralChart.setOption(option)
}

const goToSpecimens = () => {
  router.push('/specimens')
}

const goToCreate = () => {
  router.push('/specimens/create')
}

const handleResize = () => {
  mineralChart?.resize()
}

onMounted(async () => {
  await Promise.all([loadStats(), loadRecentSpecimens()])
  await nextTick()
  initMineralChart()
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 12px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.icon-blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.icon-green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.icon-orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.icon-purple {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-label {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #909399;
}

.stat-value {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
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

.specimens-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.loading-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.chart-container {
  width: 100%;
  height: 350px;
}

@media (max-width: 1200px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}
</style>
