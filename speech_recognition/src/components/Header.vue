<!-- src/components/Header.vue -->
<template>
  <header class="app-header">
    <div class="logo">会议总结系统</div>
    <div class="page-title">{{ pageTitle }}</div>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
  computed: {
    pageTitle() {
      // Get the current route's meta title, or a default title if not defined
      return this.$route.meta.title || "会议总结系统";
    },
  },
};
</script>

<style scoped>
.app-header {
  background-color: #3c8dbc;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}
.logo {
  font-size: 24px;
  font-weight: bold;
}
.page-title {
  font-size: 20px;
}
</style>
