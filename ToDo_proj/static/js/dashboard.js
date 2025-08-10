// Variáveis globais
    let currentTaskId = null;
    let isEditMode = false;

    /**
     * Função para abrir modal de criação de tarefa
     */
    function openCreateModal() {
        isEditMode = false;
        currentTaskId = null;
        
        document.getElementById('modalTitle').textContent = 'Nova Tarefa';
        document.getElementById('submitBtn').textContent = 'Criar Tarefa';
        
        // Limpar formulário
        document.getElementById('taskForm').reset();
        
        showModal('taskModal');
    }

    /**
     * Função para abrir modal de edição de tarefa
     */
    async function openEditModal(taskId) {
        isEditMode = true;
        currentTaskId = taskId;
        
        document.getElementById('modalTitle').textContent = 'Editar Tarefa';
        document.getElementById('submitBtn').textContent = 'Salvar Alterações';
        
        try {
            const response = await fetch(`/get/${taskId}/`);
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('taskTitle').value = data.task.title;
                document.getElementById('taskDescription').value = data.task.description;
                document.getElementById('taskStatus').value = data.task.status;
                
                showModal('taskModal');
            } else {
                showToast('Erro ao carregar tarefa', 'error');
            }
        } catch (error) {
            console.error('Erro:', error);
            showToast('Erro ao carregar tarefa', 'error');
        }
    }

    /**
     * Função para abrir modal de confirmação de exclusão
     */
    function openDeleteModal(taskId, taskTitle) {
        currentTaskId = taskId;
        document.getElementById('deleteTaskTitle').textContent = taskTitle;
        showModal('deleteModal');
    }

    /**
     * Função para marcar tarefa como concluída
     */
    async function completeTask(taskId) {
        try {
            const response = await fetch(`/complete/${taskId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast(data.message, 'success');
                reloadTasks();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            console.error('Erro:', error);
            showToast('Erro ao marcar tarefa como concluída', 'error');
        }
    }

    /**
     * Função para exibir modal
     */
    function showModal(modalId) {
        document.getElementById(modalId).classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Função para fechar modal
     */
    function closeModal(modalId) {
        document.getElementById(modalId).classList.remove('show');
        document.body.style.overflow = 'auto';
        
        if (modalId === 'taskModal') {
            document.getElementById('taskForm').reset();
            currentTaskId = null;
            isEditMode = false;
        }
    }



    /**
     * Função para recarregar a lista de tarefas com delay
     */
    function reloadTasks() {
        setTimeout(() => {
            window.location.reload();
        }, 1500); // Delay para permitir que o toast seja visto
    }

    /**
     * Handler do formulário de tarefa
     */
    document.getElementById('taskForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const title = document.getElementById('taskTitle').value.trim();
        const description = document.getElementById('taskDescription').value.trim();
        const status = document.getElementById('taskStatus').value;
        
        if (!title) {
            showToast('Título é obrigatório', 'error');
            return;
        }
        
        const taskData = {
            title: title,
            description: description,
            status: status
        };
        
        try {
            const url = isEditMode ? `/update/${currentTaskId}/` : '/create/';
            const method = 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(taskData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast(data.message, 'success');
                closeModal('taskModal');
                reloadTasks();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            console.error('Erro:', error);
            showToast('Erro ao salvar tarefa', 'error');
        }
    });

    /**
     * Handler do botão de confirmação de exclusão
     */
    document.getElementById('confirmDeleteBtn').addEventListener('click', async function() {
        if (!currentTaskId) return;
        
        try {
            const response = await fetch(`/delete/${currentTaskId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast(data.message, 'success');
                closeModal('deleteModal');
                reloadTasks();
            } else {
                showToast(data.error, 'error');
            }
        } catch (error) {
            console.error('Erro:', error);
            showToast('Erro ao excluir tarefa', 'error');
        }
    });


    /**
     * Fechar modais ao clicar fora deles
     */
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            const modalId = e.target.id;
            closeModal(modalId);
        }
    });

    /**
     * Fechar modais com tecla ESC
     */
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal.id);
            }
        }
    });

    /**
     * Auto-submit do formulário de filtros quando houver mudança
     */
    document.querySelector('.filter-select').addEventListener('change', function() {
        this.form.submit();
    });


//capturar os dados pro grafico de datas
document.addEventListener('DOMContentLoaded', async function() {
    
    const response = await fetch('/all_dates');
    const data = await response.json();
    if (data.success) {
        const ctx = document.getElementById('taskChart').getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data.counts),
                datasets: [{
                    label: 'Quantidade de Tarefas por mês',
                    data: Object.values(data.counts),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                animation: {
                    duration: 2000,
                }


            }
        });
    }



});

/**
 * Inicialização quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit do filtro quando o status for alterado

    showToast('Dica, use shift + enter para criar uma nova tarefa', 'success',6000);




    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            document.getElementById('filterForm').submit();
        });
    }
});

//shift + enter abrir modal de criacao de tarefa
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.shiftKey) {
        openCreateModal();
    }
});
