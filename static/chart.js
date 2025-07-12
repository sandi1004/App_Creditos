const colores = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'];
let chart;

document.addEventListener('DOMContentLoaded', () => {
    const filtro = document.getElementById('filtroGrafica');
    if (filtro) {
        cargarGrafica(filtro.value);

        filtro.addEventListener('change', () => {
            if (chart) chart.destroy();
            cargarGrafica(filtro.value);
        });
    } else {
        cargarGrafica('cliente');
    }
});

function cargarGrafica(tipo) {
    fetch('/datos')
        .then(res => res.json())
        .then(data => {
            let labels = [], valores = [];

            if (tipo === 'cliente') {
                const agrupado = {};
                data.forEach(([cliente, monto]) => {
                    agrupado[cliente] = (agrupado[cliente] || 0) + monto;
                });

                labels = Object.keys(agrupado);
                valores = Object.values(agrupado);

                // Agrupar si hay más de 15 clientes
                if (labels.length > 15) {
                    const combinados = labels.map((l, i) => ({ cliente: l, monto: valores[i] }));
                    combinados.sort((a, b) => b.monto - a.monto);
                    const top15 = combinados.slice(0, 15);
                    const resto = combinados.slice(15);
                    const otrosMonto = resto.reduce((suma, c) => suma + c.monto, 0);
                    labels = top15.map(c => c.cliente).concat("Otros");
                    valores = top15.map(c => c.monto).concat(otrosMonto);
                }

            } else if (tipo === 'rango') {
                const rangos = {
                    '0-1000': 0,
                    '1001-5000': 0,
                    '5001-10000': 0,
                    '10001-20000': 0,
                    '20001+': 0
                };

                data.forEach(([_, monto]) => {
                    if (monto <= 1000) rangos['0-1000'] += monto;
                    else if (monto <= 5000) rangos['1001-5000'] += monto;
                    else if (monto <= 10000) rangos['5001-10000'] += monto;
                    else if (monto <= 20000) rangos['10001-20000'] += monto;
                    else rangos['20001+'] += monto;
                });

                labels = Object.keys(rangos);
                valores = Object.values(rangos);
            }

            const ctx = document.getElementById('grafica').getContext('2d');
            chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        label: tipo === 'cliente' ? 'Total por cliente' : 'Total por rango de monto',
                        data: valores,
                        backgroundColor: labels.map((_, i) => colores[i % colores.length])
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                boxWidth: 20,
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.label}: $${ctx.formattedValue}`
                            }
                        }
                    }
                }
            });
        });
}
