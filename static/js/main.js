// JavaScript principal para o Sistema de Portaria

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmar exclusões
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este registro?')) {
                e.preventDefault();
            }
        });
    });

    // Máscara para campos de data
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Definir data atual como padrão se estiver vazio
        if (!input.value) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });

    // Máscara para campos de hora
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(function(input) {
        // Definir hora atual como padrão se estiver vazio
        if (!input.value) {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            input.value = `${hours}:${minutes}`;
        }
    });

    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Busca em tempo real para tabelas
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const table = document.querySelector(this.dataset.target);
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    });

    // Atualizar campos de placa automaticamente (maiúsculo)
    const placaInputs = document.querySelectorAll('input[name="placa"]');
    placaInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });

    // Função para formatar data brasileira
    window.formatDateBR = function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    };

    // Função para formatar hora
    window.formatTime = function(timeString) {
        if (!timeString) return '';
        return timeString.substring(0, 5); // Remove segundos se houver
    };

    // Função para confirmar ações
    window.confirmAction = function(message) {
        return confirm(message || 'Tem certeza que deseja realizar esta ação?');
    };

    // Função para mostrar loading
    window.showLoading = function(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Processando...';
        button.disabled = true;
        
        return function() {
            button.innerHTML = originalText;
            button.disabled = false;
        };
    };

    // Função para validar placa de veículo
    window.validatePlaca = function(placa) {
        // Formato antigo: ABC-1234 ou novo: ABC1D23
        const oldFormat = /^[A-Z]{3}-?\d{4}$/;
        const newFormat = /^[A-Z]{3}\d[A-Z]\d{2}$/;
        
        return oldFormat.test(placa) || newFormat.test(placa);
    };

    // Auto-complete para campos comuns
    setupAutoComplete();
});

// Função para configurar auto-complete
function setupAutoComplete() {
    // Esta função pode ser expandida para incluir auto-complete
    // baseado em dados históricos do banco de dados
    
    const empresaInputs = document.querySelectorAll('input[name="empresa"]');
    empresaInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            // Aqui poderia ser implementado um auto-complete
            // buscando empresas já cadastradas
        });
    });
}

// Função para imprimir relatórios
window.printReport = function() {
    window.print();
};

// Função para exportar dados (pode ser expandida)
window.exportData = function(format) {
    alert('Funcionalidade de exportação em desenvolvimento para o formato: ' + format);
};

// Função para atualizar página automaticamente (opcional)
window.autoRefresh = function(interval) {
    if (interval && interval > 0) {
        setInterval(function() {
            location.reload();
        }, interval * 1000);
    }
};
