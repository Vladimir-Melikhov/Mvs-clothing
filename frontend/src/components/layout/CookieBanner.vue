<template>
  <div v-if="!accepted" class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-6 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-50 transform transition-transform duration-500">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="text-sm text-gray-600">
        <p class="font-medium text-gray-900 mb-1">COOKIE NOTICE</p>
        <p>
          Мы используем файлы cookie и локальное хранилище для обеспечения работы сайта.
          Продолжая использование, вы соглашаетесь с нашей <router-link to="/privacy" class="underline hover:text-black">Политикой конфиденциальности</router-link>.
          Это демонстрационный сайт.
        </p>
      </div>
      <div class="flex gap-4 flex-shrink-0">
        <button
          @click="acceptCookies"
          class="px-8 py-3 bg-black text-white text-xs font-medium tracking-widest hover:bg-gray-800 transition-colors uppercase"
        >
          Принять
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const accepted = ref(true)

const acceptCookies = () => {
  localStorage.setItem('cookie_consent', 'true')
  accepted.value = true
}

onMounted(() => {
  const consent = localStorage.getItem('cookie_consent')
  if (!consent) {
    accepted.value = false
  }
})
</script>