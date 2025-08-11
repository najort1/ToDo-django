// Variáveis globais
let usersGrid;
let genderChart;
let ageChart;
let currentEditingUserId = null;

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeGrid();
    loadCharts();
    loadStats();
});

function initializeGrid() {
    const columnDefs = [
        { 
            headerName: 'ID', 
            field: 'id', 
            width: 80,
            sortable: true
        },
        { 
            headerName: 'Nome', 
            field: 'full_name', 
            flex: 1,
            sortable: true,
            filter: true
        },
        { 
            headerName: 'Email', 
            field: 'email', 
            flex: 1,
            sortable: true,
            filter: true
        },
        { 
            headerName: 'Idade', 
            field: 'age', 
            width: 100,
            sortable: true
        },
        { 
            headerName: 'Gênero', 
            field: 'gender_display', 
            width: 120,
            sortable: true,
            filter: true
        },
        { 
            headerName: 'Tipo', 
            field: 'user_type_display', 
            width: 120,
            sortable: true,
            filter: true
        },
        { 
            headerName: 'Ativo', 
            field: 'is_active', 
            width: 100,
            sortable: true,
            filter: true,
            cellRenderer: function(params) {
                return `
                    <input type="checkbox" ${params.data.is_active ? 'checked' : ''} onclick="${params.data.is_active ? `deactivateUser(${params.data.id}, '${params.data.full_name}')` : `activateUser(${params.data.id}, '${params.data.full_name}')`}" >
                `;
            }
        },
        { 
            headerName: 'Data Cadastro', 
            field: 'date_joined_formatted', 
            width: 140,
            sortable: true,
            filter: true
        },
        {
            headerName: 'Ações',
            field: 'actions',
            width: 300,
            cellRenderer: function(params) {
                return `
                    <button class="btn btn-info btn-small" onclick="viewUserDetails(${params.data.id})" title="Ver Detalhes">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-danger btn-small" onclick="deleteUser(${params.data.id}, '${params.data.full_name}')" title="Excluir">
                        <i class="fas fa-trash"></i>
                    </button>
                    <select class="user-type-select" onchange="changeUserType(${params.data.id}, this.value)" title="Alterar Tipo">
                        <option value="U" ${params.data.user_type_code === 'U' ? 'selected' : ''}>Usuário</option>
                        <option value="A" ${params.data.user_type_code === 'A' ? 'selected' : ''}>Admin</option>
                        <option value="O" ${params.data.user_type_code === 'O' ? 'selected' : ''}>Observer</option>
                    </select>

                `;
            },
            sortable: false,
            filter: false
        }
    ];

    const gridOptions = {
        columnDefs: columnDefs,
        rowData: [],
        theme: 'legacy',
        rowSelection: { mode: 'singleRow' },
        pagination: true,
        paginationPageSize: 20,
        domLayout: 'normal',
        suppressCellFocus: true,
        rowHeight: 50
    };

    const gridDiv = document.querySelector('#usersGrid');
    usersGrid = agGrid.createGrid(gridDiv, gridOptions);
    
    loadUsersData();
}

// Carregar dados dos usuários
async function loadUsersData() {
    try {
        const response = await fetch('/user/api/users/');
        const data = await response.json();
        
        if (data.users) {
            usersGrid.setGridOption('rowData', data.users);
        }
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
        showToast('Erro ao carregar dados dos usuários', 'error');
    }
}

