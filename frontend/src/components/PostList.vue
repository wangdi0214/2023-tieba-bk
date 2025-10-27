<template>
  <div class="post-list">
    <div class="post-header">
      <h2 class="section-title">热门帖子</h2>
      <div class="filter-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="posts-container">
      <div 
        v-for="post in filteredPosts" 
        :key="post.id"
        class="post-card"
        @click="handlePostClick(post)"
      >
        <div class="post-header-info">
          <div class="author-info">
            <img :src="post.author.avatar" :alt="post.author.name" class="author-avatar" />
            <div class="author-details">
              <span class="author-name">{{ post.author.name }}</span>
              <span class="post-time">{{ post.time }}</span>
            </div>
          </div>
          <div class="post-meta">
            <span class="tieba-name">{{ post.tieba }}</span>
            <span class="post-views">👁 {{ post.views }}</span>
          </div>
        </div>

        <div class="post-content">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-excerpt">{{ post.content }}</p>
          
          <div v-if="post.images && post.images.length > 0" class="post-images">
            <img 
              v-for="(image, index) in post.images.slice(0, 3)" 
              :key="index"
              :src="image" 
              :alt="'图片' + (index + 1)"
              class="post-image"
            />
            <span v-if="post.images.length > 3" class="image-count">+{{ post.images.length - 3 }}</span>
          </div>
        </div>

        <div class="post-footer">
          <div class="post-stats">
            <button class="stat-btn" @click.stop="handleLike(post)">
              <span :class="['like-icon', { liked: post.liked }]">❤️</span>
              {{ post.likes }}
            </button>
            <button class="stat-btn" @click.stop="handleComment(post)">
              💬 {{ post.comments }}
            </button>
            <button class="stat-btn" @click.stop="handleShare(post)">
              🔗 分享
            </button>
          </div>
          
          <div class="post-tags">
            <span 
              v-for="tag in post.tags" 
              :key="tag"
              class="tag"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredPosts.length === 0" class="no-posts">
      <p>暂无帖子</p>
    </div>

    <div class="load-more-container">
      <button class="load-more-btn" @click="loadMorePosts">
        加载更多帖子
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 标签页数据
const tabs = [
  { id: 'hot', label: '热门' },
  { id: 'new', label: '最新' },
  { id: 'recommend', label: '推荐' }
]

const activeTab = ref('hot')

// 模拟帖子数据
const posts = ref([
  {
    id: 1,
    title: '【技术分享】Vue3 + React混合开发的最佳实践',
    content: '最近在项目中使用了Veaury框架进行Vue和React的混合开发，分享一些踩坑经验和最佳实践...',
    author: {
      name: '前端开发者',
      avatar: 'https://via.placeholder.com/40x40/667eea/ffffff?text=FD'
    },
    tieba: '编程',
    time: '2小时前',
    views: '1.2k',
    likes: 156,
    comments: 89,
    liked: false,
    tags: ['前端', 'Vue', 'React', '技术'],
    images: [
      'https://via.placeholder.com/200x120/667eea/ffffff?text=代码',
      'https://via.placeholder.com/200x120/764ba2/ffffff?text=架构'
    ]
  },
  {
    id: 2,
    title: '考研数学复习经验分享，从零基础到130+',
    content: '作为去年成功上岸的考研党，分享一下数学复习的时间规划和重点难点突破方法...',
    author: {
      name: '考研学长',
      avatar: 'https://via.placeholder.com/40x40/4facfe/ffffff?text=KS'
    },
    tieba: '考研',
    time: '5小时前',
    views: '3.4k',
    likes: 289,
    comments: 156,
    liked: true,
    tags: ['考研', '数学', '经验分享', '学习'],
    images: [
      'https://via.placeholder.com/200x120/4facfe/ffffff?text=数学'
    ]
  },
  {
    id: 3,
    title: '英雄联盟新版本英雄强度分析',
    content: '13.24版本更新后，各位置英雄强度发生了哪些变化？来看看最新的Tier List...',
    author: {
      name: '游戏达人',
      avatar: 'https://via.placeholder.com/40x40/f093fb/ffffff?text=GD'
    },
    tieba: '英雄联盟',
    time: '1天前',
    views: '8.7k',
    likes: 567,
    comments: 234,
    liked: false,
    tags: ['LOL', '游戏', '版本更新', '攻略'],
    images: [
      'https://via.placeholder.com/200x120/f093fb/ffffff?text=LOL',
      'https://via.placeholder.com/200x120/667eea/ffffff?text=英雄'
    ]
  },
  {
    id: 4,
    title: '周末美食探店：这家川菜馆真的绝了！',
    content: '发现一家宝藏川菜馆，人均50吃到撑，强烈推荐他们的水煮鱼和麻婆豆腐...',
    author: {
      name: '美食家',
      avatar: 'https://via.placeholder.com/40x40/43e97b/ffffff?text=FS'
    },
    tieba: '美食',
    time: '2天前',
    views: '2.1k',
    likes: 134,
    comments: 67,
    liked: false,
    tags: ['美食', '探店', '川菜', '推荐'],
    images: [
      'https://via.placeholder.com/200x120/43e97b/ffffff?text=美食',
      'https://via.placeholder.com/200x120/f5576c/ffffff?text=川菜',
      'https://via.placeholder.com/200x120/ffd89b/ffffff?text=餐厅'
    ]
  }
])

