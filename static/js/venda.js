$(document).ready(function () {
    var table = $('#produtos').DataTable({
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


    table.MakeCellsEditable({
    "onUpdate": myCallbackFunction,
    "confirmationButton": {"cancelCss ": "button"},
    "columns": [0,1,2],
    "inputType":[
    {
    "column": 1,
    "type": "text"
    }]
    });
});

function addProduto()
{
var produto = document.getElementById("produto").value
var quantidade = document.getElementById("quantidade").value
var preco = parseFloat(produto.split("_")[1])
soma = parseFloat(document.getElementById("final").value) + preco * parseFloat(quantidade)
document.getElementById("compras").value += produto.split("_")[0] + ',  R$' + preco + '  ' + quantidade +  ' unidades \r\n'
document.getElementById("final").value = soma
}





function myCallbackFunction (updatedCell, updatedRow, oldValue) {
        console.log("The new value for the cell is: " + updatedCell.data());
        console.log("The values for each cell in that row are: " + updatedRow.data());
    }