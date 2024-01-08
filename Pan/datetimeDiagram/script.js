// script.js

// Function to fetch data from the server
async function fetchData() {
    try {
      const response = await fetch('http://localhost:3000/getDataByTime');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  
  // Function to create and render the chart
  async function createChart() {
    const data = await fetchData();
  
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.xValues,
        datasets: [{
          label: 'Data Values',
          data: data.yValues,
          borderColor: 'rgb(75, 192, 192)',
          borderWidth: 2,
          fill: false,
        }],
      },
      options: {
        responsive: false,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
          },
        },
      },
    });
  }
  
  // Call the createChart function when the page is loaded
  document.addEventListener('DOMContentLoaded', createChart);
  