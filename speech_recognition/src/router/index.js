// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import MeetingRecording from "../views/MeetingRecording.vue";
import SummaryGeneration from "../views/SummaryGeneration.vue";
import TextManagement from "../views/TextManagement.vue";

const routes = [
  {
    path: "/",
    redirect: "/meeting-recording",
  },
  {
    path: "/meeting-recording",
    component: MeetingRecording,
    meta: { title: "会议记录" }, // Add title here
  },
  {
    path: "/summary-generation",
    component: SummaryGeneration,
    meta: { title: "生成摘要" }, // Add title here
  },
  {
    path: "/text-management",
    component: TextManagement,
    meta: { title: "文本管理" }, // Add title here
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
