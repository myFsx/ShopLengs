<template>
  <div class="app-container">
    <div class="header">ShopLens</div>
    
    <div class="content">
      <div v-if="loading" style="text-align: center; padding: 20px; color: #666;">正在查询数据...</div>
      <ChartBlock 
        v-if="chartData" 
        :title="chartData.title"
        :x_field="chartData.x_field"
        :y_field="chartData.y_field"
        :data="chartData.data"
      />
    </div>

    <div class="footer">
      <van-field v-model="inputText" placeholder="如：近一周销量排行" @keyup.enter="sendMessage" />
      <van-button type="primary" block @click="sendMessage" :loading="loading">发送</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import ChartBlock from './components/ChartBlock.vue'

const inputText = ref('近一周销量排行')
const loading = ref(false)
const chartData = ref<any>(null)

// 注意：手机测试时，这里填电脑的局域网 IP（如 http://192.168.1.5:8000/api/chat）
const API_URL = 'https://shop-lens-api.fly.dev/api/chat'

const sendMessage = async () => {
  if (!inputText.value) return
  loading.value = true
  chartData.value = null
  
  try {
    const res = await axios.post(API_URL, {
      message: inputText.value,
      session_id: 'test-session'
    })
    chartData.value = res.data
  } catch (err) {
    alert('请求失败，请检查后端是否启动')
  } finally {
    loading.value = false
  }
}
</script>

<style>
body { margin: 0; background-color: #f7f8fa; font-family: sans-serif; }
.app-container { display: flex; flex-direction: column; height: 100vh; }
.header { background: #1989fa; color: white; padding: 16px; text-align: center; font-weight: bold; }
.content { flex: 1; padding: 16px; overflow-y: auto; }
.footer { background: white; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
</style>
