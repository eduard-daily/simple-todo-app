import React from 'react';
import TaskItem from './TaskItem'; // Import the TaskItem component

function TaskList({ tasks, onToggleComplete, onDeleteTask }) {
  // If there are no tasks, display a message
  if (!tasks || tasks.length === 0) {
    return <p className="message">No tasks yet. Add one above!</p>;
  }

  // Render the list of tasks
  return (
    <ul className="task-list">
      {tasks.map((task) => (
        // Render a TaskItem for each task in the array
        // Pass necessary data and handler functions as props
        <TaskItem
          key={task.id} // React needs a unique key for list items
          task={task}
          onToggleComplete={onToggleComplete}
          onDeleteTask={onDeleteTask}
        />
      ))}
    </ul>
  );
}

export default TaskList;
