<script setup>
import { ArticleReader } from '@/features/articles/components'
import { onMounted, ref } from "vue";
import {approveArticle, getArticleSnapshot, rejectArticle} from "@/features/articles/api";
import { useRoute } from "vue-router";

const route = useRoute();

const title = ref('')
const content = ref({ type: 'doc', content: [] })
const articleId = ref(null)

onMounted(async () => {
  const response = await getArticleSnapshot(route.params.id);

  title.value = response.data.title;
  content.value = response.data.content;
  articleId.value = response.data.article;
});

const approve = async () => {
  await approveArticle(articleId.value);
}
const reject = async () => {
  await rejectArticle(articleId.value);
}
</script>

<template>
  <div class="mainContainer">
    <button class="reviewButtons" @click="approve">Approve</button>
    <button class="reviewButtons" style="margin-left: 20px" @click="reject">Reject</button>
    <ArticleReader :title="title" :content="content" class="articleReader" />
  </div>


</template>

<style scoped>
.mainContainer {
  padding-left: 50px;
}
.mainContainer .reviewButtons {
  background-color: lightgreen;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}
</style>