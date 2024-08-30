<template>
  <div class="summary-generation">
    <h1>生成摘要</h1>
    <el-table :data="meetings" style="width: 100%">
      <el-table-column prop="meeting_name" label="会议名称" />
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button
            type="primary"
            @click="generateSummary(scope.row.meeting_name)"
          >
            生成摘要
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Summary Dialog -->
    <el-dialog
      title="会议摘要"
      v-model:visible="dialogVisible"
      width="50%"
      @close="dialogVisible = false"
    >
      <p>{{ summaryContent }}</p>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      meetings: [], // 储存从后端获取的会议列表
      dialogVisible: false, // 控制对话框的显示
      summaryContent: "", // 储存从后端获取的摘要内容
    };
  },
  created() {
    // 获取会议列表
    this.fetchMeetings();
  },
  methods: {
    fetchMeetings() {
      axios
        .get("http://localhost:5000/get_all_meetings")
        .then((response) => {
          this.meetings = response.data.meetings.map((meeting_name) => ({
            meeting_name,
          }));
        })
        .catch((error) => {
          console.error("Error fetching meetings:", error);
        });
    },
    generateSummary(meeting_name) {
      // 调用生成摘要的逻辑
      axios
        .post("http://localhost:5000/text_summary", {
          content: meeting_name, // 传递会议名称作为示例内容
        })
        .then((response) => {
          this.summaryContent = response.data.response_json;
          this.dialogVisible = true; // 显示对话框
        })
        .catch((error) => {
          console.error("Error generating summary:", error);
        });
    },
  },
};
</script>

<style scoped>
.summary-generation {
  padding: 20px;
}
</style>
