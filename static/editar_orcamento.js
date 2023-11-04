document.getElementById('editOrcamentoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Prepare o formData como um objeto contendo todas as entradas do formulário
    let formData = {};
    const formElements = this.elements;
    for (let element of formElements) {
        if (element.name && element.tagName !== 'BUTTON') {
            formData[element.name] = element.value;
        }
    }

    // Encontrar o id do orçamento na URL ou em um campo oculto se necessário
    const orcamentoId = window.location.pathname.split('/').pop(); // Supondo que a ID está na URL

    // Adicione uma chamada fetch para enviar os dados atualizados
    fetch(`/editar_orcamento/${orcamentoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            alert('Orçamento atualizado com sucesso!');
            window.location.href = '/lista_orcamentos'; // Ou a rota que mostra os orçamentos
        } else {
            alert('Erro ao atualizar orçamento. Por favor, tente novamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar orçamento:', error);
        alert('Erro ao atualizar orçamento. Por favor, verifique a conexão e tente novamente.');
    });
});
