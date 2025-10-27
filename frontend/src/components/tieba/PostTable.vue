<template>
  <div class="posts-table-container">
    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>正在加载帖子...</p>
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="posts.length === 0" class="empty-container">
        <div class="empty-icon">📝</div>
        <p class="empty-text">暂无帖子</p>
        <p class="empty-subtext">快来发布第一个帖子吧！</p>
      </div>
      
      <!-- 帖子列表表格 -->
      <div v-else class="table-wrapper">
        <table class="posts-table">
          <thead>
            <tr>
              <th class="title-column">帖子标题</th>
              <th class="author-column">作者</th>
              <th class="replies-column">回复数</th>
              <th class="time-column">最后回复时间</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="post in posts" 
              :key="post.id"
              class="post-row"
              @click="$emit('post-click', post)"
            >
              <td class="post-title-cell">
                <a 
                  href="#" 
                  class="post-title-link"
                  @click.prevent="$emit('post-click', post)"
                >
                  {{ post.title }}
                </a>
                <div class="post-tags">
                  <span 
                    v-for="tag in post.tags" 
                    :key="tag"
                    class="tag"
                    :class="getTagClass(tag)"
                  >
                    {{ tag }}
                  </span>
                </div>
              </td>
              <td class="author-cell">
                <div class="author-info">
                  <div class="author-avatar">{{ post.author.avatar }}</div>
                  <span class="author-name">{{ post.author.name }}</span>
                </div>
              </td>
              <td class="replies-cell">
                <span class="replies-count">{{ post.replies }}</span>
              </td>
              <td class="time-cell">
                <span class="time-text">{{ post.lastReplyTime }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// 定义Props
const props = defineProps({
  posts: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// 定义Emits
const emit = defineEmits(['post-click'])

// 标签样式映射
const tagStyles = {
  '精华': { class: 'tag-essence', color: '#FF6B35' },
  '攻略': { class: 'tag-guide', color: '#4CD964' },
  '讨论': { class: 'tag-discuss', color: '#007AFF' },
  '求助': { class: 'tag-help', color: '#FF9500' },
  '分享': { class: 'tag-share', color: '#5856D6' },
  '图片': { class: 'tag-image', color: '#FF2D55' },
  '视频': { class: 'tag-video', color: '#AF52DE' }
}

// 获取标签样式类
const getTagClass = (tag) => {
  return tagStyles[tag]?.class || 'tag-default'
}
</script>

<style scoped>
.posts-table-container {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  margin: 20px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007AFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
}

.empty-subtext {
  font-size: 14px;
  color: #999;
}

.table-wrapper {
  overflow-x: auto;
}

.posts-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.posts-table th {
  background: rgba(248, 249, 250, 0.8);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 16px 20px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
  white-space: nowrap;
}

.posts-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  background: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
}

.post-row:hover td {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.01);
  cursor: pointer;
}

.post-title-cell {
  max-width: 400px;
  min-width: 300px;
}

.post-title-link {
  color: #007AFF;
  text-decoration: none;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
  transition: all 0.3s ease;
  font-size: 14px;
  line-height: 1.4;
}

.post-title-link:hover {
  color: #0056CC;
  transform: translateX(4px);
}

.post-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  border: 1px solid;
}

.tag-essence {
  background: rgba(255, 107, 53, 0.1);
  color: #FF6B35;
  border-color: rgba(255, 107, 53, 0.3);
}

.tag-guide {
  background: rgba(76, 217, 100, 0.1);
  color: #4CD964;
  border-color: rgba(76, 217, 100, 0.3);
}

.tag-discuss {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
  border-color: rgba(0, 122, 255, 0.3);
}

.tag-help {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
  border-color: rgba(255, 149, 0, 0.3);
}

.tag-share {
  background: rgba(88, 86, 214, 0.1);
  color: #5856D6;
  border-color: rgba(88, 86, 214, 0.3);
}

.tag-image {
  background: rgba(255, 45, 85, 0.1);
  color: #FF2D55;
  border-color: rgba(255, 45, 85, 0.3);
}

.tag-video {
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
  border-color: rgba(175, 82, 222, 0.3);
}

.tag-default {
  background: rgba(102, 102, 102, 0.1);
  color: #666;
  border-color: rgba(102, 102, 102, 0.3);
}

.author-cell {
  min-width: 120px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007AFF, #5856D6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.author-name {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.replies-cell {
  text-align: center;
  min-width: 80px;
}

.replies-count {
  font-weight: 600;
  color: #007AFF;
  font-size: 14px;
}

.time-cell {
  min-width: 120px;
}

.time-text {
  font-size: 13px;
  color: #666;
}

/* 列宽调整 */
.title-column {
  width: 50%;
}

.author-column {
  width: 20%;
}

.replies-column {
  width: 15%;
}

.time-column {
  width: 15%;
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 0 16px;
  }
  
  .posts-table-container {
    margin: 16px 0;
    border-radius: 8px;
  }
  
  .posts-table th,
  .posts-table td {
    padding: 12px 16px;
  }
  
  .post-title-cell {
    min-width: 200px;
  }
  
  .author-cell {
    min-width: 100px;
  }
  
  .replies-cell {
    min-width: 60px;
  }
  
  .time-cell {
    min-width: 100px;
  }
  
  .author-avatar {
    width: 28px;
    height: 28px;
    font-size: 11px;
  }
  
  .author-name {
    font-size: 13px;
  }
  
  .post-title-link {
    font-size: 13px;
  }
  
  .tag {
    font-size: 10px;
    padding: 1px 6px;
  }
}

@media (max-width: 480px) {
  .posts-table th:nth-child(3),
  .posts-table td:nth-child(3) {
    display: none;
  }
  
  .title-column {
    width: 60%;
  }
  
  .author-column {
    width: 40%;
  }
}
</style>