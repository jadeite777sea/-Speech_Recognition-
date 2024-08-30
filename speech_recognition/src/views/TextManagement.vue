<template>
  <div class="meeting-management">
    <h1>会议管理</h1>
    <!-- 会议列表 -->
    <el-table :data="meetings" style="width: 100%">
      <el-table-column prop="meeting_name" label="会议名称" />
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button @click="viewMeeting(scope.row)" size="mini"
            >查看</el-button
          >
          <el-button
            @click="deleteMeeting(scope.row.id)"
            type="danger"
            size="mini"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 查看会议内容的对话框 -->
    <el-dialog v-model:visible="dialogVisible" title="会议内容">
      <el-card>
        <p>{{ meetingContent }}</p>
      </el-card>
      <template v-slot:footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const meetings = ref([]); // 存储会议记录
    const dialogVisible = ref(false); // 控制对话框显示
    const meetingContent = ref(""); // 存储会议内容

    // 从后端获取会议记录
    const fetchMeetings = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/get_all_meetings"
        );
        meetings.value = response.data.meetings;
      } catch (error) {
        console.error("Error fetching meetings:", error);
      }
    };

    // 查看会议详细内容
    const viewMeeting = async (meeting) => {
      try {
        const response = await axios.get(
          `http://localhost:5000/get_text_content`,
          {
            params: { meeting_name: meeting.meeting_name },
          }
        );
        meetingContent.value = response.data.names.join("\n"); // 假设内容为列表形式展示
        dialogVisible.value = true;
      } catch (error) {
        console.error("Error fetching meeting content:", error);
      }
    };

    // 删除会议
    const deleteMeeting = async (id) => {
      try {
        await axios.delete(`http://localhost:5000/delete_meeting/${id}`);
        meetings.value = meetings.value.filter((meeting) => meeting.id !== id);
      } catch (error) {
        console.error("Error deleting meeting:", error);
      }
    };

    // 组件挂载时获取会议数据
    onMounted(fetchMeetings);

    return {
      meetings,
      dialogVisible,
      meetingContent,
      viewMeeting,
      deleteMeeting,
    };
  },
};
</script>

<style scoped>
.meeting-management {
  padding: 20px;
}
</style>
