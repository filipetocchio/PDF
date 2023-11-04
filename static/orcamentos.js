document.addEventListener('DOMContentLoaded', function () {
    carregarOrcamentos();
});

function carregarOrcamentos() {
    fetch('/get_orcamentos', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin'  // ou 'include' se estiver fazendo solicitações cross-origin
    })
    .then(response => response.json())
    .then(orcamentos => {
        const tabelaOrcamentos = document.getElementById('orcamento-list');
        tabelaOrcamentos.innerHTML = '';
        orcamentos.forEach(orcamento => {
            const dataFormatada = new Date(orcamento[8]).toLocaleDateString('pt-BR');
            const valorTotalFormatado = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(parseFloat(orcamento[7]));
            
            const linha = document.createElement('tr');
            linha.innerHTML = `
                <td>${orcamento[1]}</td>
                <td>${dataFormatada}</td>
                <td>${orcamento[3]}</td>
                <td>${valorTotalFormatado}</td>
                <td>
                    <button onclick="editarOrcamento(${orcamento[0]})">Editar</button>
                    <button onclick="excluirOrcamento(${orcamento[0]})">Excluir</button>
                    <button onclick="gerarPDF(${orcamento[0]})">Gerar PDF</button>
                </td>
            `;
            tabelaOrcamentos.appendChild(linha);
        });
    })
    .catch(error => console.error('Erro ao carregar orçamentos:', error));
}



function editarOrcamento(id) {
    // Redireciona para a página de edição do orçamento
    window.location.href = `/editar_orcamento/${id}`;
}

function excluirOrcamento(id) {
    if (confirm('Tem certeza de que deseja excluir este orçamento?')) {
        fetch(`/delete_orcamento/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                alert('Orçamento excluído com sucesso!');
                carregarOrcamentos();
            } else {
                alert('Erro ao excluir orçamento. Por favor, tente novamente.');
            }
        })
        .catch(error => console.error('Erro ao excluir orçamento:', error));
    }
}

function gerarPDF(id) {
    // Implemente a lógica para gerar um PDF do orçamento
    window.location.href = `/gerar_pdf/${id}`;
}

