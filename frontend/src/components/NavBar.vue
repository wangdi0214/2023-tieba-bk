<template>
  <nav class="navbar" :class="{ 'mobile-menu-open': isMobileMenuOpen }">
    <div class="nav-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-icon">🏮</span>
        百度贴吧
      </router-link>

      <!-- 汉堡菜单按钮（移动端） -->
      <button 
        class="nav-toggle" 
        :class="{ 'active': isMobileMenuOpen }"
        @click="toggleMobileMenu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- 导航链接 -->
      <ul class="nav-links" :class="{ 'active': isMobileMenuOpen }">
        <li>
          <router-link to="/" @click="closeMobileMenu">首页</router-link>
        </li>
        <li>
          <router-link to="/tiebas" @click="closeMobileMenu">贴吧</router-link>
        </li>
        <li>
          <router-link to="/posts" @click="closeMobileMenu">帖子</router-link>
        </li>
        <li>
          <router-link to="/messages" @click="closeMobileMenu">消息</router-link>
        </li>
        <li>
          <router-link to="/profile" @click="closeMobileMenu">我的</router-link>
        </li>
      </ul>

      <!-- 用户操作区域 -->
      <div class="nav-user">
        <template v-if="isLoggedIn">
          <div class="user-info">
            <img :src="userAvatar" alt="用户头像" class="user-avatar" />
            <span class="user-name">{{ userName }}</span>
          </div>
          <button class="btn btn-secondary" @click="handleLogout">退出</button>
        </template>
        <template v-else>
          <button class="btn btn-secondary" @click="handleLogin">登录</button>
          <button class="btn btn-primary" @click="handleRegister">注册</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMobileMenuOpen = ref(false)
const isLoggedIn = ref(false) // 模拟登录状态
const userName = ref('贴吧用户')
const userAvatar = ref('https://via.placeholder.com/40x40')

// 切换移动端菜单
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// 关闭移动端菜单
const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// 处理登录
const handleLogin = () => {
  console.log('跳转到登录页面')
  router.push('/login')
}

// 处理注册
const handleRegister = () => {
  console.log('跳转到注册页面')
  router.push('/register')
}

// 处理退出
const handleLogout = () => {
  isLoggedIn.value = false
  console.log('用户退出登录')
}

// 响应式处理
const handleResize = () => {
  if (window.innerWidth > 768) {
    closeMobileMenu()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  // 模拟登录状态
  isLoggedIn.value = Math.random() > 0.5
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid #e0e0e0;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ff6b6b;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 1.2em;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  cursor: pointer;
  padding: 0.5rem;
  background: none;
  border: none;
  z-index: 1001;
}

.nav-toggle span {
  width: 25px;
  height: 3px;
  background: #333;
  margin: 3px 0;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.nav-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.nav-toggle.active span:nth-child(2) {
  opacity: 0;
}

.nav-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
  align-items: center;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  position: relative;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
}

.nav-user {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 0.9rem;
  color: #333;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b, #ff9800);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-1px);
}

/* 移动端样式 */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .nav-toggle {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100vh;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    transition: left 0.3s ease;
    z-index: 1000;
  }

  .nav-links.active {
    left: 0;
  }

  .nav-links a {
    font-size: 1.25rem;
    padding: 1rem 2rem;
    width: 80%;
    text-align: center;
    border: 1px solid #e0e0e0;
    background: rgba(255, 255, 255, 0.9);
  }

  .nav-user {
    gap: 0.5rem;
  }

  .user-info {
    display: none;
  }

  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0.75rem 1rem;
  }

  .nav-user .btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>