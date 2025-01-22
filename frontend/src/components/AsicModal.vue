<template>
  <div>
    <b-modal id="asic_modal" @hide="resetModal" :title="modalAsic.asicName" ok-only ref="modal">
      <div class="row">
        <div class="col-md-6">
          <h4>
            <select name="type" class="form-control" title="" id="id_type" v-model="newAsicType" v-if="isEditAsicType"
                    @change="saveAsicType()">
              <option v-for="asicType in asicTypes" v-bind:value="asicType.value">{{asicType.text}}</option>
            </select>
            <span v-else="isEditAsicType" @click="editAsicType()">{{modalAsic.asicName}}</span>
            <span class="fa fa-signal" :class="have_connect_error(modalAsic)"
                  :title="have_connect_error_title(modalAsic)">
            </span>
            <span class="fa fa-exclamation red-icon" title="Автообновление выключено!"
                  v-if="modalAsic.stopUpdate">
            </span>
            <span class="fa fa-asterisk red-icon" :title="'Ошибок: '+modalAsic.openErrors.length"
                  v-if="modalAsic.openErrors && modalAsic.openErrors.length>0">
            </span>
            <span class="fa fa-asterisk yellow-icon"
                  :title="'Уведомлений: '+modalAsic.openWarnings.length"
                  v-if="modalAsic.openWarnings && modalAsic.openWarnings.length>0">
            </span>
          </h4>
          <h4>
            <select name="alg_type" class="form-control" title="" id="id_alg_type" v-model="newAlgType"
                    v-if="isEditAlgType"
                    @change="saveAlgType()">
              <option v-for="algType in algTypes" v-bind:value="algType.value">{{algType.text}}</option>
            </select>
            <span v-else @click="editAlgType()">{{ modalAsic.algType }}</span>
          </h4>
          <h4><span class="grey-color">{{ modalAsic.defaultRate }}</span></h4>
          <h4>{{ modalAsic.hostName }}</h4>
          <h4>
            <a :href="'http://'+modalAsic.ipAddress" target="_blank">{{ modalAsic.ipAddress}}</a></h4>
          <h4>
            <span v-if="haveErrorsWithWarnings('btn-', modalAsic, FieldName.FULL_RATE) != 'btn-success'"
                  class="btn font-weight-bold btn-lg m-1 p-1"
                  :class="haveErrorsWithWarnings('btn-', modalAsic, FieldName.FULL_RATE)"
                  @click.stop="openErrors(modalAsic, FieldName.FULL_RATE)">
              {{modalAsic.fullRate}}</span>
            <span v-else class="btn btn-success btn-lg m-1 p-1">{{modalAsic.fullRate}}</span>
          </h4>
          <h5>Статус пула
            <span v-if="haveErrors('btn-', modalAsic, FieldName.POOL_STATUS) != 'btn-success'"
                  class="btn font-weight-bold m-1 p-1" :class="haveErrors('badge-', modalAsic, FieldName.POOL_STATUS)"
                  @click.stop="openErrors(modalAsic, FieldName.POOL_STATUS)"
            >{{ modalAsic.poolStatus}}</span>
            <span v-else class="btn btn-success font-weight-bold m-1 p-1">{{ modalAsic.poolStatus}}</span>
          </h5>
          <h5 v-b-tooltip.hover :title="modalAsic.poolAddress">Адрес
            пула: {{modalAsic.poolAddress | truncate(8) }}</h5>
          <h5 v-b-tooltip.hover :title="modalAsic.poolUsername">Пользователь на
            пуле: {{modalAsic.poolUsername | truncate(8) }}</h5>
          <div class="row">
            <div class="col">
              <a @click.stop="closeErrors(modalAsic)" class="btn btn-light btn-issa" title="Проблемы решены">
                <span class="fa fa-check"></span>
              </a>
              <a @click.stop="update(modalAsic)" class="btn btn-light btn-issa" title="Обновить">
                <span class="fa fa-repeat"></span>
              </a>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <a @click.stop="reboot(modalAsic)" class="btn btn-light btn-issa" title="Перезагрузка">
                <span class="fa fa-refresh"></span>
              </a>
              <a class="btn btn-light btn-issa" title="Настройки" @click.stop="openSettings(modalAsic)">
                <span class="fa fa-cog"></span>
              </a>
              <a class="btn btn-light btn-issa" title="Возобновить обновление" @click.stop="resumeUpdate(modalAsic)"
                 v-if="modalAsic.stopUpdate">
                <span class="fa fa-play"></span>
              </a>
              <a class="btn btn-light btn-issa" title="Остановить обновление" @click.stop="stopUpdate(modalAsic)"
                 v-else>
                <span class="fa fa-pause"></span>
              </a>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="">
            <div class="row">
              <span class="col badge grey-color no-background">&#8451;</span>
              <span class="col badge grey-color no-background">Частота</span>
              <span class="col badge grey-color no-background">Мощн.</span>
              <span class="col badge grey-color no-background">Чипы</span>
            </div>
            <div v-for="chain in modalAsic.chains" class="">
              <div class="row">

                <span class="col btn font-weight-bold btn-sm m-1 p-1"
                      :class="haveErrors('btn-', modalAsic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                      v-if="haveErrors('btn-', modalAsic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)!='btn-success'"
                      @click.stop="openErrors(modalAsic, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                >{{ chain.temperature}}</span>
                <span v-else class="col m-1 p-1 btn btn-sm btn-success font-weight-bold">
                  {{ chain.temperature}}</span>
                <span class="col m-1 p-1 btn btn-sm btn-primary font-weight-bold">{{ chain.frequency }}</span>
                <span class="col m-1 p-1 btn btn-sm btn-primary font-weight-bold">{{ chain.rate }}</span>
                <span class="col m-1 p-1 btn btn-sm font-weight-bold"
                      :class="haveErrors('btn-', modalAsic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)"
                      v-if="haveErrors('btn-', modalAsic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)!='btn-success'"
                      @click.stop="openErrors(modalAsic, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)"
                >{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
                <span v-else class="col m-1 p-1 btn btn-sm btn-success font-weight-bold">{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
              </div>
              <div class="clearfix"></div>
              <b-progress class="row" :max="chain.allChips">
                <b-progress-bar variant="success" :value="chain.workingChips"></b-progress-bar>
                <b-progress-bar variant="danger" :value="chain.wrongChips"></b-progress-bar>
              </b-progress>
            </div>
            <div class="row">
              <span v-if="haveErrors('btn-', modalAsic, FieldName.FAN_INFO_SPEED, fanInfo.id)!='btn-success'"
                    v-for="fanInfo in modalAsic.fans" class="btn btn-sm font-weight-bold m-1 p-1"
                    :class="haveErrors('btn-', modalAsic, FieldName.FAN_INFO_SPEED, fanInfo.id)"
                    @click.stop="openErrors(modalAsic, FieldName.FAN_INFO_SPEED, fanInfo.id)"
              >{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
              <span v-else
                    class="m-1 p-1 btn font-weight-bold btn-success">{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
            </div>
          </div>
        </div>
      </div>
    </b-modal>
    <error-modal ref="errorModal"></error-modal>
    <settings-modal ref="settingsModal"></settings-modal>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import Errors from './Errors';
  import SettingsModal from './SettingsModal';
  export default{
    name: 'AsicModal',
    computed: {
      ...mapState('utils', [
        'asicTypes',
        'algTypes',
      ]),
      ...mapState('asics', [
        'modalAsic'
      ]),
    },
    components: {
      'error-modal': Errors,
      SettingsModal
    },
    data: function () {
      return {
        isEditAsicType: false,
        newAsicType: '',
        newAlgType: '',
        isEditAlgType: false,
      }
    },
    methods: {
      resetModal () {
//        this.$store.dispatch('asics/setModalAsic', {})
      },
      openErrors(asic, fieldName, objectId){
        this.$store.dispatch('errors/fetchAsicErrors', {asicId: asic.id, fieldName, objectId})
        this.$refs.errorModal.$refs.modal.show()
      },
      openSettings(asic){
        this.$refs.settingsModal.$refs.modal.show()
      },
      editAsicType(){
        const self = this
        console.log(self.modalAsic)
        self.newAsicType = self.asicTypes.find(function (elem) {
          return elem.text == self.modalAsic.type
        }).value;

        self.isEditAsicType = true
      },
      saveAsicType(){
        this.$store.dispatch('asics/setAsicType', {asic: this.modalAsic, type: this.newAsicType})

        this.isEditAsicType = false
      },
      editAlgType(){
        const self = this
        console.log(self.modalAsic)
        self.newAlgType = self.algTypes.find(function (elem) {
          return elem.text == self.modalAsic.algType
        }).value;

        self.isEditAlgType = true
      },
      saveAlgType(){
        this.$store.dispatch('asics/setAlgType', {asic: this.modalAsic, type: this.newAlgType})

        this.isEditAlgType = false
      }
    }
  }
</script>
