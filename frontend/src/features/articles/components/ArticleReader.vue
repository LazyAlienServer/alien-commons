<script setup>
import {computed, ref} from 'vue'
import { generateHTML } from '@tiptap/core'
import StarterKit from "@tiptap/starter-kit";
import { TaskItem, TaskList } from "@tiptap/extension-list";
import Superscript from "@tiptap/extension-superscript";
import Subscript from "@tiptap/extension-subscript";
import Highlight from "@tiptap/extension-highlight";
import TextAlign from "@tiptap/extension-text-align";
import Mathematics from "@tiptap/extension-mathematics";
import Image from "@tiptap/extension-image";
import Youtube from "@tiptap/extension-youtube";
import { ReviewToolBar } from '@/features/articles/components'
import { withdrawArticle } from '@/features/articles/api'
import { useToast } from "vue-toastification";
import { useRouter, useRoute } from "vue-router";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  content: {
    type: Object,
    required: true,
  }
})

const extensions = [
  StarterKit.configure({
    link: {
      openOnClick: true,
      autolink: true,
      defaultProtocol: 'https',
      linkOnPaste: true,
      HTMLAttributes: {
        class: 'link',
        rel: 'noopener noreferrer',
        target: '_blank',
      },
    },
    heading: {
      levels: [1, 2, 3],
    },
  }),
  TaskList,
  TaskItem.configure({
    nested: false,
  }),
  Superscript,
  Subscript,
  Highlight,
  TextAlign.configure({
    types: ['heading', 'paragraph'],
    defaultAlignment: 'left',
  }),
  Mathematics,
  Image.configure({
    inline: false,
    allowBase64: false,
  }),
  Youtube.configure({
    width: 480,
    height: 320,
    controls: false,
    nocookie: true,
  }),
]
// Generate HTML from JSON
const html = computed(() => {
  try {
    return generateHTML(props.content, extensions)
  } catch (error) {
    console.error("Failed to render content", error)
    return "<p class='text-red-600'>Failed to render content.</p>"
  }
})

const loading = ref(false);
const toast = useToast();
const router = useRouter();
const route = useRoute();

async function handleWithdraw() {
  loading.value = true;
  const id = route.params.id

  try {
    await withdrawArticle(id);
    toast.success("Article withdrew successfully!");
    await router.push({ name: 'article-editor', params: { id }});

  } catch (error) {
    toast.error(error.response?.data?.toast_error);
    console.error("Failed to withdraw the article", error);

  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <Teleport to="#page-header">
    <ReviewToolBar
        :loading="loading"
        @withdraw="handleWithdraw()"
    />
  </Teleport>

  <article class="flex flex-col flex-1 w-3/5">
    <!-- title -->
    <h1 class="text-[45px] font-semibold mb-6">{{ title || "Untitled"}}</h1>

    <!-- content -->
    <div class="ProseMirror" v-html="html"></div>
  </article>
</template>
