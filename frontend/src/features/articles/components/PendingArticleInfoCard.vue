<script setup>
import { ref } from "vue";
import { useToast } from "vue-toastification";
import {RouterLink, useRouter} from "vue-router";

const router = useRouter();

const props = defineProps({
  article: {
    type: Object,
    required: true,
  }
})

</script>

<template>
  <div class="flex flex-col gap-2 p-4 w-full bg-white rounded-lg border-0 shadow items-start">
    <!-- Title -->
    <router-link
      :to="{ name: 'article-moderation', params: { id: article.id } }"
      class="link text-[20px] font-semibold"
    >
      <h3 class="link text-lg font-semibold truncate">
        {{ article.title }}
      </h3>
    </router-link>

    <!-- Meta -->
    <span>
      Created:
      {{ new Date(article.created_at).toLocaleString() }}
    </span>
  </div>
</template>

<style scoped>

</style>