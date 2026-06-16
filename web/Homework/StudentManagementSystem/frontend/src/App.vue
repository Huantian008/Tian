<template>
  <div v-if="!currentUser" class="login-screen">
    <section class="login-card">
      <div>
        <p class="eyebrow">WEB框架技术期末作品</p>
        <h1>学生管理系统</h1>
        <p class="login-copy">面向班级学生、课程与成绩信息的统一维护平台。</p>
      </div>
      <el-form :model="loginForm" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" size="large" placeholder="admin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" size="large" type="password" show-password placeholder="123456" />
        </el-form-item>
        <el-button type="primary" size="large" class="full-btn" :loading="loading" @click="handleLogin">登录系统</el-button>
      </el-form>
    </section>
  </div>

  <el-container v-else class="app-shell">
    <el-aside width="228px" class="sidebar">
      <div class="brand">
        <span>SMS</span>
        <strong>学生管理系统</strong>
      </div>
      <el-menu :default-active="activeView" class="menu" @select="switchView">
        <el-menu-item index="dashboard">首页统计</el-menu-item>
        <el-menu-item index="students">学生管理</el-menu-item>
        <el-menu-item index="courses">课程管理</el-menu-item>
        <el-menu-item index="scores">成绩管理</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div>
          <h2>{{ viewTitle }}</h2>
          <p>当前用户：{{ currentUser.realName }} / {{ currentUser.role }}</p>
        </div>
        <el-button @click="logout">退出登录</el-button>
      </el-header>

      <el-main class="content">
        <section v-if="activeView === 'dashboard'" class="dashboard">
          <div class="stat-grid">
            <article class="stat-card"><span>学生总数</span><strong>{{ summary.studentCount }}</strong></article>
            <article class="stat-card"><span>课程总数</span><strong>{{ summary.courseCount }}</strong></article>
            <article class="stat-card"><span>选课记录</span><strong>{{ summary.scoreCount }}</strong></article>
            <article class="stat-card"><span>平均成绩</span><strong>{{ summary.averageScore }}</strong></article>
          </div>
          <div class="panel">
            <h3>系统说明</h3>
            <p>本系统围绕学生信息、课程信息与成绩选课关系展开，提供后台管理常用的查询、新增、修改和删除操作。</p>
          </div>
        </section>

        <section v-if="activeView === 'students'" class="panel">
          <CrudToolbar v-model="studentState.keyword" title="学生列表" @search="loadStudents" @create="openStudent()" />
          <el-table :data="studentState.rows" stripe>
            <el-table-column prop="studentNo" label="学号" width="150" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="gender" label="性别" width="80" />
            <el-table-column prop="age" label="年龄" width="80" />
            <el-table-column prop="className" label="班级" min-width="150" />
            <el-table-column prop="major" label="专业" min-width="160" />
            <el-table-column prop="phone" label="电话" width="130" />
            <el-table-column label="操作" width="160" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" @click="openStudent(row)">编辑</el-button>
                <el-button link type="danger" @click="removeStudent(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>

        <section v-if="activeView === 'courses'" class="panel">
          <CrudToolbar v-model="courseState.keyword" title="课程列表" @search="loadCourses" @create="openCourse()" />
          <el-table :data="courseState.rows" stripe>
            <el-table-column prop="courseNo" label="课程编号" width="130" />
            <el-table-column prop="courseName" label="课程名称" min-width="180" />
            <el-table-column prop="credit" label="学分" width="90" />
            <el-table-column prop="teacher" label="任课教师" width="120" />
            <el-table-column prop="semester" label="学期" width="140" />
            <el-table-column label="操作" width="160">
              <template #default="{ row }">
                <el-button link type="primary" @click="openCourse(row)">编辑</el-button>
                <el-button link type="danger" @click="removeCourse(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>

        <section v-if="activeView === 'scores'" class="panel">
          <CrudToolbar v-model="scoreState.keyword" title="成绩列表" @search="loadScores" @create="openScore()" />
          <el-table :data="scoreState.rows" stripe>
            <el-table-column prop="studentNo" label="学号" width="140" />
            <el-table-column prop="studentName" label="学生姓名" width="110" />
            <el-table-column prop="courseName" label="课程名称" min-width="170" />
            <el-table-column prop="score" label="成绩" width="90" />
            <el-table-column prop="semester" label="学期" width="140" />
            <el-table-column label="操作" width="160">
              <template #default="{ row }">
                <el-button link type="primary" @click="openScore(row)">编辑</el-button>
                <el-button link type="danger" @click="removeScore(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>
      </el-main>
    </el-container>
  </el-container>

  <el-dialog v-model="studentDialog" title="学生信息" width="520px">
    <el-form :model="studentForm" label-width="90px">
      <el-form-item label="学号"><el-input v-model="studentForm.studentNo" /></el-form-item>
      <el-form-item label="姓名"><el-input v-model="studentForm.name" /></el-form-item>
      <el-form-item label="性别"><el-select v-model="studentForm.gender"><el-option label="男" value="男" /><el-option label="女" value="女" /></el-select></el-form-item>
      <el-form-item label="年龄"><el-input-number v-model="studentForm.age" :min="16" :max="60" /></el-form-item>
      <el-form-item label="班级"><el-input v-model="studentForm.className" /></el-form-item>
      <el-form-item label="专业"><el-input v-model="studentForm.major" /></el-form-item>
      <el-form-item label="电话"><el-input v-model="studentForm.phone" /></el-form-item>
      <el-form-item label="邮箱"><el-input v-model="studentForm.email" /></el-form-item>
    </el-form>
    <template #footer><el-button @click="studentDialog=false">取消</el-button><el-button type="primary" @click="saveStudent">保存</el-button></template>
  </el-dialog>

  <el-dialog v-model="courseDialog" title="课程信息" width="500px">
    <el-form :model="courseForm" label-width="90px">
      <el-form-item label="课程编号"><el-input v-model="courseForm.courseNo" /></el-form-item>
      <el-form-item label="课程名称"><el-input v-model="courseForm.courseName" /></el-form-item>
      <el-form-item label="学分"><el-input-number v-model="courseForm.credit" :min="0" :step="0.5" /></el-form-item>
      <el-form-item label="任课教师"><el-input v-model="courseForm.teacher" /></el-form-item>
      <el-form-item label="学期"><el-input v-model="courseForm.semester" /></el-form-item>
    </el-form>
    <template #footer><el-button @click="courseDialog=false">取消</el-button><el-button type="primary" @click="saveCourse">保存</el-button></template>
  </el-dialog>

  <el-dialog v-model="scoreDialog" title="成绩信息" width="520px">
    <el-form :model="scoreForm" label-width="90px">
      <el-form-item label="学生"><el-select v-model="scoreForm.studentId" filterable><el-option v-for="item in allStudents" :key="item.id" :label="`${item.studentNo} ${item.name}`" :value="item.id" /></el-select></el-form-item>
      <el-form-item label="课程"><el-select v-model="scoreForm.courseId" filterable><el-option v-for="item in allCourses" :key="item.id" :label="`${item.courseNo} ${item.courseName}`" :value="item.id" /></el-select></el-form-item>
      <el-form-item label="成绩"><el-input-number v-model="scoreForm.score" :min="0" :max="100" :precision="1" /></el-form-item>
      <el-form-item label="学期"><el-input v-model="scoreForm.semester" /></el-form-item>
    </el-form>
    <template #footer><el-button @click="scoreDialog=false">取消</el-button><el-button type="primary" @click="saveScore">保存</el-button></template>
  </el-dialog>
