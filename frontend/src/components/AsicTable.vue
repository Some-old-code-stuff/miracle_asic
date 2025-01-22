<template>
  <div class="col-md-12">
    <!--:thead-class="columnWidths"-->
    <!--:tbody-class="columnWidths"-->
    <h5>Найдено: <span class="badge badge-info">{{ asics.length }}</span></h5>
    <b-pagination :total-rows="asics.length" :per-page="100" v-model="currentPage"/>
    <b-table striped bordered stacked="md" responsive="true" :items="asics" :fields="fields" ref="asicTable"
             :current-page="currentPage"
             :per-page="100"
             class="asic-table"
    >
      <template slot="HEAD_id" slot-scope="data" class="col-1">
        <input type="checkbox" name="check_all" @click.stop="toggleAllAsics" ref="selectAll"/>
      </template>
      <template slot="id" slot-scope="data">
        <input type="checkbox" :name="data.item.id" class="asic_id" @change.stop="toggleSelectAsic"
               :ref="'asic_'+data.item.id"/>
      </template>
      <template slot="asicName" slot-scope="data">
        <button type="button" class="btn btn-primary btn-sm" @click.stop="showAsic(data.item)">
          <span>{{data.item.asicName}}</span>
          <span class="fa fa-signal" :class="have_connect_error(data.item)"
                :title="have_connect_error_title(data.item)">
            </span>
          <span class="fa fa-exclamation red-icon" title="Автообновление выключено!"
                v-if="data.item.stopUpdate">
            </span>
          <span class="fa fa-asterisk red-icon" :title="'Ошибок: '+data.item.openErrors.length"
                v-if="data.item.openErrors && data.item.openErrors.length>0">
            </span>
          <span class="fa fa-asterisk yellow-icon"
                :title="'Уведомлений: '+data.item.openWarnings.length"
                v-if="data.item.openWarnings && data.item.openWarnings.length>0">
            </span>
        </button>
      </template>
      <template slot="ipAddress" slot-scope="data">
        <a :href="'http://'+data.item.ipAddress" target="_blank">{{ data.item.ipAddress}}</a>
      </template>
      <template slot="poolStatus" slot-scope="data">
        <span v-if="haveErrors('btn-', data.item, FieldName.POOL_STATUS) != 'btn-success'"
              class="btn btn-sm font-weight-bold m-1 p-1"
              @click.stop="openErrors(data.item, FieldName.POOL_STATUS)"
              :class="haveErrors('btn-', data.item, FieldName.POOL_STATUS)">{{ data.item.poolStatus}}</span>

        <span v-else class="btn btn-success btn-sm font-weight-bold m-1 p-1">{{ data.item.poolStatus}}</span>
      </template>
      <template slot="clientName" slot-scope="data">
        <span class="badge badge-primary">{{ data.item.clientName}}</span>
      </template>
      <template slot="fullRate" slot-scope="data">
        <span v-if="haveErrorsWithWarnings('btn-', data.item, FieldName.FULL_RATE) != 'btn-success'"
              class="btn btn-sm font-weight-bold m-1 p-1"
              :class="haveErrorsWithWarnings('btn-', data.item, FieldName.FULL_RATE)"
              @click.stop="openErrors(data.item, FieldName.FULL_RATE)">{{data.item.fullRate}}</span>

        <span v-else class="btn btn-success btn-sm font-weight-bold m-1 p-1">{{ data.item.fullRate}}</span>

      </template>
      <template slot="chains" slot-scope="data">
        <div class="container">
          <div class="row">
            <div class="col-md-12">
              <div class="row">
                <div class="col-md-3 col-center" v-for="chain in data.item.chains">
                  <div class="row">
                    <span
                  v-if="haveErrors('btn-', data.item, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id) != 'btn-success'"
                  class="btn btn-sm font-weight-bold m-1 p-1 col"
                  :class="haveErrors('btn-', data.item, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)"
                  @click.stop="openErrors(data.item, FieldName.CHAIN_INFO_WRONG_CHIPS, chain.id)">{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
            <span v-else
                  class="btn btn-success btn-sm font-weight-bold m-1 p-1 col">{{ chain.wrongChips }}/{{ chain.workingChips }}</span>
                  </div>
            </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <div class="row">
                <div class="col-md-3 col-center" v-for="chain in data.item.chains">
                  <div class="row">
                    <span class="btn btn-sm font-weight-bold m-1 p-1 col"
                    :class="haveErrors('btn-', data.item, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                    v-if="haveErrors('btn-', data.item, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)!='btn-success'"
                    @click.stop="openErrors(data.item, FieldName.CHAIN_INFO_TEMPERATURE, chain.id)"
                    >{{ chain.temperature}}&#186;</span>
                  <span v-else class="btn btn-success btn-sm font-weight-bold m-1 p-1 col">
                  {{ chain.temperature}}&#186;</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template slot="fans" slot-scope="data">
        <span v-if="haveErrors('btn-', data.item, FieldName.FAN_INFO_SPEED, fanInfo.id)!='btn-success'"
              v-for="fanInfo in data.item.fans" class="btn btn-sm font-weight-bold m-1 p-1"
              :class="haveErrors('btn-', data.item, FieldName.FAN_INFO_SPEED, fanInfo.id)"
              @click.stop="openErrors(data.item, FieldName.FAN_INFO_SPEED, fanInfo.id)"
        >{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
        <span v-else
              class="btn btn-success btn-sm font-weight-bold m-1 p-1">{{ fanInfo.name }}: {{ fanInfo.speed }}</span>
      </template>
      <template slot="poolUsername" slot-scope="data">
        <span v-b-tooltip.hover :title="data.item.poolUsername">{{data.item.poolUsername | truncate(8) }}</span>
      </template>
      <template slot="poolAddress" slot-scope="data">
        <span v-b-tooltip.hover :title="data.item.poolAddress">{{data.item.poolAddress | truncate(8) }}</span>
      </template>
      <template slot="updated" slot-scope="data">
        <b-btn size="sm" variant="danger" class="font-weight-bold m-1 p-1" v-if="notUpdatedLongTime(data.item.updated)">
          {{data.item.updated}}
        </b-btn>
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1" v-else>{{data.item.updated}}</b-btn>
      </template>
      <template slot="actions" slot-scope="data">
        <a @click.stop="closeErrors(data.item)" class="btn btn-light btn-sm" title="Проблемы решены">
          <span class="fa fa-check"></span>
        </a>
        <a @click.stop="update(data.item)" class="btn btn-light btn-sm" title="Обновить">
          <span class="fa fa-repeat"></span>
        </a>
        <a @click.stop="reboot(data.item)" class="btn btn-light btn-sm" title="Перезагрузка">
          <span class="fa fa-refresh"></span>
        </a>
        <a class="btn btn-danger btn-sm" title="Возобновить обновление" @click.stop="resumeUpdate(data.item)"
           v-if="data.item.stopUpdate">
          <span class="fa fa-play"></span>
        </a>
        <a class="btn btn-light btn-sm" title="Остановить обновление" @click.stop="stopUpdate(data.item)" v-else>
          <span class="fa fa-pause"></span>
        </a>
      </template>
      <template slot="row-details" slot-scope="row">
        <!--<span :value="row.item._rowVariant"></span>-->
        {{row.item._rowVariant}} {{row.item.stopUpdate}} {{row.item.errors}}
      </template>

    </b-table>
    <b-pagination :total-rows="asics.length" :per-page="100" v-model="currentPage"/>
    <asic-modal ref="asicModal"></asic-modal>
    <error-modal ref="errorModal"></error-modal>

  </div>
</template>

<script>

  import {mapState, mapActions} from 'vuex';
  import AsicModal from './AsicModal'
  import ErrorModal from './Errors'

  export default{
    name: 'AsicTable',

    computed: {
      ...mapState('asics', [
        'asics',
        'modalAsic',
        'selectedAsics'
      ]),
    },
    components: {
      'asic-modal': AsicModal,
      ErrorModal
    },
    data(){
      return {
        fields: {
          id: {
            sortable: false,
          },
          asicName: {
            sortable: true,
            label: 'Название',
          },
          ipAddress: {
            sortable: true,
            label: 'IP',
          },
          clientName: {
            sortable: true,
            label: 'Клиент',
          },
          fullRate: {
            sortable: true,
            label: 'Мощность',
          },
          defaultRate: {
            sortable: true,
            label: 'Средняя',
          },
          chains: {
            sortable: false,
            label: 'Платы',
          },
          fans: {
            sortable: false,
            label: 'Вентиляторы',
          },
          farmName: {
            sortable: true,
            label: 'Ферма',
          },
          updated: {
            sortable: true,
            label: 'Обновлено',
          },
          actions: {
            sortable: false,
            label: 'Действия',
          }
        },
        currentPage: 1,
      }

    },
    methods: {
      ...mapActions('asics', [
        'selectAsic', 'deselectAsic'
      ]),
      get_errors_data: function (asic) {
        this.$store.dispatch('errors/getErrorsData', asic)
      },
      showAsic: function (asic) {
        this.$store.dispatch('asics/setModalAsic', asic)
        this.$refs.asicModal.$refs.modal.show()
      },
      toggleSelectAsic(event){
        const id = event.target.name
        if (event.target.checked) {
          this.selectAsic({id})
          if (this.selectedAsics.length == this.asics.length || this.selectedAsics.length == 100) {
            this.$refs.selectAll.checked = true
          }
        } else {
          this.deselectAsic({id})
          if (this.selectedAsics.length == 0) {
            this.$refs.selectAll.checked = false
          }
        }
      },
      toggleAllAsics(event){
        let selectedAsics = []
        for (const asic of this.$refs.asicTable.computedItems) {
          const ref = this.$refs['asic_' + asic.id];
          if (event.target.checked) {
            if (ref) {
              ref.checked = true
            }
          } else {
            if (ref) {
              ref.checked = false
            }
          }
        }
        if (event.target.checked) {
          selectedAsics = this.$refs.asicTable.computedItems.map(el => el)
        }

        this.$store.dispatch('asics/setSelectedAsics', selectedAsics)
      },
      created(){
        const self = this
        this.$eventBus.$on('clearSelected', function () {
          console.log('clear selected');
          for (const asic of self.asics) {
            const ref = self.$refs['asic_' + asic.id];
            ref.checked = false
          }
        })
      },
      openErrors(asic, fieldName, objectId){
        this.$store.dispatch('errors/fetchAsicErrors', {asicId: asic.id, fieldName, objectId})
        this.$refs.errorModal.$refs.modal.show()
      },
      notUpdatedLongTime(stringDate){
        const now = new Date(Date.now())
        const monthYear = stringDate.split(' ')[0].split('.').reverse().join('.') + '.' + now.getFullYear()
        const time = stringDate.split(' ')[1]
        const date = new Date(monthYear + ' ' + time)
        const hours = Math.abs(now - date) / 3.6e6;
        return hours >= 3
      }
    }
  }
</script>

<style>
  .asic-table.table-bordered td, .asic-table.table-bordered th, .asic-table.table thead th {
    border: 1px solid #6c757d;
    /*vertical-align:middle;*/
    /*display:inline-flex !important;*/
  }
  .col-center{
    margin-left: auto;
    margin-right: auto;
  }
</style>
