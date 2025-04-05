import React, { useState, useEffect, useCallback } from 'react';
import TaskList from './components/TaskList';
import AddTaskForm from './components/AddTaskForm';
import './index.css'; // Ensure styles are imported

// Get the API base URL from environment variables defined by Vite
// Fallback needed if running outside Vite context (though unlikely here)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
console.log("API Base URL:", API_BASE_URL); // For debugging

function App() {
  // State for the list of tasks
  const [tasks, setTasks] = useState([]);
  // State for loading status
  const [loading, setLoading] = useState(true);
  // State for error messages
  const [error, setError] = useState(null);

  // --- Fetch Tasks Function ---
  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null); // Reset error before fetching
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`);
      if (!response.ok) {
        // Throw an error if response status is not OK (e.g., 4xx, 5xx)
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTasks(data); // Update tasks state with fetched data
    } catch (e) {
      console.error("Failed to fetch tasks:", e);
      setError(`Failed to load tasks: ${e.message}. Is the backend running?`);
    } finally {
      setLoading(false); // Set loading to false regardless of success or failure
    }
  }, []); // Empty dependency array means this function is created once

  // --- useEffect Hook to Fetch Tasks on Mount ---
  useEffect(() => {
    fetchTasks(); // Fetch tasks when the component mounts
  }, [fetchTasks]); // Depend on fetchTasks (which itself has no dependencies)

  // --- Add Task Handler ---
  const handleAddTask = async (description) => {
    setError(null); // Clear previous errors
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: description, is_completed: false }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const newTask = await response.json();
      // Add the new task to the existing list in state
      setTasks(prevTasks => [...prevTasks, newTask]);
    } catch (e) {
      console.error("Failed to add task:", e);
      setError(`Failed to add task: ${e.message}`);
    }
  };

  // --- Toggle Task Completion Handler ---
  const handleToggleComplete = async (id, is_completed) => {
     setError(null);
     // Optimistically update UI first for better UX
     const originalTasks = [...tasks];
     setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id ? { ...task, is_completed: is_completed } : task
        )
     );

    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_completed: is_completed }), // Only send the changed field
      });
      if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Optional: Fetch tasks again or update state with response if needed,
      // but optimistic update often suffices here.
      // const updatedTask = await response.json();
      // setTasks(prevTasks => prevTasks.map(task => task.id === id ? updatedTask : task));

    } catch (e) {
      console.error("Failed to update task:", e);
      setError(`Failed to update task ${id}: ${e.message}. Reverting.`);
      // Revert optimistic update on failure
      setTasks(originalTasks);
    }
  };

  // --- Delete Task Handler ---
  const handleDeleteTask = async (id) => {
    setError(null);
    // Optimistic update
    const originalTasks = [...tasks];
    setTasks(prevTasks => prevTasks.filter(task => task.id !== id));

    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'DELETE',
      });
      // DELETE often returns 204 No Content, response.ok handles this
      if (!response.ok && response.status !== 204) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // No need to update state further if successful, already done optimistically
    } catch (e) {
      console.error("Failed to delete task:", e);
      setError(`Failed to delete task ${id}: ${e.message}. Reverting.`);
      // Revert optimistic update on failure
      setTasks(originalTasks);
    }
  };

  // --- Render Logic ---
  return (
    <div>
      <h1>My To-Do List</h1>
      <AddTaskForm onAddTask={handleAddTask} />

      {/* Display loading message */}
      {loading && <p className="message">Loading tasks...</p>}

      {/* Display error message */}
      {error && <p className="message error">{error}</p>}

      {/* Display task list if not loading and no critical error preventing display */}
      {!loading && (
         <TaskList
            tasks={tasks}
            onToggleComplete={handleToggleComplete}
            onDeleteTask={handleDeleteTask}
          />
      )}
    </div>
  );
}

export default App;
