function addProduto()
{
var produto = document.getElementById("produto").value
var quantidade = document.getElementById("quantidade").value
var preco = parseFloat(produto.split("_")[1])
soma = parseFloat(document.getElementById("final").value) + preco * parseFloat(quantidade)
document.getElementById("compras").value += produto.split("_")[0] + ',  R$' + preco + '  ' + quantidade +  ' unidades \r\n'
document.getElementById("final").value = soma
}

$(document).ready(function () {
      $('#produtos').DataTable({
        ajax: '/api/produto',
        columns: [
          {data: 'name'},
          {data: 'preco'},
          {data: 'categoria'},
        ],
        buttons: [
        {
        extend: 'excel',
        title:'',
        classname: 'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect'
        }]
      });
    });