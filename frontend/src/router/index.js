import { createRouter, createWebHistory } from 'vue-router'

// 页面组件
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import TiebaList from '@/pages/tieba/TiebaList.vue'
import TiebaDetail from '@/pages/tieba/TiebaDetail.vue'
import PostDetail from '@/pages/post/PostDetail.vue'
import UserProfile from '@/pages/user/UserProfile.vue'
import SearchResult from '@/pages/search/SearchResult.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/tieba',
    name: 'TiebaList',
    component: TiebaList
  },
  {
    path: '/tieba/:id',
    name: 'TiebaDetail',
    component: TiebaDetail
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetail
  },
  {
    path: '/user/:id',
    name: 'UserProfile',
    component: UserProfile
  },
  {
    path: '/search',
    name: 'SearchResult',
    component: SearchResult
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查用户登录状态
  const token = localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router