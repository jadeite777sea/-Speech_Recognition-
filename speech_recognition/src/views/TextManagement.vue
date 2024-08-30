<template>
  <div class="text-management">
    <h1>文本管理</h1>
    <!-- 会议记录列表 -->
    <ul>
      <li v-for="(record, index) in records" :key="index">
        {{ record.title }}
        <button @click="viewRecord(record)">查看</button>
        <button @click="deleteRecord(record.id)">删除</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      records: [], // 会议记录数组
    };
  },
  created() {
    // 从后端获取会议记录
    fetch("http://localhost:8080/records")
      .then((response) => response.json())
      .then((data) => {
        this.records = data.records;
      });
  },
  methods: {
    viewRecord(record) {
      // 查看详细记录的逻辑
      this.$router.push(`/record/${record.id}`);
    },
    deleteRecord(id) {
      // 删除记录的逻辑
      fetch(`http://localhost:8080/records/${id}`, { method: "DELETE" }).then(
        () => {
          this.records = this.records.filter((record) => record.id !== id);
        }
      );
    },
  },
};
</script>

<style scoped>
.text-management {
  padding: 20px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}
</style>
