<template>
  <div id="app">
    <Meeting />
  </div>
</template>

<script>
import Meeting from './components/Meeting.vue'

export default {
  name: 'App',
  components: {
    Meeting
  }
}
</script>

<style>
body, html, #app {
  margin: 0;
  height: 100%;
  font-family: Arial, sans-serif;
}
</style>
