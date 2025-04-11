// Variável global para armazenar os textos
let textos = JSON.parse(localStorage.getItem('textos')) || [];
let editandoId = null; // Armazena o ID do item em edição

// Função para salvar/editar textos
function salvarTexto() {
    const titulo = document.getElementById('titulo').value;
    const texto = document.getElementById('texto').value;
    const traducao = document.getElementById('traducao').value;

    if (!titulo || !texto || !traducao) {
        alert('Preencha todos os campos!');
        return;
    }

    // Se estiver editando
    if (editandoId !== null) {
        textos[editandoId] = { titulo, texto, traducao }; // Atualiza o item existente
        editandoId = null; // Reseta o ID de edição
    } else {
        textos.push({ titulo, texto, traducao }); // Adiciona novo item
    }

    localStorage.setItem('textos', JSON.stringify(textos));
    buscarTexto(); // Atualiza a lista

    // Limpa os campos
    document.getElementById('titulo').value = '';
    document.getElementById('texto').value = '';
    document.getElementById('traducao').value = '';
}

// Função para buscar textos
function buscarTexto() {
    const termo = document.getElementById('busca').value.toLowerCase();
    const resultados = textos.filter((item, index) => {
        item.id = index; // Adiciona o ID original ao item
        return (
            item.titulo.toLowerCase().includes(termo) ||
            item.texto.toLowerCase().includes(termo) ||
            item.traducao.toLowerCase().includes(termo)
        );
    });

    const divResultados = document.getElementById('resultados');
    divResultados.innerHTML = '';

    resultados.forEach(item => {
        divResultados.innerHTML += `
            <div style="margin: 20px 0; padding: 10px; border: 1px solid #ddd;">
                <h3>${item.titulo}</h3>
                <p><strong>Original:</strong> ${item.texto}</p>
                <p><strong>Tradução:</strong> ${item.traducao}</p>
                <button onclick="editarTexto(${item.id})">✏️ Editar</button>
                <button onclick="excluirTexto(${item.id})">🗑️ Excluir</button>
            </div>
        `;
    });
}

// Função para excluir textos
function excluirTexto(id) {
    textos.splice(id, 1); // Remove pelo ID original
    localStorage.setItem('textos', JSON.stringify(textos));
    buscarTexto(); // Atualiza a lista
}

// Função para editar textos
function editarTexto(id) {
    const item = textos[id];
    // Preenche os campos com os dados do item
    document.getElementById('titulo').value = item.titulo;
    document.getElementById('texto').value = item.texto;
    document.getElementById('traducao').value = item.traducao;
    editandoId = id; // Define o ID em edição
}