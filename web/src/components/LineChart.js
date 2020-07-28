import { Line, mixins } from "vue-chartjs";

export default {
  mixins: [mixins.reactiveProp],
  extends: Line,
  props: {
    label: {
      type: String
    },
    chartData: {
      type: Array
    },
    options: {
      type: Object
    },
    chartColors: {
      type: Object
    }
  },
  mounted() {
    const dates = this.chartData.map(d => d.date);
    const totals = this.chartData.map(d => d.total);

    this.renderChart(
      {
        labels: dates,
        datasets: [
          {
            label: this.label,
            data: totals,
          }
        ]
      },
      this.options
    );
  }
};