<template>
  <div class="container-fluid">
    <div class="row mt-5 ml-4 mr-4">
      <div class="col mr-4 pt-4 card text-center">
        <h5>Sensor Temperatura</h5>
        <div class="card-body">
          <img
            src="./assets/icons/temperatura_ideal.png"
            alt="icone temperatura"
            style="max-width: 30%; height: auto;"
          />
          <h2 class="card-text mt-2">{{currentTemperature}} ºc</h2>
        </div>
      </div>
      <div class="col mr-4 pt-4 card text-center">
        <h5>Sensor PH</h5>
        <div class="card-body">
          <img
            src="./assets/icons/ph_neutro.png"
            alt="icone temperatura"
            style="max-width: 30%; height: auto;"
          />
          <h2 class="card-text mt-2">{{currentPH}}</h2>
        </div>
      </div>
      <div class="col mr-4 pt-4 card text-center">
        <h5>Oxigênio Dissolvido</h5>
        <div class="card-body">
          <img
            src="./assets/icons/oxygen.png"
            alt="icone temperatura"
            style="max-width: 30%; height: auto;"
          />
          <h2 class="card-text mt-2">{{currentOxygen}} mg/l</h2>
        </div>
      </div>
      <div class="col mr-4 pt-4 card text-center">
        <h5>Threshold Temperatura</h5>
        <div class="row mt-4 pl-2 pr-2">
          <div class="col">
            <div class="input-group input-group-sm mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroup-sizing-sm">Min</span>
              </div>
              <input
                type="text"
                class="form-control"
                aria-label="Small"
                aria-describedby="inputGroup-sizing-sm"
                v-model="temperatureThreshold.min"
                disabled
              />
            </div>
            <input
              type="range"
              class="custom-range"
              v-model="temperatureThreshold.min"
              min="20"
              max="28"
              step="0.5"
            />
          </div>
          <div class="col">
            <div class="input-group input-group-sm mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroup-sizing-sm">Max</span>
              </div>
              <input
                type="text"
                class="form-control"
                aria-label="Small"
                aria-describedby="inputGroup-sizing-sm"
                v-model="temperatureThreshold.max"
                disabled
              />
            </div>
            <input
              type="range"
              class="custom-range"
              v-model="temperatureThreshold.max"
              min="29"
              max="36"
              step="0.5"
            />
          </div>
        </div>
        <div class="row mt-2 pl-5 pr-5 justify-content-center mb-2">
          <button class="btn btn-outline-primary btn-block">Configurar</button>
        </div>
      </div>
      <div class="col pt-4 pb-4 card text-center">
        <h5>Threshold PH</h5>
        <div class="row mt-4 pl-2 pr-2">
          <div class="col">
            <div class="input-group input-group-sm mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroup-sizing-sm">Min</span>
              </div>
              <input
                type="text"
                class="form-control"
                aria-label="Small"
                aria-describedby="inputGroup-sizing-sm"
                v-model="phThreshold.min"
                disabled
              />
            </div>
            <input
              type="range"
              class="custom-range"
              v-model="phThreshold.min"
              min="4"
              max="6"
              step="0.1"
            />
          </div>
          <div class="col">
            <div class="input-group input-group-sm mb-3">
              <div class="input-group-prepend">
                <span class="input-group-text" id="inputGroup-sizing-sm">Max</span>
              </div>
              <input
                type="text"
                class="form-control"
                aria-label="Small"
                aria-describedby="inputGroup-sizing-sm"
                v-model="phThreshold.max"
                disabled
              />
            </div>
            <input
              type="range"
              class="custom-range"
              v-model="phThreshold.max"
              min="7"
              max="9"
              step="0.1"
            />
          </div>
        </div>
        <div class="row mt-2 pl-5 pr-5 justify-content-center mb-2">
          <button class="btn btn-outline-primary btn-block">Configurar</button>
        </div>
      </div>
    </div>
    <div class="row mt-4 ml-4 mr-4">
      <div class="col card mr-4 pt-3 pb-3" v-if="temperatureChartData.length > 0">
        <line-chart
          :chartData="temperatureChartData"
          :options="temperatureChartOptions"
          label="Temperatura"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import LineChart from "./components/LineChart";

export default {
  name: "app",
  components: {
    LineChart,
  },
  data() {
    return {
      url: "http://localhost:5000",
      currentTemperature: 0,
      currentPH: 0,
      currentOxygen: 0,
      temperatureThreshold: {
        min: 0,
        max: 0,
      },
      phThreshold: {
        min: 0,
        max: 0,
      },
      temperatureChartData: [],
      phChartData: [],
      oxygenChartData: [],
      temperatureChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [
            {
              ticks: {
                suggestedMin: 26,
                suggestedMax: 27.5,
              },
            },
          ],
        },
      },
      phChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [
            {
              ticks: {
                suggestedMin: 7.6,
                suggestedMax: 8.4,
              },
            },
          ],
        },
      },
      oxygenChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [
            {
              ticks: {
                suggestedMin: 5,
                suggestedMax: 7.5,
              },
            },
          ],
        },
      },
      lastReadingTime: "",
    };
  },
  methods: {
    async getCurrentLog() {
      const { data } = await axios.get(this.url + "/lastreading");

      let currTime = data.ph.time;
      if (this.lastReadingTime !== currTime) {
        this.lastReadingTime = currTime;
        this.currentTemperature = data.temperature.value;
        this.currentOxygen = data.oxygen.value;
        this.currentPH = data.ph.value;
      }

      let auxPhThreshold = data.ph.threshold;
      let auxTempThreshold = data.temperature.threshold;
      if (
        auxPhThreshold.min !== this.phThreshold.min ||
        auxPhThreshold.max !== this.phThreshold.max ||
        auxTempThreshold.min !== this.temperatureThreshold.min ||
        auxTempThreshold.max !== this.temperatureThreshold.max
      ) {
        this.temperatureThreshold = data.temperature.threshold;
        this.phThreshold = data.ph.threshold;
      }

      // Teste, atualizando os dados do grafico de temperatura para ver
      // se ele tambem atualiza
      this.temperatureChartData = this.updateChartData(
        this.temperatureChartData,
        this.currentTemperature,
        currTime
      );
    },

    updateChartData(arrChart, currValue, currDate) {
      arrChart = arrChart.slice(1, 10);
      let date = moment(currDate, "DD-MM-YYYY HH:mm:ss").format("mm:ss");
      arrChart.push({ date, total: currValue });
      return arrChart;
    },
    formatChartData(arrValue, arrDate) {
      let arrAux = [];
      for (let i = 0; i < arrValue.length; i++) {
        let date = moment(arrDate[i], "DD-MM-YYYY HH:mm:ss").format("mm:ss");
        arrAux.push({ date, total: arrValue[i] });
      }
      return arrAux;
    },
  },
  async mounted() {
    const { data } = await axios.get(this.url + "/log?amount=10");

    this.temperatureChartData = this.formatChartData(
      data.temperature.value,
      data.temperature.time
    );
    this.oxygenChartData = this.formatChartData(
      data.oxygen.value,
      data.oxygen.time
    );
    this.phChartData = this.formatChartData(data.ph.value, data.ph.time);

    await this.getCurrentLog();
  },
};
</script>

<style>
.card_config {
  height: 100px;
  width: 200px;
}

.card_icons {
  height: 200px;
  width: 200px;
}
</style>