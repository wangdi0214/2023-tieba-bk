<template>
  <div class="pagination-container">
    <div class="pagination-info">
      <span class="info-text">
        共 {{ totalItems }} 条记录，第 {{ currentPage }}/{{ totalPages }} 页
      </span>
    </div>
    
    <div class="pagination-controls">
      <!-- 第一页按钮 -->
      <button 
        class="pagination-btn first-btn"
        :disabled="currentPage <= 1"
        @click="goToPage(1)"
      >
        ««
      </button>
      
      <!-- 上一页按钮 -->
      <button 
        class="pagination-btn prev-btn"
        :disabled="currentPage <= 1"
        @click="goToPage(currentPage - 1)"
      >
        «
      </button>
      
      <!-- 页码按钮 -->
      <template v-for="page in visiblePages" :key="page">
        <button 
          v-if="page === '...'"
          class="pagination-btn ellipsis"
          disabled
        >
          ...
        </button>
        <button 
          v-else
          class="pagination-btn page-btn"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>
      
      <!-- 下一页按钮 -->
      <button 
        class="pagination-btn next-btn"
        :disabled="currentPage >= totalPages"
        @click="goToPage(currentPage + 1)"
      >
        »
      </button>
      
      <!-- 最后一页按钮 -->
      <button 
        class="pagination-btn last-btn"
        :disabled="currentPage >= totalPages"
        @click="goToPage(totalPages)"
      >
        »»
      </button>
    </div>
    
    <!-- 跳转输入框 -->
    <div class="pagination-jump">
      <span class="jump-text">跳转到</span>
      <input 
        v-model.number="jumpPage"
        type="number"
        min="1"
        :max="totalPages"
        class="jump-input"
        @keyup.enter="handleJump"
      />
      <span class="jump-text">页</span>
      <button 
        class="jump-btn"
        @click="handleJump"
        :disabled="!isValidJumpPage"
      >
        确定
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue'

// 定义Props
const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
    default: 1
  },
  totalPages: {
    type: Number,
    required: true,
    default: 1
  },
  totalItems: {
    type: Number,
    required: true,
    default: 0
  },
  maxVisiblePages: {
    type: Number,
    default: 5
  }
})

// 定义Emits
const emit = defineEmits(['page-change'])

// 跳转页码
const jumpPage = ref('')

// 计算可见页码
const visiblePages = computed(() => {
  const pages = []
  const { currentPage, totalPages, maxVisiblePages } = props
  
  if (totalPages <= maxVisiblePages) {
    // 如果总页数小于等于最大可见页数，显示所有页码
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i)
    }
  } else {
    // 计算起始和结束页码
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2))
    let endPage = startPage + maxVisiblePages - 1
    
    if (endPage > totalPages) {
      endPage = totalPages
      startPage = Math.max(1, endPage - maxVisiblePages + 1)
    }
    
    // 添加第一页和省略号
    if (startPage > 1) {
      pages.push(1)
      if (startPage > 2) {
        pages.push('...')
      }
    }
    
    // 添加中间页码
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }
    
    // 添加最后一页和省略号
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pages.push('...')
      }
      pages.push(totalPages)
    }
  }
  
  return pages
})

// 验证跳转页码是否有效
const isValidJumpPage = computed(() => {
  const page = parseInt(jumpPage.value)
  return !isNaN(page) && page >= 1 && page <= props.totalPages && page !== props.currentPage
})

// 跳转到指定页码
const goToPage = (page) => {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('page-change', page)
  }
}

// 处理跳转
const handleJump = () => {
  if (isValidJumpPage.value) {
    goToPage(parseInt(jumpPage.value))
    jumpPage.value = ''
  }
}

// 监听当前页码变化，重置跳转输入框
watch(() => props.currentPage, () => {
  jumpPage.value = ''
})
</script>

<style scoped>
.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 8px;
  margin: 20px 0;
  border: 1px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 16px;
}

.pagination-info {
  flex: 1;
  min-width: 200px;
}

.info-text {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.pagination-controls {
  display: flex;
  gap: 4px;
  align-items: center;
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.pagination-btn:hover:not(:disabled) {
  background: #007AFF;
  color: white;
  border-color: #007AFF;
  transform: translateY(-1px);
}

.pagination-btn.active {
  background: #007AFF;
  color: white;
  border-color: #007AFF;
}

.pagination-btn:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
  border-color: #e0e0e0;
}

.pagination-btn.ellipsis {
  background: transparent;
  border: none;
  cursor: default;
}

.pagination-btn.ellipsis:hover {
  background: transparent;
  color: #333;
  transform: none;
}

.pagination-jump {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 200px;
  justify-content: flex-end;
}

.jump-text {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.jump-input {
  width: 60px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  text-align: center;
  transition: border-color 0.3s;
}

.jump-input:focus {
  outline: none;
  border-color: #007AFF;
}

.jump-btn {
  padding: 8px 16px;
  border: 1px solid #007AFF;
  background: #007AFF;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.jump-btn:hover:not(:disabled) {
  background: #0056CC;
  border-color: #0056CC;
  transform: translateY(-1px);
}

.jump-btn:disabled {
  background: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
  transform: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .pagination-container {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .pagination-info {
    text-align: center;
  }
  
  .pagination-controls {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .pagination-jump {
    justify-content: center;
  }
  
  .pagination-btn {
    min-width: 36px;
    height: 36px;
    font-size: 13px;
    padding: 6px 10px;
  }
  
  .jump-input {
    width: 50px;
    padding: 6px 10px;
  }
  
  .jump-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .pagination-controls {
    gap: 2px;
  }
  
  .pagination-btn {
    min-width: 32px;
    height: 32px;
    font-size: 12px;
    padding: 4px 8px;
  }
  
  .first-btn,
  .last-btn {
    display: none;
  }
  
  .jump-input {
    width: 40px;
    padding: 4px 8px;
  }
  
  .jump-btn {
    padding: 4px 8px;
    font-size: 12px;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .pagination-btn:hover:not(:disabled) {
    transform: none;
  }
  
  .pagination-btn:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  .jump-btn:hover:not(:disabled) {
    transform: none;
  }
  
  .jump-btn:active:not(:disabled) {
    transform: scale(0.95);
  }
}
</style>