'use client'

import { useQuery } from '@tanstack/react-query'
import apiClient from '../../lib/api/client'
import { API_ENDPOINTS } from '../../lib/api/endpoints'

interface Exam {
  id: string
  title: string
  description: string
  duration: number
  total_marks: number
  teacher_name: string
  subject_name: string
  class_name: string
  question_count: number
}

export function ExamList() {
  const { data: exams, isLoading, error } = useQuery({
    queryKey: ['exams'],
    queryFn: async () => {
      const response = await apiClient.get(API_ENDPOINTS.exams)
      return response.data
    },
  })

  if (isLoading) return <div>Loading exams...</div>
  if (error) return <div>Error loading exams</div>

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">CBT Exams</h1>
      <div className="grid gap-4">
        {exams?.map((exam: Exam) => (
          <div key={exam.id} className="border rounded-lg p-4 shadow-sm">
            <h2 className="text-xl font-semibold">{exam.title}</h2>
            <p className="text-gray-600">{exam.description}</p>
            <div className="mt-2 text-sm text-gray-500">
              <p>Teacher: {exam.teacher_name}</p>
              <p>Subject: {exam.subject_name}</p>
              <p>Class: {exam.class_name}</p>
              <p>Duration: {exam.duration} minutes</p>
              <p>Total Marks: {exam.total_marks}</p>
              <p>Questions: {exam.question_count}</p>
            </div>
            <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Start Exam
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}