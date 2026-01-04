<template>
  <div class="city-card group cursor-pointer" @click="$emit('select', city)">
    <!-- 图片 -->
    <div class="relative h-52 overflow-hidden rounded-xl">
      <img 
        :src="city.image" 
        :alt="city.name"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
      />
      <!-- 渐变遮罩 -->
      <div class="absolute inset-0 bg-gradient-to-t from-space-900 via-space-900/20 to-transparent"></div>
      
      <!-- 内容覆盖在图片上 -->
      <div class="absolute bottom-0 left-0 right-0 p-5">
        <h3 class="text-xl font-medium text-white mb-2">{{ city.name }}</h3>
        <p class="text-gray-400 text-sm line-clamp-1 mb-3">{{ city.description }}</p>
        <div class="flex flex-wrap gap-2">
          <span v-for="tag in city.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  city: { type: Object, required: true }
})

defineEmits(['select'])
</script>

<style scoped>
.city-card {
  @apply relative rounded-xl overflow-hidden;
  @apply transition-all duration-500;
  @apply hover:-translate-y-1;
}

.tag {
  @apply px-2 py-0.5 text-xs rounded;
  @apply bg-white/10 text-gray-300;
}
</style>
