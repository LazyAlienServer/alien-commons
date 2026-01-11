<script setup>
import { ArticleReader } from '@/features/articles/components'
import { onMounted, ref } from "vue";
import { getTheSourceArticle } from "@/features/articles/api";
import { useRoute } from "vue-router";

const route = useRoute();

const title = ref('')
const content = ref({ type: 'doc', content: [] })

onMounted(async () => {
  const response = await getTheSourceArticle(route.params.id)

  title.value = response.data.title
  content.value = response.data.content
})
</script>

<template>

</template>