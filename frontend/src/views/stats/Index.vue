<template>
  <div class="stats-page">
    <div class="stats-overview">
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
          <div class="stat-icon icon-red">
            <el-icon :size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">有争议</p>
            <p class="stat-value">{{ stats?.disputed_specimens || 0 }}</p>
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

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon icon-cyan">
            <el-icon :size="32"><User /></el-icon>
          </div>
          <div class="stat-info">
            <p class="stat-label">矿物种类</p>
            <p class="stat-value">{{ stats?.mineral_type_count || 0 }}</p>
          </div>
        </div>
      </el-card>
    </div>

    <div class="charts-grid">
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <span class="card-title">矿物类型分布</span>
        </template>
        <div ref="mineralChartRef" class="chart-container"></div>
      </el-card>

      <el-card class="chart-card" shadow="hover">
        <template #header>
          <span class="card-title">晶系分布</span>
        </template>
        <div ref="crystalChartRef" class="chart-container"></div>
      </el-card>

      <el-card class="chart-card" shadow="hover">
        <template #header>
          <span class="card-title">鉴定状态分布</span>
        </template>
        <div ref="statusChartRef" class="chart-container"></div>
      </el-card>

      <el-card class="chart-card" shadow="hover">
        <template #header>
          <span class="card-title">获取方式分布</span>
        </template>
        <div ref="acquisitionChartRef" class="chart-container"></div>
      </el-card>

      <el-card class="chart-card chart-wide" shadow="hover">
        <template #header>
          <span class="card-title">产地分布（省份）</span>
        </template>
        <div ref="provinceChartRef" class="chart-container"></div>
      </el-card>

      <el-card class="chart-card chart-wide" shadow="hover">
        <template #header>
          <span class="card-title">月度新增趋势</span>
        </template>
        <div ref="trendChartRef" class="chart-container"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getOverallStats } from '@/api/stats'

const stats = ref(null)
const mineralChartRef = ref(null)
const crystalChartRef = ref(null)
const statusChartRef = ref(null)
const acquisitionChartRef = ref(null)
const provinceChartRef = ref(null)
const trendChartRef = ref(null)

let mineralChart = null
let crystalChart = null
let statusChart = null
let acquisitionChart = null
let provinceChart = null
let trendChart = null

const crystalSystemMap = {
  isometric: '等轴晶系',
  tetragonal: '四方晶系',
  orthorhombic: '斜方晶系',
  hexagonal: '六方晶系',
  trigonal: '三方晶系',
  monoclinic: '单斜晶系',
  triclinic: '三斜晶系',
  amorphous: '非晶质'
}

const acquisitionMap = {
  purchase: '购买',
  mining: '采集',
  gift: '赠送',
  trade: '交换',
  excavation: '发掘',
  other: '其他'
}

const statusMap = {
  pending: '待鉴定',
  confirmed: '已确认',
  disputed: '有争议'
}

const loadStats = async () => {
  try {
    const response = await getOverallStats()
    stats.value = response.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
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
      type: 'scroll',
      orient: 'vertical',
      right: '5%',
      top: 'center'
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      itemStyle: {
        borderRadius: 8,
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
          fontSize: 16,
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
    }]
  }

  mineralChart.setOption(option)
}

const initCrystalChart = () => {
  if (!crystalChartRef.value || !stats.value?.crystal_system_distribution) return

  crystalChart = echarts.init(crystalChartRef.value)
  const data = stats.value.crystal_system_distribution
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: '5%',
      top: 'center'
    },
    series: [{
      type: 'pie',
      radius: '60%',
      center: ['35%', '50%'],
      itemStyle: {
        borderRadius: 8
      },
      data: data.map(item => ({
        value: item.count,
        name: crystalSystemMap[item.crystal_system] || item.crystal_system
      }))
    }]
  }

  crystalChart.setOption(option)
}

const initStatusChart = () => {
  if (!statusChartRef.value || !stats.value?.identification_status_distribution) return

  statusChart = echarts.init(statusChartRef.value)
  const data = stats.value.identification_status_distribution
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '50%'],
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        position: 'outside',
        formatter: '{b}\n{d}%'
      },
      data: data.map(item => ({
        value: item.count,
        name: statusMap[item.status] || item.status,
        itemStyle: {
          color: item.status === 'confirmed' ? '#67c23a' : 
                 item.status === 'pending' ? '#e6a23c' : '#f56c6c'
        }
      }))
    }]
  }

  statusChart.setOption(option)
}

const initAcquisitionChart = () => {
  if (!acquisitionChartRef.value || !stats.value?.acquisition_method_distribution) return

  acquisitionChart = echarts.init(acquisitionChartRef.value)
  const data = stats.value.acquisition_method_distribution
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => acquisitionMap[item.method] || item.method),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [{
      type: 'bar',
      data: data.map(item => item.count),
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#83bff6' },
          { offset: 1, color: '#188df0' }
        ])
      }
    }]
  }

  acquisitionChart.setOption(option)
}

const initProvinceChart = () => {
  if (!provinceChartRef.value || !stats.value?.province_distribution) return

  provinceChart = echarts.init(provinceChartRef.value)
  const data = stats.value.province_distribution.slice(0, 15)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      minInterval: 1
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.province || '未知').reverse()
    },
    series: [{
      type: 'bar',
      data: data.map(item => item.count).reverse(),
      itemStyle: {
        borderRadius: [0, 4, 4, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#667eea' },
          { offset: 1, color: '#764ba2' }
        ])
      }
    }]
  }

  provinceChart.setOption(option)
}

const initTrendChart = () => {
  if (!trendChartRef.value || !stats.value?.monthly_trend) return

  trendChart = echarts.init(trendChartRef.value)
  const data = stats.value.monthly_trend
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map(item => item.month)
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [{
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      data: data.map(item => item.count),
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(102, 126, 234, 0.4)' },
          { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
        ])
      },
      lineStyle: {
        width: 3,
        color: '#667eea'
      },
      itemStyle: {
        color: '#667eea'
      }
    }]
  }

  trendChart.setOption(option)
}

const handleResize = () => {
  mineralChart?.resize()
  crystalChart?.resize()
  statusChart?.resize()
  acquisitionChart?.resize()
  provinceChart?.resize()
  trendChart?.resize()
}

onMounted(async () => {
  await loadStats()
  await nextTick()
  
  initMineralChart()
  initCrystalChart()
  initStatusChart()
  initAcquisitionChart()
  initProvinceChart()
  initTrendChart()
  
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.stats-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
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
  width: 56px;
  height: 56px;
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

.icon-red {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
}

.icon-purple {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.icon-cyan {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-label {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #909399;
}

.stat-value {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-card {
  border-radius: 12px;
}

.chart-wide {
  grid-column: span 2;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.chart-container {
  width: 100%;
  height: 350px;
}

@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-wide {
    grid-column: span 1;
  }
}
</style>
