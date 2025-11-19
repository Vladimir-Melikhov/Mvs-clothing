<template>
  <div class="min-h-screen flex items-center justify-center bg-white">
    <div class="text-center px-6">
      <h1 class="text-9xl font-light text-gray-900 mb-4" style="font-family: 'Times New Roman', Georgia, serif;">
        404
      </h1>
      <div class="divider-line w-24 mx-auto mb-8"></div>
      <h2 class="text-2xl font-light tracking-wide text-gray-900 mb-4">Page Not Found</h2>
      <p class="text-gray-600 mb-8 max-w-md mx-auto">
        The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
      </p>
      <router-link
        to="/"
        class="inline-block px-8 py-3 border border-black text-sm font-medium tracking-widest text-black bg-white hover:bg-black hover:text-white transition-all"
      >
        BACK TO HOME
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No script needed for this component
</script>

<style scoped>
.divider-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
}
</style>
