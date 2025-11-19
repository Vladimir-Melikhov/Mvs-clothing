import { createRouter, createWebHistory } from 'vue-router'
import { getAccessToken } from '@/services/api'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { guest: true },
    },
    {
      path: '/password-reset',
      name: 'password-reset',
      component: () => import('@/views/auth/PasswordResetView.vue'),
      meta: { guest: true },
    },
    {
      path: '/password-reset/confirm',
      name: 'password-reset-confirm',
      component: () => import('@/views/auth/PasswordResetConfirmView.vue'),
      meta: { guest: true },
    },
    {
      path: '/email/verify',
      name: 'email-verify',
      component: () => import('@/views/auth/EmailVerifyView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/profile/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile/edit',
      name: 'profile-edit',
      component: () => import('@/views/profile/ProfileEditView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile/change-password',
      name: 'change-password',
      component: () => import('@/views/profile/ChangePasswordView.vue'),
      meta: { requiresAuth: true },
    },
    // Products routes
    {
      path: '/products',
      name: 'products',
      component: () => import('@/views/products/ProductsView.vue'),
    },
    {
      path: '/products/:slug',
      name: 'product-detail',
      component: () => import('@/views/products/ProductDetailView.vue'),
    },
    // Cart route
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/cart/CartView.vue'),
      meta: { requiresAuth: true },
    },
    // Orders routes
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('@/views/orders/CheckoutView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('@/views/orders/OrdersView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/orders/:id',
      name: 'order-detail',
      component: () => import('@/views/orders/OrderDetailView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!getAccessToken()

  // Redirect to home if authenticated user tries to access guest pages
  if (to.meta.guest && isAuthenticated) {
    next({ name: 'home' })
  }
  // Redirect to login if unauthenticated user tries to access protected pages
  else if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  }
  // Allow navigation
  else {
    next()
  }
})

export default router