<template>
  <div class="city-card group cursor-pointer" @click="$emit('select', city)">
    <!-- 图片 -->
    <div class="relative h-52 overflow-hidden rounded-xl">
      <img 
        :src="city.image" 
        :alt="city.name"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
      />
      
      <!-- ✨ 加强版渐变遮罩 - 保证任何模式下文字都可读 -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-black/10"></div>
      
      <!-- hover 时的光效 -->
      <div class="absolute inset-0 bg-gradient-to-br from-nebula-500/0 to-nebula-600/0 group-hover:from-nebula-500/10 group-hover:to-nebula-600/20 transition-all duration-500"></div>
      
      <!-- 内容覆盖在图片上 -->
      <div class="absolute bottom-0 left-0 right-0 p-5">
        <h3 class="text-xl font-medium text-white mb-2 drop-shadow-lg">{{ city.name }}</h3>
        <p class="text-gray-200 text-sm line-clamp-1 mb-3 drop-shadow">{{ city.description }}</p>
        <div class="flex flex-wrap gap-2">
          <span v-for="tag in city.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>

      <!-- 角标装饰 -->
      <div class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <span class="text-white/60 text-lg">→</span>
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
  @apply hover:shadow-xl hover:shadow-nebula-500/10;
}

.tag {
  @apply px-2.5 py-1 text-xs rounded-full;
  @apply bg-white/20 text-white backdrop-blur-sm;
  @apply border border-white/10;
}
</style>
