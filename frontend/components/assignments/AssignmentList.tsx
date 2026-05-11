'use client'

import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface Assignment {
  id: string
  title: string
  instructions: string
  due_date: string
  teacher_name: string
  subject_name: string
  class_name: string
}

export function AssignmentList() {
  const { data: assignments, isLoading, error } = useQuery({
    queryKey: ['assignments'],
    queryFn: async () => {
      const response = await axios.get('/api/assignments/')
      return response.data
    },
  })

  if (isLoading) return <div>Loading assignments...</div>
  if (error) return <div>Error loading assignments</div>

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Assignments</h1>
      <div className="grid gap-4">
        {assignments?.map((assignment: Assignment) => (
          <div key={assignment.id} className="border rounded-lg p-4 shadow-sm">
            <h2 className="text-xl font-semibold">{assignment.title}</h2>
            <p className="text-gray-600">{assignment.instructions}</p>
            <div className="mt-2 text-sm text-gray-500">
              <p>Teacher: {assignment.teacher_name}</p>
              <p>Subject: {assignment.subject_name}</p>
              <p>Class: {assignment.class_name}</p>
              <p>Due: {new Date(assignment.due_date).toLocaleDateString()}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}