</template>

<script setup>
import { computed, defineComponent, h, onMounted, reactive, ref } from 'vue'
import { ElButton, ElInput, ElMessage, ElMessageBox } from 'element-plus'
import { api } from './api'

const CrudToolbar = defineComponent({
  props: { modelValue: String, title: String },
  emits: ['update:modelValue', 'search', 'create'],
  setup(props, { emit }) {
    return () => h('div', { class: 'crud-toolbar' }, [
      h('h3', props.title),
      h('div', { class: 'toolbar-actions' }, [
        h(ElInput, {
          modelValue: props.modelValue,
          'onUpdate:modelValue': (value) => emit('update:modelValue', value),
          placeholder: '输入关键字查询',
          clearable: true,
          onClear: () => emit('search'),
          onKeyup: (event) => event.key === 'Enter' && emit('search')
        }),
        h(ElButton, { onClick: () => emit('search') }, () => '查询'),
        h(ElButton, { type: 'primary', onClick: () => emit('create') }, () => '新增')
      ])
    ])
  }
})

const activeView = ref('dashboard')
const loading = ref(false)
const currentUser = ref(JSON.parse(localStorage.getItem('sms-user') || 'null'))
const loginForm = reactive({ username: 'admin', password: '123456' })
const summary = reactive({ studentCount: 0, courseCount: 0, scoreCount: 0, averageScore: 0 })
const studentState = reactive({ keyword: '', rows: [] })
const courseState = reactive({ keyword: '', rows: [] })
const scoreState = reactive({ keyword: '', rows: [] })
const allStudents = ref([])
const allCourses = ref([])

