import apiClient from './client'
import { API_ENDPOINTS } from './endpoints'

export interface Assignment {
  id: string
  title: string
  instructions: string
  due_date: string
  teacher_name: string
  subject_name: string
  class_name: string
}

export const getAssignments = async (): Promise<Assignment[]> => {
  const response = await apiClient.get(API_ENDPOINTS.assignments)
  return response.data
}

export const getAssignment = async (id: string): Promise<Assignment> => {
  const response = await apiClient.get(`${API_ENDPOINTS.assignments}${id}/`)
  return response.data
}

export const createAssignment = async (data: Partial<Assignment>): Promise<Assignment> => {
  const response = await apiClient.post(API_ENDPOINTS.assignments, data)
  return response.data
}

export const updateAssignment = async (id: string, data: Partial<Assignment>): Promise<Assignment> => {
  const response = await apiClient.put(`${API_ENDPOINTS.assignments}${id}/`, data)
  return response.data
}

export const deleteAssignment = async (id: string): Promise<void> => {
  await apiClient.delete(`${API_ENDPOINTS.assignments}${id}/`)
}