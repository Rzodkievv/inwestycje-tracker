<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>Tracker inwestycji</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: Arial; padding: 20px; background: #f5f5f5; }
table { border-collapse: collapse; width: 100%; background: white; margin-bottom: 20px; }
th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
th { background: #333; color: white; }
canvas { background: white; padding: 20px; }
input, button { padding: 5px; margin: 5px; }
</style>
</head>
<body>

<h2>Mój portfel</h2>

<form id="addStockForm">
<input type="text" id="name" placeholder="Nazwa spółki" required>
<input type="text" id="ticker" placeholder="Ticker (np. AAPL lub PEO.WA)" required>
<input type="number" id="shares" placeholder="Ilość" required>
<input type="number" id="buyPrice" placeholder="Cena zakupu (PLN/USD)" required>
<select id="currency">
<option value="USD">USD</option>
<option value="PLN">PLN</option>
</select>
<button type="submit">Dodaj spółkę</button>
</form>

<table>
<tr>
<th>Spółka</th>
<th>Ilość</th>
<th>Cena zakupu (PLN)</th>
<th>Aktualna cena (PLN)</th>
<th>Wartość (PLN)</th>
<th>Zysk/Strata (PLN)</th>
</tr>
<tbody id="table"></tbody>
</table>

<canvas id="chart"></canvas>

<script>
const BACKEND_URL = "https://inwestycje-tracker.onrender.com"; // Twój backend
let portfolio = [];
let chartInstance = null;

// Kurs USD → PLN
async function getUSDPLN() {
    try {
        const res = await fetch("https://api.exchangerate.host/latest?base=USD&symbols=PLN");
        const data = await res.json();
        return parseFloat(data.rates.PLN);
    } catch {
        return 1;
    }
}

// Pobranie ceny z backendu
async function getPrice(symbol) {
    try {
        const res = await fetch(`${BACKEND_URL}/get_price?symbol=${symbol}`);
        const data = await res.json();
        return data.price || 0;
    } catch {
        return 0;
    }
}

// Render tabeli i wykresu
async function render() {
    const table = document.getElementById("table");
    table.innerHTML = "";
    const usdToPln = await getUSDPLN();
    let labels = [];
    let values = [];

    for (let stock of portfolio) {
        if(!stock.tempPrice) {
            stock.tempPrice = await getPrice(stock.ticker);
        }

        const pricePLN = stock.currency === "USD" ? stock.tempPrice * usdToPln : stock.tempPrice;
        const buyPricePLN = stock.buyPrice * (stock.currency === "USD" ? usdToPln : 1);
        const value = stock.shares * pricePLN;
        const cost = stock.shares * buyPricePLN;
        const profit = value - cost;

        labels.push(stock.name);
        values.push(value);

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${stock.name}</td>
            <td>${stock.shares}</td>
            <td>${buyPricePLN.toFixed(2)}</td>
            <td>${pricePLN ? pricePLN.toFixed(2) : "Ładuję..."}</td>
            <td>${value.toFixed(2)}</td>
            <td style="color:${profit>=0?'green':'red'}">${profit.toFixed(2)}</td>
        `;
        table.appendChild(row);
    }

    const ctx = document.getElementById("chart");
    if(chartInstance) chartInstance.destroy();
    chartInstance = new Chart(ctx, {
        type: "pie",
        data: { labels, datasets: [{ data: values, backgroundColor: ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f'] }] },
        options: { responsive:true, plugins: { legend: { position: 'bottom' } } }
    });
}

// Dodawanie spółki
document.getElementById("addStockForm").addEventListener("submit", e=>{
    e.preventDefault();
    const name = document.getElementById("name").value;
    const ticker = document.getElementById("ticker").value.toUpperCase();
    const shares = parseFloat(document.getElementById("shares").value);
    const buyPrice = parseFloat(document.getElementById("buyPrice").value);
    const currency = document.getElementById("currency").value;

    portfolio.push({name, ticker, shares, buyPrice, currency, tempPrice:null});
    e.target.reset();
    render();
});

window.addEventListener("DOMContentLoaded", render);
</script>

</body>
</html>
