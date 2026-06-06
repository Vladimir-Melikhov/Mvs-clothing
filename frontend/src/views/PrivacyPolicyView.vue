<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader variant="dark" />
    <div class="max-w-4xl mx-auto px-6 py-12 mt-20">
      <h1 class="text-3xl font-light tracking-[0.3em] text-gray-900 mb-8" style="font-family: Georgia, serif;">
        Privacy Policy
      </h1>
      
      <div class="bg-white border border-gray-200 p-8 space-y-6 text-sm text-gray-600 leading-relaxed">
        <section>
          <h2 class="text-lg font-medium text-gray-900 mb-3">1. Введение</h2>
          <p>Это демонстрационный сайт (портфолио). Все данные, которые вы вводите (email, имя, адрес), обрабатываются исключительно в целях демонстрации функционала и могут быть удалены в любое время.</p>
        </section>

        <section>
          <h2 class="text-lg font-medium text-gray-900 mb-3">2. Сбор данных</h2>
          <p>Мы собираем только те данные, которые необходимы для работы демо-версии магазина: email для входа, имя для профиля и адрес для оформления тестового заказа.</p>
        </section>

        <section>
          <h2 class="text-lg font-medium text-gray-900 mb-3">3. Безопасность</h2>
          <p>Мы принимаем меры предосторожности для защиты данных, однако, так как это демо-проект, мы не рекомендуем использовать реальные пароли, которые вы используете на других сервисах.</p>
        </section>
        
        <router-link to="/" class="inline-block mt-4 text-black underline hover:text-gray-600 transition-colors">
          Вернуться на главную
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
</script>