const elemento = document.querySelector("#dadosGrafico");

const mediasSensor = JSON.parse(elemento.dataset.medias);
const unidadeSensor = elemento.dataset.unidade;
const canvas = document.querySelector("#graficoSensor");

if (canvas && mediasSensor.length > 0) {

    const datas = mediasSensor.map(item => {
        const [ano, mes, dia] = item.data.split("-");
        return `${dia}/${mes}/${ano}`;
    });

    const valores = mediasSensor.map(item => item.media);

    new Chart(canvas, {
        type: "line",

        data: {
            labels: datas,

            datasets: [{
                label: `Média diária (${unidadeSensor})`,
                data: valores,
                borderWidth: 2,
                tension: 0.3,
                fill: false
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Data"
                    }
                },

                y: {
                    title: {
                        display: true,
                        text: `Média (${unidadeSensor})`
                    }
                }
            }
        }
    });

} else if (canvas) {

    canvas.parentElement.innerHTML =
        "<p>Não existem dados suficientes para gerar o gráfico.</p>";

}