const studentDialog = ref(false)
const courseDialog = ref(false)
const scoreDialog = ref(false)
const studentForm = reactive({})
const courseForm = reactive({})
const scoreForm = reactive({})

const viewTitle = computed(() => ({
  dashboard: '首页统计',
  students: '学生管理',
  courses: '课程管理',
  scores: '成绩管理'
})[activeView.value])

async function handleLogin() {
  loading.value = true
  try {
    currentUser.value = await api.login(loginForm)
    localStorage.setItem('sms-user', JSON.stringify(currentUser.value))
    ElMessage.success('登录成功')
    await loadDashboard()
  } finally {
    loading.value = false
  }
}

function logout() {
  localStorage.removeItem('sms-user')
  currentUser.value = null
}

async function switchView(view) {
  activeView.value = view
  if (view === 'dashboard') await loadDashboard()
  if (view === 'students') await loadStudents()
  if (view === 'courses') await loadCourses()
  if (view === 'scores') await loadScorePage()
}

async function loadDashboard() {
  Object.assign(summary, await api.summary())
}

async function loadStudents() {
  const data = await api.students({ keyword: studentState.keyword, page: 1, size: 20 })
  studentState.rows = data.records
}

async function loadCourses() {
  const data = await api.courses({ keyword: courseState.keyword, page: 1, size: 20 })
  courseState.rows = data.records
}

async function loadScores() {
  const data = await api.scores({ keyword: scoreState.keyword, page: 1, size: 20 })
  scoreState.rows = data.records
}

async function loadScorePage() {
  await Promise.all([refreshOptions(), loadScores()])
}

async function refreshOptions() {
  const [students, courses] = await Promise.all([api.allStudents(), api.allCourses()])
  allStudents.value = students
  allCourses.value = courses
}

function resetForm(target, source) {
  Object.keys(target).forEach((key) => delete target[key])
  Object.assign(target, source)
}

function openStudent(row = null) {
  resetForm(studentForm, row ? { ...row } : { studentNo: '', name: '', gender: '男', age: 22, className: '23专升本计算机7班', major: '计算机科学与技术', phone: '', email: '' })
  studentDialog.value = true
}

async function saveStudent() {
  studentForm.id ? await api.updateStudent(studentForm.id, studentForm) : await api.createStudent(studentForm)
  studentDialog.value = false
  ElMessage.success('学生信息已保存')
  await loadStudents()
}

async function removeStudent(id) {
  await ElMessageBox.confirm('确定删除该学生吗？', '删除确认')
  await api.deleteStudent(id)
  await loadStudents()
}

function openCourse(row = null) {
  resetForm(courseForm, row ? { ...row } : { courseNo: '', courseName: '', credit: 3, teacher: '', semester: '2025-2026-2' })
  courseDialog.value = true
}

async function saveCourse() {
  courseForm.id ? await api.updateCourse(courseForm.id, courseForm) : await api.createCourse(courseForm)
  courseDialog.value = false
  ElMessage.success('课程信息已保存')
  await loadCourses()
}

async function removeCourse(id) {
  await ElMessageBox.confirm('确定删除该课程吗？', '删除确认')
  await api.deleteCourse(id)
  await loadCourses()
}

async function openScore(row = null) {
  await refreshOptions()
  resetForm(scoreForm, row ? { ...row } : { studentId: null, courseId: null, score: 90, semester: '2025-2026-2' })
  scoreDialog.value = true
}

async function saveScore() {
  scoreForm.id ? await api.updateScore(scoreForm.id, scoreForm) : await api.createScore(scoreForm)
  scoreDialog.value = false
  ElMessage.success('成绩信息已保存')
  await loadScores()
}

async function removeScore(id) {
  await ElMessageBox.confirm('确定删除该成绩记录吗？', '删除确认')
  await api.deleteScore(id)
  await loadScores()
}

onMounted(async () => {
  if (currentUser.value) {
    await loadDashboard()
  }
})
</script>

