import Vue from 'vue'
import VueCodemirror from 'vue-codemirror'

import App from './App.vue'

import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/theme/base16-dark.css'
import './index.css'


Vue.config.productionTip = false

Vue.use(VueCodemirror)
new Vue({
  render: h => h(App),
}).$mount('#app')
