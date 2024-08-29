<!-- src/App.vue -->
<template>
  <div id="app">
    <AppHeader />
    <div class="main-layout">
      <AppSidebar />
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "./components/Header.vue";
import AppSidebar from "./components/Sidebar.vue";

export default {
  components: {
    AppHeader,
    AppSidebar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.main-layout {
  display: flex;
}
.content {
  margin-left: 200px; /* Same as sidebar width */
  padding: 20px;
  flex-grow: 1;
  background-color: #ecf0f5;
  min-height: 100vh;
}
</style>
