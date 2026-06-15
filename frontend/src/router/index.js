import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表板' }
      },
      {
        path: 'specimens',
        name: 'SpecimenList',
        component: () => import('@/views/specimen/List.vue'),
        meta: { title: '标本列表' }
      },
      {
        path: 'specimens/:id',
        name: 'SpecimenDetail',
        component: () => import('@/views/specimen/Detail.vue'),
        meta: { title: '标本详情' }
      },
      {
        path: 'specimens/create',
        name: 'SpecimenCreate',
        component: () => import('@/views/specimen/Form.vue'),
        meta: { title: '新增标本' }
      },
      {
        path: 'specimens/:id/edit',
        name: 'SpecimenEdit',
        component: () => import('@/views/specimen/Form.vue'),
        meta: { title: '编辑标本' }
      },
      {
        path: 'identification',
        name: 'IdentificationList',
        component: () => import('@/views/identification/List.vue'),
        meta: { title: '鉴定管理', requiresAdmin: true }
      },
      {
        path: 'stats',
        name: 'Stats',
        component: () => import('@/views/stats/Index.vue'),
        meta: { title: '统计分析' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
