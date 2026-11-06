<template>
  <div class="chart-wrapper">
    <h4 class="title">{{ title }}</h4>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent])

const props = defineProps<{
  title: string
  x_field: string
  y_field: string
  data: any[]
}>()

const option = computed(() => {
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: props.data.map(item => item[props.x_field]),
      axisLabel: { interval: 0, rotate: 30, fontSize: 10 }
    },
    yAxis: { type: 'value' },
    series: [
      {
        type: 'bar',
        data: props.data.map(item => item[props.y_field]),
        itemStyle: { color: '#1989fa' }
      }
    ]
  }
})
</script>

<style scoped>
.chart-wrapper { background: #fff; border-radius: 8px; padding: 12px; margin-top: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.title { margin: 0 0 10px 0; font-size: 14px; color: #333; }
.chart { height: 280px; width: 100%; }
</style>
