document.addEventListener("DOMContentLoaded", function () {
  const livrosLista = document.getElementById("livros-lista");
  const modal = document.getElementById("modal");
  const closeModal = document.getElementById("closeModal");
  const qrcodeImg = document.getElementById("qrcode-img");

  // Fetch lista de livros
  fetch("http://localhost:5001/livros/")
    .then((response) => response.json())
    .then((data) => {
      data.livros.forEach((livro) => {
        const livroCard = document.createElement("div");
        livroCard.className = "livro-card";
        livroCard.innerHTML = `
                    <img src="${livro.url_capa}" alt="Capa do Livro">
                    <h3>${livro.titulo}</h3>
                    <p>Autor: ${livro.autor}</p>
                    <p>R$ ${livro.valor_unitario.toFixed(2)}</p>
                    <button class="comprar-btn" onclick="comprarLivro(${
                      livro.id
                    }, ${livro.valor_unitario})">Comprar</button>
                `;
        livrosLista.appendChild(livroCard);
      });
    })
    .catch((error) => console.error("Erro ao carregar livros:", error));

  // Abrir modal de compra com QR Code
  window.comprarLivro = function (idLivro, valor) {
    fetch("http://localhost:5001/vendas/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id_livro: idLivro, quantidade: 1 }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.qr_code_url) {
          qrcodeImg.src = `data:image/png;base64,${data.qr_code_url}`;
          modal.style.display = "flex";
        } else {
          alert("Erro ao gerar QR Code para o pagamento.");
        }
      })
      .catch((error) => console.error("Erro ao processar a compra:", error));
  };

  // Fechar o modal
  closeModal.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
    }
  });
});
