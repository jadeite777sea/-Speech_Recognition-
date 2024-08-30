<template>
  <div class="summary-generation">
    <h1>生成摘要</h1>
    <button @click="generateSummary">生成摘要</button>
    <div v-if="summary" class="summary">
      <h2>会议摘要</h2>
      <p>{{ summary }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      summary: "",
    };
  },
  methods: {
    generateSummary() {
      // 调用后端API生成摘要
      fetch("http://localhost:8080/generate-summary")
        .then((response) => response.json())
        .then((data) => {
          this.summary = data.summary;
        });
    },
  },
};
</script>

<style scoped>
.summary-generation {
  padding: 20px;
}
.summary {
  margin-top: 20px;
}
</style>
