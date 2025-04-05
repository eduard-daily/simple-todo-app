import React, { useState } from 'react';

function AddTaskForm({ onAddTask }) {
  // State to hold the value of the input field
  const [description, setDescription] = useState('');

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior (page reload)
    if (!description.trim()) return; // Don't add empty tasks

    // Call the onAddTask function passed from the parent (App.jsx)
    onAddTask(description);

    // Clear the input field after adding the task
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="add-task-form">
      <input
        type="text"
        placeholder="Add a new task..."
        value={description}
        onChange={(e) => setDescription(e.target.value)} // Update state on input change
        aria-label="New task description" // Accessibility
      />
      <button type="submit">Add Task</button>
    </form>
  );
}

export default AddTaskForm;
