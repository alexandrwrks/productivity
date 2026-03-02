document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const todoList = document.getElementById('todoList');
    const totalTasksSpan = document.getElementById('totalTasks');
    const completedTasksSpan = document.getElementById('completedTasks');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const clearCompletedBtn = document.getElementById('clearCompleted');

    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    let currentFilter = 'all';

    // Функция для сохранения задач в localStorage
    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    // Функция для обновления статистики
    function updateStats() {
        const total = tasks.length;
        const completed = tasks.filter(task => task.completed).length;
        
        totalTasksSpan.textContent = total;
        completedTasksSpan.textContent = completed;
    }

    // Функция для экранирования HTML специальных символов
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Функция для отображения задач
    function renderTasks() {
        let filteredTasks = tasks;
        
        if (currentFilter === 'active') {
            filteredTasks = tasks.filter(task => !task.completed);
        } else if (currentFilter === 'completed') {
            filteredTasks = tasks.filter(task => task.completed);
        }

        if (filteredTasks.length === 0) {
            todoList.innerHTML = '<li class="empty-message">✨ Задач пока нет. Добавьте новую задачу!</li>';
            return;
        }

        todoList.innerHTML = filteredTasks.map(task => `
            <li class="todo-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
                <input type="checkbox" class="todo-checkbox" ${task.completed ? 'checked' : ''}>
                <span class="todo-text">${escapeHtml(task.text)}</span>
                <button class="delete-btn" title="Удалить задачу">🗑️</button>
            </li>
        `).join('');

        updateStats();
    }

    // Функция для добавления новой задачи
    function addTask() {
        const text = taskInput.value.trim();
        
        if (text === '') {
            alert('Пожалуйста, введите текст задачи!');
            return;
        }

        const newTask = {
            id: Date.now().toString(),
            text: text,
            completed: false
        };

        tasks.push(newTask);
        saveTasks();
        renderTasks();
        
        taskInput.value = '';
        taskInput.focus();
    }

    // Обработчик для переключения статуса задачи
    function toggleTask(taskId) {
        const task = tasks.find(t => t.id === taskId);
        if (task) {
            task.completed = !task.completed;
            saveTasks();
            renderTasks();
        }
    }

    // Обработчик для удаления задачи
    function deleteTask(taskId) {
        tasks = tasks.filter(t => t.id !== taskId);
        saveTasks();
        renderTasks();
    }

    // Обработчик для очистки выполненных задач
    function clearCompleted() {
        tasks = tasks.filter(task => !task.completed);
        saveTasks();
        renderTasks();
    }

    // Обработчик для фильтрации задач
    function setFilter(filter) {
        currentFilter = filter;
        
        filterButtons.forEach(btn => {
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        renderTasks();
    }

    // Обработчик клика по списку задач (делегирование событий)
    todoList.addEventListener('click', function(e) {
        const todoItem = e.target.closest('.todo-item');
        
        if (!todoItem) return;
        
        const taskId = todoItem.dataset.id;

        if (e.target.classList.contains('delete-btn')) {
            deleteTask(taskId);
        } else if (e.target.classList.contains('todo-checkbox')) {
            toggleTask(taskId);
        }
    });

    // Обработчик добавления задачи по кнопке
    addBtn.addEventListener('click', addTask);

    // Обработчик добавления задачи по Enter
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // Обработчики для фильтров
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            setFilter(this.dataset.filter);
        });
    });

    // Обработчик для очистки выполненных задач
    clearCompletedBtn.addEventListener('click', clearCompleted);

    // Начальная отрисовка задач
    renderTasks();
});