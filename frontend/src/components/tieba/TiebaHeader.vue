<template>
  <div class="tieba-header">
    <div class="container">
      <div class="tieba-info">
        <!-- 贴吧头像 -->
        <div class="tieba-avatar">
          <span class="avatar-text">{{ tieba.avatar }}</span>
        </div>
        
        <!-- 贴吧详细信息 -->
        <div class="tieba-details">
          <h1 class="tieba-name">{{ tieba.name }}</h1>
          <p class="tieba-description">{{ tieba.description }}</p>
          
          <!-- 统计数据 -->
          <div class="tieba-stats">
            <div class="stat-item">
              <span class="stat-icon">👥</span>
              <span class="stat-value">{{ formatNumber(tieba.stats.members) }}成员</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">📝</span>
              <span class="stat-value">{{ formatNumber(tieba.stats.posts) }}帖子</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🌡</span>
              <span class="stat-value">热度值:{{ tieba.stats.heat }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="header-actions">
        <button 
          class="action-btn follow-btn"
          :class="{ followed: isFollowed }"
          @click="$emit('follow')"
        >
          {{ isFollowed ? '已关注' : '关注' }}
        </button>
        <button 
          class="action-btn join-btn"
          :class="{ joined: isMember }"
          @click="$emit('join')"
        >
          {{ isMember ? '已加入' : '加入会员' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// 定义Props
const props = defineProps({
  tieba: {
    type: Object,
    required: true,
    default: () => ({
      id: '',
      name: '',
      avatar: '',
      description: '',
      stats: {
        members: 0,
        posts: 0,
        heat: 0
      }
    })
  },
  isFollowed: {
    type: Boolean,
    default: false
  },
  isMember: {
    type: Boolean,
    default: false
  }
})

// 定义Emits
const emit = defineEmits(['follow', 'join'])

// 格式化数字显示
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}
</script>

<style scoped>
.tieba-header {
  background: linear-gradient(135deg, 
    rgba(102, 126, 234, 0.9) 0%, 
    rgba(118, 75, 162, 0.9) 50%, 
    rgba(240, 147, 251, 0.9) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: white;
  padding: 40px 0 30px;
  position: relative;
  overflow: hidden;
}

.tieba-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="25" cy="25" r="2" fill="rgba(255,255,255,0.1)"><animate attributeName="r" values="1;3;1" dur="4s" repeatCount="indefinite"/></circle><circle cx="75" cy="75" r="1.5" fill="rgba(255,255,255,0.1)"><animate attributeName="r" values="0.5;2.5;0.5" dur="3s" repeatCount="indefinite" begin="1s"/></circle></svg>') repeat;
  animation: float 15s ease-in-out infinite;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.tieba-info {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 20px;
}

.tieba-avatar {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: #007AFF;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.avatar-text {
  background: linear-gradient(135deg, #007AFF, #5856D6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tieba-details {
  flex: 1;
}

.tieba-name {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.tieba-description {
  opacity: 0.9;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  max-width: 600px;
}

.tieba-stats {
  display: flex;
  gap: 32px;
  font-size: 14px;
  opacity: 0.9;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.stat-icon {
  font-size: 16px;
}

.stat-value {
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.action-btn {
  padding: 10px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.follow-btn.followed {
  background: rgba(255, 255, 255, 0.9);
  color: #007AFF;
  border-color: rgba(255, 255, 255, 0.9);
}

.join-btn.joined {
  background: rgba(255, 255, 255, 0.9);
  color: #FF9500;
  border-color: rgba(255, 255, 255, 0.9);
}

/* 动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }
  
  .tieba-info {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .tieba-avatar {
    width: 60px;
    height: 60px;
    font-size: 20px;
  }
  
  .tieba-name {
    font-size: 24px;
  }
  
  .tieba-description {
    font-size: 14px;
  }
  
  .tieba-stats {
    justify-content: center;
    gap: 24px;
  }
  
  .header-actions {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .tieba-stats {
    flex-direction: column;
    gap: 12px;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>