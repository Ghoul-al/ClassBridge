export const API_ENDPOINTS = {
  // Auth
  login: '/auth/login/',
  register: '/auth/register/',
  refreshToken: '/auth/token/refresh/',

  // Schools
  schools: '/schools/schools/',

  // Classes
  sections: '/classes/sections/',
  classes: '/classes/classes/',
  arms: '/classes/arms/',

  // Subjects
  subjects: '/subjects/subjects/',

  // Academic
  sessions: '/academic/sessions/',
  terms: '/academic/terms/',

  // Students
  students: '/students/students/',

  // Teachers
  teachers: '/teachers/teachers/',
  teacherSubjects: '/teachers/teacher-subjects/',
  teacherClasses: '/teachers/teacher-classes/',

  // Parents
  parents: '/parents/parents/',
  parentStudents: '/parents/parent-students/',

  // Learning
  assignments: '/learning/assignments/',
  submissions: '/learning/submissions/',
  fileUpload: '/learning/files/upload/',

  // CBT
  exams: '/cbt/exams/',
  questions: '/cbt/questions/',
  choices: '/cbt/choices/',
  examAttempts: '/cbt/attempts/',
}