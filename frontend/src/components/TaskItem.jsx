import React from 'react';

function TaskItem({ task, onToggleComplete, onDeleteTask }) {
  // Handle checkbox change to toggle completion status
  const handleCheckboxChange = () => {
    onToggleComplete(task.id, !task.is_completed);
  };

  // Handle delete button click
  const handleDeleteClick = () => {
    onDeleteTask(task.id);
  };

  return (
    <li className="task-item">
      <input
        type="checkbox"
        checked={task.is_completed}
        onChange={handleCheckboxChange}
        aria-labelledby={`task-description-${task.id}`} // Accessibility
      />
      <span
         id={`task-description-${task.id}`}
         className={task.is_completed ? 'completed' : ''}
      >
        {task.description}
      </span>
      <button onClick={handleDeleteClick} aria-label={`Delete task: ${task.description}`}>
        Delete
      </button>
    </li>
  );
}

export default TaskItem;