// Carregar estatísticas
async function loadStats() {
    try {
        const response = await fetch('/user/api/users/');
        const data = await response.json();
        
        if (data.users) {
            const users = data.users;
            const today = new Date().toLocaleDateString('pt-BR');
            
            document.getElementById('total-users').textContent = users.length;
            document.getElementById('active-users').textContent = users.filter(u => u.is_active).length;
            document.getElementById('admin-users').textContent = users.filter(u => u.user_type_code === 'A').length;
            document.getElementById('new-users').textContent = users.filter(u => u.date_joined_formatted === today).length;
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Carregar gráficos
async function loadCharts() {
    await loadGenderChart();
    await loadAgeChart();
}

// Gráfico de gênero (pizza)
async function loadGenderChart() {
    try {
        const response = await fetch('/user/api/gender-stats/');
        const data = await response.json();
        
        const ctx = document.getElementById('genderChart').getContext('2d');
        
        if (genderChart) {
            genderChart.destroy();
        }
        
        genderChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.data.map(item => item.label),
                datasets: [{
                    data: data.data.map(item => item.value),
                    backgroundColor: [
                        '#3498db',
                        '#e74c3c',
                        '#f39c12',
                        '#27ae60',
                        '#9b59b6'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        });
    } catch (error) {
        console.error('Erro ao carregar gráfico de gênero:', error);
    }
}

// Gráfico de idade (barras)
async function loadAgeChart() {
    try {
        const response = await fetch('/user/api/age-stats/');
        const data = await response.json();
        
        const ctx = document.getElementById('ageChart').getContext('2d');
        
        if (ageChart) {
            ageChart.destroy();
        }
        
        ageChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.data.map(item => item.label),
                datasets: [{
                    label: 'Número de Usuários',
                    data: data.data.map(item => item.value),
                    backgroundColor: '#3498db',
                    borderColor: '#2980b9',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erro ao carregar gráfico de idade:', error);
    }
}

// Função para alterar tipo de usuário
async function changeUserType(userId, newType) {
    try {
        const response = await fetch(`/user/api/user/update-type/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ user_type: newType })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadUsersData();
            loadStats();
            loadCharts();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Erro ao alterar tipo de usuário:', error);
        showToast('Erro ao alterar tipo de usuário', 'error');
    }
}

// Função para ver detalhes do usuário
async function viewUserDetails(userId) {
    try {
        const response = await fetch(`/user/api/user/details/${userId}/`);
        const data = await response.json();
        
        if (data.user) {
            // Preencher dados pessoais
            document.getElementById('detailFullName').textContent = data.user.full_name;
            document.getElementById('detailEmail').textContent = data.user.email;
            document.getElementById('detailCpf').textContent = data.user.cpf;
            document.getElementById('detailPhone').textContent = data.user.phone;
            document.getElementById('detailBirthdate').textContent = data.user.birthdate;
            document.getElementById('detailAge').textContent = data.user.age;
            document.getElementById('detailGender').textContent = data.user.gender_display;
            document.getElementById('detailUserType').textContent = data.user.user_type_display;
            document.getElementById('detailStatus').textContent = data.user.is_active;
            document.getElementById('detailDateJoined').textContent = data.user.date_joined;
            
            // Preencher dados de endereço
            document.getElementById('detailAddress').textContent = data.address.formatted_address;
            document.getElementById('detailZipcode').textContent = data.address.zipcode;
            document.getElementById('detailCityState').textContent = data.address.city_state;
            
            // Preencher estatísticas de tasks
            document.getElementById('detailTasksPending').textContent = data.task_stats.pending;
            document.getElementById('detailTasksInProgress').textContent = data.task_stats.in_progress;
            document.getElementById('detailTasksCompleted').textContent = data.task_stats.completed;
            document.getElementById('detailTasksTotal').textContent = data.task_stats.total;
            
            // Mostrar modal
            document.getElementById('userDetailsModal').classList.add('show');
        } else {
            showToast('Erro ao carregar detalhes do usuário', 'error');
        }
    } catch (error) {
        console.error('Erro ao carregar detalhes do usuário:', error);
        showToast('Erro ao carregar detalhes do usuário', 'error');
    }
}

function closeUserDetailsModal() {
    document.getElementById('userDetailsModal').classList.remove('show');
}

// Função para deletar usuário
function deleteUser(userId, userName) {
    document.getElementById('confirmMessage').textContent = 
        `Tem certeza que deseja excluir o usuário "${userName}"? Esta ação não pode ser desfeita.`;
    
    document.getElementById('confirmButton').onclick = async function() {
        try {
            const response = await fetch(`/user/api/user/delete/${userId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message, 'success');
                loadUsersData();
                loadStats();
                loadCharts();
            } else {
                showToast(result.error, 'error');
            }
        } catch (error) {
            console.error('Erro ao deletar usuário:', error);
            showToast('Erro ao deletar usuário', 'error');
        }
        
        closeConfirmModal();
    };
    
    document.getElementById('confirmModal').classList.add('show');
}

async function deactivateUser(userId, userName) {
    try {
        const response = await fetch(`/user/api/user/deactivate/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadUsersData();
            loadStats();
            loadCharts();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Erro ao desativar usuário:', error);
        showToast('Erro ao desativar usuário', 'error');
    }
}

async function activateUser(userId, userName) {
    try {
        const response = await fetch(`/user/api/user/activate/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadUsersData();
            loadStats();
            loadCharts();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Erro ao ativar usuário:', error);
        showToast('Erro ao ativar usuário', 'error');
    }
}

function closeConfirmModal() {
    document.getElementById('confirmModal').classList.remove('show');
}

// Fechar modais ao clicar fora
window.onclick = function(event) {
    const confirmModal = document.getElementById('confirmModal');
    const userDetailsModal = document.getElementById('userDetailsModal');
    
    if (event.target === confirmModal) {
        closeConfirmModal();
    }
    if (event.target === userDetailsModal) {
        closeUserDetailsModal();
    }
}