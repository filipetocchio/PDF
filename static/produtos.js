async function fetchProdutos() {
  try {
    const response = await fetch('http://localhost:5000/get_produtos');
    const produtos = await response.json();
    const productList = document.getElementById('product-list');
    produtos.forEach(produto => {
      const productRow = document.createElement('tr');
      productRow.className = 'product-item';
      productRow.innerHTML = `
        <td>${produto.id}</td>
        <td>${produto.nome}</td>
        <td><img src="${produto.imagem}" alt="${produto.nome}" width="100"></td>
      `;
      productList.appendChild(productRow);
    });
  } catch (error) {
    console.error('Erro ao buscar produtos:', error);
  }
}

fetchProdutos();

document.getElementById('searchInput').addEventListener('input', function() {
  const searchValue = this.value.toLowerCase();
  const productItems = document.querySelectorAll('.product-item');
  productItems.forEach(item => {
    const nome = item.children[1].textContent.toLowerCase();
    const id = item.children[0].textContent.toLowerCase();
    const isVisible = nome.includes(searchValue) || id.includes(searchValue);
    item.style.display = isVisible ? '' : 'none';
  });
});
<script src="{{ url_for('static', filename='produtos.js') }}" defer></script>
