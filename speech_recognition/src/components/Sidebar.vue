<!-- src/components/Sidebar.vue -->
<template>
  <aside class="app-sidebar">
    <ul>
      <li><router-link to="/meeting-recording">会议记录</router-link></li>
      <li><router-link to="/summary-generation">生成摘要</router-link></li>
      <li><router-link to="/text-management">文本管理</router-link></li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: "AppSidebar",
};
</script>

<style scoped>
.app-sidebar {
  width: 200px;
  background-color: #222d32;
  padding: 20px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
}
.app-sidebar ul {
  list-style: none;
  padding: 0;
}
.app-sidebar ul li {
  margin-bottom: 20px;
}
.app-sidebar ul li a {
  color: #b8c7ce;
  text-decoration: none;
  font-size: 18px;
  display: block;
}
.app-sidebar ul li a:hover {
  color: #fff;
}
</style>
