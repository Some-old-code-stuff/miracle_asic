<template>
  <Layout>
    <div class="row">
      <div v-for="asic in dashboardAsics" class="col-md-4 card">
        <div class="card-body row">
          <div class="col">
            <h4>
              <span>{{asic.asicName}}</span>
              <span class="fa fa-signal" :class="have_connect_error(asic)"
                    :title="have_connect_error_title(asic)">
              </span>
              <span class="fa fa-exclamation red-icon" title="Автообновление выключено!"
                    v-if="asic.stopUpdate">
              </span>
              <span class="fa fa-asterisk red-icon" :title="'Ошибок: '+asic.openErrors.length"
                    v-if="asic.openErrors && asic.openErrors.length>0">
              </span>
              <span class="fa fa-asterisk yellow-icon"
                    :title="'Уведомлений: '+asic.openWarnings.length"
                    v-if="asic.openWarnings && asic.openWarnings.length>0">
              </span>
            </h4>
            <h4><span class="grey-color">{{ asic.defaultRate }}</span></h4>
            <h4>{{ asic.hostName }}</h4>
            <h4>
              <a :href="'http://'+asic.ipAddress" target="_blank">{{ asic.ipAddress}}</a></h4>
            <h4>
              <span v-if="haveErrorsWithWarnings('btn-', asic, FieldName.FULL_RATE) != 'btn-success'"
                    class="btn font-weight-bold m-1 p-1" :class="haveErrorsWithWarnings('badge-', asic, FieldName.FULL_RATE)"
                    @click.stop="openErrors(asic, FieldName.FULL_RATE)">
              {{asic.fullRate}}</span>
              <span v-else class="btn btn-success font-weight-bold m-1 p-1">{{asic.fullRate}}</span>
            </h4>
            <h5>Статус пула
              <span v-if="haveErrors('btn-', asic, FieldName.POOL_STATUS) != 'btn-success'"
                    class="btn font-weight-bold m-1 p-1" :class="haveErrors('btn-', asic, FieldName.POOL_STATUS)"
                    @click.stop="openErrors(asic, FieldName.POOL_STATUS)"
              >{{ asic.poolStatus}}</span>
              <span v-else class="btn btn-success font-weight-bold m-1 p-1">{{ asic.poolStatus}}</span>
            </h5>
            <h5 v-b-tooltip.hover :title="asic.poolAddress">Адрес
              пула: {{asic.poolAddress | truncate(8) }}</h5>
            <h5 v-b-tooltip.hover :title="asic.poolUsername">Пользователь на
              пуле: {{asic.poolUsername | truncate(8) }}</h5>

            <a @click.stop="closeErrors(asic)" class="btn btn-light btn-issa" title="Проблемы решены">
              <span class="fa fa-check"></span>
            </a>
            <a @click.stop="update(asic)" class="btn btn-light btn-issa" title="Обновить">
              <span class="fa fa-repeat"></span>
            </a>
            <a @click.stop="reboot(asic)" class="btn btn-light btn-issa" title="Перезагрузка">
              <span class="fa fa-refresh"></span>
            </a>
            <a class="btn btn-light btn-issa" title="Настройки" @click.stop="openSettings(asic)">
              <span class="fa fa-cog"></span>
            </a>
            <a class="btn btn-light btn-issa" title="Возобновить обновление" @click.stop="resumeUpdate(asic)"
               v-if="asic.stopUpdate">
              <span class="fa fa-play"></span>
            </a>
            <a class="btn btn-light btn-issa" title="Остановить обновление" @click.stop="stopUpdate(asic)" v-else>
              <span class="fa fa-pause"></span>
            </a>
          </div>
          <div class="col">
            <div class="row">
              <span class="col badge grey-color no-background">&#8451;</span>
              <span class="col badge grey-color no-background">Частота</span>
              <span class="col badge grey-color no-background">Мощн.</span>
              <span class="col badge grey-color no-background">Чипы</span>
            </div>
            <div v-for="chain in asic.chains" class="">
              <div class="row">
                <span class="col m-1 p-1 btn btn-sm font-weight-bold"
                      :class="haveErrors('btn-', asic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                      v-if="haveErrors('btn-', asic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)!='btn-success'"
                      @click.stop="openErrors(asic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                >{{ chain.temperature}}</span>
                <span v-else class="col m-1 p-1 btn btn-sm font-weight-bold btn-success">
                  {{ chain.temperature}}</span>
                <span class="col m-1 p-1 btn btn-sm font-weight-bold btn-primary">{{ chain.frequency }}</span>
                <span class="col m-1 p-1 btn btn-sm font-weight-bold btn-primary">{{ chain.rate }}</span>

                <span class="col m-1 p-1 btn btn-sm font-weight-bold"
                      :class="haveErrors('btn-', asic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)"
                      v-if="haveErrors('btn-', asic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)!='btn-success'"
                      @click.stop="openErrors(asic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)"
                >{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
                <span v-else class="col m-1 p-1 btn btn-sm font-weight-bold btn-success">{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
              </div>
              <div class="clearfix"></div>
              <b-progress class="row" :max="chain.allChips">
                <b-progress-bar variant="success" :value="chain.workingChips"></b-progress-bar>
                <b-progress-bar variant="danger" :value="chain.wrongChips"></b-progress-bar>
              </b-progress>
            </div>
            <div class="row">
              <span v-if="haveErrors('btn-', asic, FieldName.FAN_INFO_SPEED, fanInfo.id)!='btn-success'"
                    v-for="fanInfo in asic.fans" class="m-1 p-1 btn btn-sm font-weight-bold"
                    :class="haveErrors('btn-', asic, FieldName.FAN_INFO_SPEED, fanInfo.id)"
                    @click.stop="openErrors(asic, FieldName.FAN_INFO_SPEED, fanInfo.id)"
              >{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
              <span v-else class="m-1 p-1 btn btn-sm font-weight-bold btn-success">{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <error-modal ref="errorModal"></error-modal>
    <settings-modal ref="settingsModal"></settings-modal>
  </Layout>
</template>

<script>
  import Layout from '../layouts/main'
  import ErrorModal from '../../components/Errors';
  import SettingsModal from '../../components/SettingsModal';
  import {mapState} from 'vuex'
  export default{
    name: 'DashboardView',
    components: {
      Layout,
      ErrorModal,
      SettingsModal
    },
    computed: {
      ...mapState('asics', ['dashboardAsics', 'loading']),
    },
    data() {
      return {
        trigger: 100,   // how far from the bottom to trigger infinite scroll
      }
    },
    methods: {
      // check to see if we're at the bottom of the page

      openErrors(asic, fieldName, objectId){
        this.$store.dispatch('errors/fetchAsicErrors', {asicId: asic.id, fieldName, objectId})
        this.$refs.errorModal.$refs.modal.show()
      },
      openSettings(asic){
        this.$store.dispatch('asics/setModalAsic', asic)
        this.$store.dispatch('asicSettings/fetchSettings', asic.id)
        this.$refs.settingsModal.$refs.modal.show()
      }
    },
    created() {
      // get the data by performing API request
      this.$store.dispatch('asics/fetchDashboardAsics', this.dashboardAsics.pageInfo);
    }
  }
</script>

