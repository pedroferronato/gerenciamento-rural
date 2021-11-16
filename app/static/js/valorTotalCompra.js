var valor_unitario = document.getElementById('valor_unitario')
var quantidade = document.getElementById('quantidade')
var desconto = document.getElementById('desconto')
var valor_total = document.getElementById('valor_total')

function definir_valor_total() {
    desconto.value = desconto.value.trim().replace(',', '.');
    if (isNaN(desconto.value.replaceAll('%', ''))) return;
    quantidade.value = quantidade.value.trim().replace(',', '.');
    if (isNaN(quantidade.value)) return;
    valor_unitario.value = valor_unitario.value.trim().replace(',', '.');
    if (isNaN(valor_unitario.value)) return;

    var valor_final = parseFloat(quantidade.value) * parseFloat(valor_unitario.value, 2)
    
    if (desconto.value != null && desconto.value != "") {
        if (desconto.value.includes('%')) {
            let desconto_bruto = desconto.value.replaceAll('%', '')
            desconto_total = (valor_final * desconto_bruto) / 100
            valor_final -= desconto_total
        } else valor_final -= parseFloat(desconto.value, 2);
    }
    if (isNaN(valor_final)) valor_final = "";
    if (!isNaN(valor_final) && valor_final > 0) valor_final = valor_final.toFixed(2);
    valor_total.value = valor_final.toString();
}

valor_unitario.addEventListener('input', () => { definir_valor_total() })
quantidade.addEventListener('input', () => { definir_valor_total() })
desconto.addEventListener('input', () => { definir_valor_total() })