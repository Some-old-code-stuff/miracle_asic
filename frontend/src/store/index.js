/**
 * Created by mrakolice on 11.09.18.
 */

import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/auth'
import asics from './modules/asics'
import alerts from './modules/alerts'
import errors from './modules/errors'
import utils from './modules/utils'
import asicSettings from './modules/asicSettings'
import balance from './modules/balance'
import errorRules from './modules/errorRules'

Vue.use(Vuex)
const modules = {
  auth,
  asics,
  alerts,
  errors,
  utils,
  asicSettings,
  balance,
  errorRules
}

const store = new Vuex.Store({
  modules,
  strict: process.env.NODE_ENV !== 'production',
})

// Automatically run the `init` action for every module,
// if one exists.
for (const moduleName of Object.keys(modules)) {
  if (modules[moduleName].actions && modules[moduleName].actions.init) {
    store.dispatch(`${moduleName}/init`)
  }
}
export default store
