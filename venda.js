function addProduto()
{
var produto = document.getElementById("produto").value
var quantidade = document.getElementById("quantidade").value
console.log('dasda')
document.getElementById("compras").value += produto + '  ' + quantidade + '|| \r\n'
}