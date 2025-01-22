<template>
  <div class="container-fluid bg-light">
    <div class="page-header">
      <b-navbar toggleable="md" type="light" sticky>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand to="/home">DASHBOARD</b-navbar-brand>
        <b-collapse is-nav id="nav_collapse" class="py-2" v-if="loggedIn">
          <b-navbar-nav>
            <b-nav-item to="/home">Все устройства <span v-if="menuInfo.asicCount">({{menuInfo.asicCount}})</span></b-nav-item>
            <b-nav-item to="/dashboard">Устройства с ошибками <span v-if="menuInfo.errorAsicCount">({{menuInfo.errorAsicCount}})</span>
            </b-nav-item>
            <b-nav-item to="/balance">Баланс</b-nav-item>
            <b-nav-item to="/error_rules">Правила</b-nav-item>
            <!--<b-nav-item to="/errors">Тип ошибки <span v-if="menuInfo.errorCount">({{menuInfo.errorCount}})</span></b-nav-item>-->
            <!--<b-nav-item to="/warnings">Нужно решить <span v-if="menuInfo.warningCount">({{menuInfo.warningCount}})</span></b-nav-item>-->
            <b-nav-item :href="menuInfo.flowerUrl" target="blank">Мониторинг автоматического обновления</b-nav-item>
            <b-nav-item :href="menuInfo.adminUrl" target="blank">Админка</b-nav-item>
            <b-nav-item to="/logout">Выход</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <div class="col-md-4 clearfix">

      <b-alert v-for="alert in alerts" :variant="alert.variant" dismissible @dismissed="dismissAlert(alert)" :show="30">
        {{alert.message}}
      </b-alert>
    </div>


    <slot/>
  </div>
</template>

<script>
  import {mapState, mapGetters, mapActions} from 'vuex';

  export default{
    name: 'Layout',
    computed: {
      ...mapState('utils', [
        'menuInfo',
      ]),
      ...mapState('alerts', [
        'alerts',
      ]),
      ...mapGetters('auth', [
          'loggedIn'
      ]),
    },
    methods: {
      dismissAlert(alert){
        this.$store.dispatch('alerts/deleteAlert', alert)
      }
    }
  }
</script>
