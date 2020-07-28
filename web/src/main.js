import Vue from "vue";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.css";
import axios from 'axios' // we import axios from installed dependencies

Vue.config.productionTip = false

Vue.use(axios) // we register axios globally
new Vue({
  render: (h) => h(App),
}).$mount("#app");