// 根据标签过滤帖子
const filteredPosts = computed(() => {
  // 这里可以根据activeTab实现不同的排序逻辑
  return posts.value
})

// 处理帖子点击
const handlePostClick = (post) => {
  console.log('查看帖子详情:', post.title)
  // 这里可以添加路由跳转逻辑
}

// 处理点赞
const handleLike = (post) => {
  post.liked = !post.liked
  post.likes += post.liked ? 1 : -1
  console.log(post.liked ? '点赞帖子:' : '取消点赞:', post.title)
}

// 处理评论
const handleComment = (post) => {
  console.log('评论帖子:', post.title)
  // 这里可以打开评论框或跳转到评论页面
}

// 处理分享
const handleShare = (post) => {
  console.log('分享帖子:', post.title)
  // 这里可以实现分享功能
}

// 加载更多帖子
const loadMorePosts = () => {
  console.log('加载更多帖子')
  // 这里可以实现分页加载逻辑
}
</script>

<style scoped>
.post-list {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.25rem;
}

.tab-btn {
  padding: 0.5rem 1.5rem;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: #666;
  transition: all 0.3s ease;
}

.tab-btn.active {
  background: linear-gradient(135deg, #ff6b6b, #ff9800);
  color: white;
}

.tab-btn:hover:not(.active) {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  border-color: #ff6b6b;
}

.post-header-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.post-time {
  font-size: 0.875rem;
  color: #999;
}

.post-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.tieba-name {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.post-views {
  font-size: 0.875rem;
  color: #999;
}

.post-content {
  margin-bottom: 1.5rem;
}

.post-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.post-excerpt {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-images {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  position: relative;
}

.post-image {
  width: 120px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.image-count {
  position: absolute;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.stat-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e0e0e0;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.875rem;
  color: #666;
  transition: all 0.3s ease;
}

.stat-btn:hover {
  background: rgba(255, 107, 107, 0.1);
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.like-icon.liked {
  color: #ff6b6b;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: rgba(255, 255, 255, 0.9);
  color: #666;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  border: 1px solid #e0e0e0;
}

.no-posts {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.load-more-container {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #f0f0f0;
}

.load-more-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff9800);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-list {
    padding: 1.5rem;
  }

  .post-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
    text-align: center;
  }

  .filter-tabs {
    justify-content: center;
  }

  .post-card {
    padding: 1.25rem;
  }

  .post-header-info {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .post-meta {
    align-items: flex-start;
    flex-direction: row;
    justify-content: space-between;
  }

  .post-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .post-stats {
    justify-content: center;
  }

  .post-tags {
    justify-content: center;
  }

  .post-image {
    width: 100px;
    height: 70px;
  }
}

@media (max-width: 480px) {
  .post-list {
    padding: 1rem;
  }

  .post-card {
    padding: 1rem;
  }

  .post-title {
    font-size: 1.1rem;
  }

  .post-excerpt {
    font-size: 0.9rem;
  }

  .stat-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .post-image {
    width: 80px;
    height: 60px;
  }
}
</style>