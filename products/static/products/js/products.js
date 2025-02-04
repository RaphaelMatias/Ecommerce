document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/products/');
        const products = await response.json();
        const container = document.getElementById('products-container');

        products.forEach(product => {
            const card = document.createElement('div');
            card.className = 'col';
            card.innerHTML = `
                <div class="card shadow-sm border-light h-100">
                    <img src="${product.image}" 
                        class="card-img-top" 
                        alt="${product.name}"
                        style="height: 250px; object-fit: contain">
                    
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text flex-grow-1">${truncateText(product.description, 20)}</p>
                        <div class="mt-3">
                            <p class="card-text fw-bold fs-4 text-primary">
                                R$ ${product.final_price.toFixed(2)}
                            </p>
                            <a href="/product/${product.id}/" class="btn btn-primary">Ver Detalhes</a>
                        </div>
                    </div>
                </div>
            `;
            
            container.appendChild(card);
        });

    } catch (error) {
        console.error("Erro:", error);
        container.innerHTML = `
            <div class="alert alert-danger">
                Falha ao carregar produtos. Tente recarregar a página.
            </div>
        `;
    }
});

function truncateText(text, maxWords) {
    const words = text.split(' ');
    return words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
}