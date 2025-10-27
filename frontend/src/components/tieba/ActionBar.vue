<template>
  <div class="action-bar">
    <div class="container">
      <!-- 左侧操作按钮 -->
      <div class="action-buttons">
        <button 
          class="btn btn-primary"
          @click="$emit('create-post')"
        >
          <span class="btn-icon">+</span>
          发帖
        </button>
        <button 
          class="btn btn-secondary"
          :class="{ active: isFollowed }"
          @click="$emit('follow')"
        >
          <span class="btn-icon">{{ isFollowed ? '✓' : '☆' }}</span>
          {{ isFollowed ? '已关注' : '关注贴吧' }}
        </button>
        <button 
          class="btn btn-secondary"
          :class="{ active: isMember }"
          @click="$emit('join')"
        >
          <span class="btn-icon">{{ isMember ? '✓' : '👑' }}</span>
          {{ isMember ? '已加入' : '加入会员' }}
        </button>
      </div>
      
      <!-- 右侧搜索框 -->
      <div class="search-bar">
        <div class="search-input-container">
          <input 
            v-model="searchKeyword"
            type="text"
            placeholder="搜索本吧内容..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <button 
            class="search-btn"
            @click="handleSearch"
          >
            <span class="search-icon">🔍</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

// 定义Props
const props = defineProps({
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
const emit = defineEmits(['create-post', 'follow', 'join', 'search'])

// 搜索关键词
const searchKeyword = ref('')

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    emit('search', searchKeyword.value.trim())
  }
}
</script>

<style scoped>
.action-bar {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 16px 0;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  white-space: nowrap;
}

.btn-primary {
  background: linear-gradient(135deg, #007AFF, #5856D6);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.8);
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #007AFF;
  transform: translateY(-1px);
}

.btn-secondary.active {
  background: #007AFF;
  color: white;
  border-color: #007AFF;
}

.btn-icon {
  font-size: 16px;
  font-weight: bold;
}

.search-bar {
  flex: 1;
  max-width: 400px;
}

.search-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 12px 50px 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #007AFF;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
  background: rgba(255, 255, 255, 1);
}

.search-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background: rgba(0, 122, 255, 0.1);
}

.search-icon {
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    gap: 16px;
    padding: 0 16px;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: center;
  }
  
  .search-bar {
    width: 100%;
    max-width: none;
  }
  
  .btn {
    flex: 1;
    justify-content: center;
    min-width: 0;
  }
}

@media (max-width: 480px) {
  .action-buttons {
    flex-direction: column;
    gap: 8px;
  }
  
  .btn {
    width: 100%;
  }
  
  .search-input {
    padding: 10px 45px 10px 12px;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .btn:hover {
    transform: none;
  }
  
  .btn:active {
    transform: scale(0.98);
  }
}
</style>