// Assuming you have data from Python in this format
const pythonData = {
    labels: ['Label1', 'Label2', 'Label3'],
    values: [10, 20, 30],
};

// Get the canvas element
const ctx = document.getElementById('myChart').getContext('2d');

// Create a bar chart
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: pythonData.labels,
        datasets: [{
            label: 'Data from Python',
            data: pythonData.values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true
            }
        }
    }
});