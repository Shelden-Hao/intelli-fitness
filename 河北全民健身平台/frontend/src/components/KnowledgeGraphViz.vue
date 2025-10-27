<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps<{
  graphData: any
}>()

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value || !props.graphData) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  // 准备节点数据
  const nodes = props.graphData.nodes.map((node: any) => ({
    id: node.id,
    name: node.label,
    symbolSize: getNodeSize(node.type),
    category: getCategoryIndex(node.type),
    itemStyle: {
      color: getNodeColor(node.type)
    },
    label: {
      show: true,
      fontSize: 12
    }
  }))
  
  // 准备边数据
  const links = props.graphData.edges.map((edge: any) => ({
    source: edge.source,
    target: edge.target,
    label: {
      show: true,
      formatter: edge.label,
      fontSize: 10
    },
    lineStyle: {
      curveness: 0.3
    }
  }))
  
  // 分类
  const categories = [
    { name: '城市', itemStyle: { color: '#5470c6' } },
    { name: '设施', itemStyle: { color: '#91cc75' } },
    { name: '活动', itemStyle: { color: '#fac858' } },
    { name: '政策', itemStyle: { color: '#ee6666' } },
    { name: '其他', itemStyle: { color: '#73c0de' } }
  ]
  
  const option = {
    title: {
      text: '全民健身知识图谱',
      subtext: '基于Neo4j的时空知识表示',
      top: 'top',
      left: 'center'
    },
    tooltip: {
      formatter: (params: any) => {
        if (params.dataType === 'edge') {
          return `${params.data.source} → ${params.data.target}<br/>${params.data.label.formatter}`
        } else {
          return `${params.data.name}<br/>类型: ${params.data.category}`
        }
      }
    },
    legend: [{
      data: categories.map(c => c.name),
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    }],
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        name: '知识图谱',
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: links,
        categories: categories,
        roam: true,
        label: {
          position: 'right',
          formatter: '{b}'
        },
        labelLayout: {
          hideOverlap: true
        },
        scaleLimit: {
          min: 0.4,
          max: 2
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3,
          width: 2
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        },
        force: {
          repulsion: 1000,
          edgeLength: [100, 200],
          gravity: 0.1
        }
      }
    ]
  }
  
  chartInstance.setOption(option)
  
  // 响应式
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
}

const getNodeSize = (type: string) => {
  const sizeMap: Record<string, number> = {
    'City': 60,
    'Facility': 40,
    'Activity': 35,
    'Policy': 45,
    'Person': 30
  }
  return sizeMap[type] || 35
}

const getNodeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    'City': '#5470c6',
    'Facility': '#91cc75',
    'Activity': '#fac858',
    'Policy': '#ee6666',
    'Person': '#73c0de'
  }
  return colorMap[type] || '#73c0de'
}

const getCategoryIndex = (type: string) => {
  const categoryMap: Record<string, number> = {
    'City': 0,
    'Facility': 1,
    'Activity': 2,
    'Policy': 3
  }
  return categoryMap[type] || 4
}

onMounted(() => {
  initChart()
})

watch(() => props.graphData, () => {
  initChart()
}, { deep: true })
</script>

<template>
  <div ref="chartRef" class="graph-container"></div>
</template>

<style scoped>
.graph-container {
  width: 100%;
  height: 600px;
}
</style>
