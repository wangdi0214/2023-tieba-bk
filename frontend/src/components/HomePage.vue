<template>
  <div class="home-page">
    <!-- 导航栏 -->
    <NavBar />
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 轮播图区域 -->
      <section class="carousel-section">
        <Carousel />
      </section>

      <!-- 搜索框区域 -->
      <section class="search-section">
        <div class="search-container">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="搜索贴吧、帖子、用户..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <button class="search-btn" @click="handleSearch">
            🔍 搜索
          </button>
        </div>
      </section>

      <!-- 热门贴吧网格 -->
      <section class="tieba-section">
        <TiebaGrid />
      </section>

      <!-- 热门帖子列表 -->
      <section class="posts-section">
        <PostList />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from './NavBar.vue'
import Carousel from './Carousel.jsx'
import TiebaGrid from './TiebaGrid.jsx'
import PostList from './PostList.vue'

const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    console.log('搜索关键词:', searchQuery.value)
    // 这里可以添加搜索逻辑
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.carousel-section {
  margin-bottom: 2rem;
}

.search-section {
  margin-bottom: 2rem;
}

.search-container {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 25px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.search-input {
  flex: 1;
  padding: 12px 20px;
  border: none;
  font-size: 16px;
  outline: none;
  background: transparent;
  color: #333;
  min-height: 44px;
}

.search-input::placeholder {
  color: #999;
}

.search-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff9800);
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 44px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-btn:hover {
  background: linear-gradient(135deg, #ff9800, #ff6b6b);
  transform: translateY(-1px);
}

.tieba-section {
  margin-bottom: 2rem;
}

.posts-section {
  margin-bottom: 2rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .search-container {
    max-width: 100%;
    border-radius: 12px;
  }
  
  .search-input {
    font-size: 14px;
    padding: 10px 16px;
  }
  
  .search-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .search-container {
    flex-direction: column;
    border-radius: 8px;
  }
  
  .search-input {
    border-bottom: 1px solid #e0e0e0;
    border-radius: 0;
  }
  
  .search-btn {
    border-radius: 0 0 8px 8px;
  }
}
</style>