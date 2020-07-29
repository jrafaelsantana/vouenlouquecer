import { Line, mixins } from "vue-chartjs";

export default {
  mixins: [mixins.reactiveProp],
  extends: Line,
  props: ['label', 'chartData', 'options', 'chartColors'],

  computed: {
    data: function () {
      return this.chartData;
    }
  },

  mounted () {
    this.renderLineChart();
  },

  methods: {
    renderLineChart () {
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
  },

  watch: {
    data: function () {
      this.renderLineChart();
    }
  }
};