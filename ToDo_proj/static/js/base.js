/**
 * Função para exibir toast de feedback
 */
function showToast(message, type = 'success') {
    // Criar elemento de toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Adicionar ao body
    document.body.appendChild(toast);
    
    // Mostrar toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Inicializar toasts para mensagens do Django
 */
function initializeDjangoMessages() {
    // Esta função será chamada pelo template com as mensagens do Django
    window.showDjangoToast = function(message, tags) {
        showToast(message, tags);
    };
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeDjangoMessages();
});