<template>
  <div class="meeting-management">
    <h1>文本管理</h1>
    <!-- 查看文本内容的对话框 -->
    <el-dialog v-model="dialogVisible" title="文本内容">
      <el-card>
        <p>{{ textContent }}</p>
      </el-card>
      <template v-slot:footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
    <!-- 会议及其文本列表 -->
    <el-table
      :data="
        meetings.flatMap((meeting) =>
          meeting.textContents.map((textContent) => ({
            ...textContent,
            meeting_name: meeting.meeting_name,
          }))
        )
      "
      style="width: 100%"
    >
      <el-table-column prop="meeting_name" label="会议名称" />
      <el-table-column prop="text_name" label="文本名称" />

      <!-- 查看和删除按钮 -->
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button @click="viewTextContent(scope.row)" size="mini"
            >查看</el-button
          >
          <el-button
            @click="deleteTextContent(scope.row)"
            type="danger"
            size="mini"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const meetings = ref([]); // 存储会议记录及其文本内容
    const dialogVisible = ref(false);
    const textContent = ref(""); // 存储文本内容

    // 从后端获取会议记录及其文本内容
    const fetchMeetings = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/get_all_meetings"
        );
        const meetingsData = response.data.meetings;

        if (Array.isArray(meetingsData)) {
          meetings.value = await Promise.all(
            meetingsData.map(async (meetingName) => {
              const textNamesResponse = await axios.get(
                `http://localhost:5000/get_text_names_by_meeting`,
                {
                  params: { meeting_name: meetingName },
                }
              );

              const textNames = textNamesResponse.data.names || [];
              const textContents = textNames.map((textName) => ({
                text_name: textName,
              }));

              return {
                meeting_name: meetingName,
                textContents,
              };
            })
          );
        } else {
          console.error("Unexpected response structure:", response.data);
        }
      } catch (error) {
        console.error("Error fetching meetings:", error);
      }
    };

    // 查看文本内容
    const viewTextContent = async (row) => {
      try {
        const response = await axios.get(
          `http://localhost:5000/get_text_content/${row.meeting_name}/${row.text_name}`
        );
        textContent.value = response.data.text_content;
        dialogVisible.value = true;
      } catch (error) {
        console.error("Error fetching text content:", error);
      }
    };

    // 删除文本内容
    const deleteTextContent = async (row) => {
      try {
        await axios.delete(
          `http://localhost:5000/delete_text_content/${row.meeting_name}/${row.text_name}`
        );
        // Refresh meetings after deletion
        await fetchMeetings();
      } catch (error) {
        console.error("Error deleting text content:", error);
      }
    };

    // 组件挂载时获取会议数据
    onMounted(fetchMeetings);

    return {
      meetings,
      textContent,
      dialogVisible,
      viewTextContent,
      deleteTextContent,
    };
  },
};
</script>

<style scoped>
.meeting-management {
  padding: 20px;
}
</style>
