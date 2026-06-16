import axios from 'axios'
import { ElMessage } from 'element-plus'

const http = axios.create({
  baseURL: '/api',
  timeout: 10000
})

http.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && body.success === false) {
      ElMessage.error(body.message || '操作失败')
      return Promise.reject(new Error(body.message || '操作失败'))
    }
    return body?.data ?? body
  },
  (error) => {
    ElMessage.error(error.response?.data?.message || error.message || '请求失败')
    return Promise.reject(error)
  }
)

export const api = {
  login: (data) => http.post('/auth/login', data),
  summary: () => http.get('/dashboard/summary'),
  students: (params) => http.get('/students', { params }),
  allStudents: () => http.get('/students/all'),
  createStudent: (data) => http.post('/students', data),
  updateStudent: (id, data) => http.put(`/students/${id}`, data),
  deleteStudent: (id) => http.delete(`/students/${id}`),
  courses: (params) => http.get('/courses', { params }),
  allCourses: () => http.get('/courses/all'),
  createCourse: (data) => http.post('/courses', data),
  updateCourse: (id, data) => http.put(`/courses/${id}`, data),
  deleteCourse: (id) => http.delete(`/courses/${id}`),
  scores: (params) => http.get('/scores', { params }),
  createScore: (data) => http.post('/scores', data),
  updateScore: (id, data) => http.put(`/scores/${id}`, data),
  deleteScore: (id) => http.delete(`/scores/${id}`)
}

