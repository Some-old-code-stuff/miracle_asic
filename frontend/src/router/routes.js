/**
 * Created by mrakolice on 25.09.18.
 */


import HomeView from './views/HomeView'
import MaksView from './views/MaksView'
import ErrorView from './views/ErrorView'
import DashboardView from './views/DashboardView'
import ErrorRuleView from './views/ErrorRuleView'
import LoginView from './views/LoginView'
import BalanceView from './views/BalanceView'
import store from '../store/index'

export default [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    beforeEnter(routeTo, routeFrom, next) {
      // If the user is already logged in
      if (store.getters['auth/loggedIn']) {
        // Redirect to the home page instead
        next({name: 'home'})
      } else {
        // Continue to the login page
        next()
      }
    },
  },
  {
    path: '/logout',
    name: 'logout',
    meta: {
      authRequired: true,
    },
    beforeEnter(routeTo, routeFrom, next) {
      store.dispatch('auth/logout')
      const authRequiredOnPreviousRoute = routeFrom.matched.some(
        route => route.meta.authRequired
      )
      // Navigate back to previous page, or home as a fallback
      next(authRequiredOnPreviousRoute ? { name: 'login' } : { ...routeFrom })
    },
  },
  {
    path: '/404',
    name: '404',
    component: require('./views/404').default,
    // Allows props to be passed to the 404 page through route
    // params, such as `resource` to define what wasn't found.
    props: true,
  },
  // Redirect any unmatched routes to the 404 page. This may
  // require some server configuration to work in production:
  // https://router.vuejs.org/en/essentials/history-mode.html#example-server-configurations
  {
    path: '*',
    redirect: '404',
  },
  {
    path: '/',
    redirect: '/home',
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/maks',
    name: 'maks',
    component: MaksView,
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/error_rules',
    name: 'error_rules',
    component: ErrorRuleView,
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/errors',
    name: 'Errors',
    component: ErrorView,
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/warnings',
    name: 'Warnings',
    component: ErrorView,
    props: {warnings: true},
    meta: {
      authRequired: true,
    },
  },
  {
    path: '/balance',
    name: 'balance',
    component: BalanceView,
    meta: {
      authRequired: true,
    },
  },
]
