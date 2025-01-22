// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store';
import validateMixins from './mixins/validateMixins'
import filters from './mixins/filters'
import asicMethods from './mixins/asicMethods'

import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);
Vue.config.productionTip = false
Vue.mixin(validateMixins)
Vue.mixin(filters)
Vue.mixin(asicMethods)
Vue.prototype.$eventBus = new Vue()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
