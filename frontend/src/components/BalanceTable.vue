<template>
  <div class="">
    <b-input-group class="col-md-3">
      <b-input-group-prepend>
        <b-btn variant="primary" v-b-modal.balanceModal>Добавить запись</b-btn>
      </b-input-group-prepend>
      <b-select v-model="dateFilter" :options="dates"></b-select>
    </b-input-group>


    <div class="clearfix"></div>
    <b-table bordered striped responsive :items="balanceData" :fields="fields" class="balance-table"
             :filter="dateFilter">
      <template slot="date" slot-scope="data">
        <h1>{{dateFormat(data.item.date)}}</h1>

        <b-btn-group v-if="canEdit(data)">
          <b-button size="sm" v-b-modal.counterModal @click.stop="setBalanceId(data.item.id)" variant="primary">
            Добавить счетчик
          </b-button>
          <b-button size="sm" @click.stop="deleteCounterRecord(data.item.id)" variant="danger">
            Удалить запись
          </b-button>
        </b-btn-group>
        <b-btn-group v-if="canEditWithAuth(data)">
          <b-button size="sm" v-b-modal.smsTokenAuthModal @click.stop="setEditItem(data.item)" variant="primary">
            Получить доступ к редактированию
          </b-button>
        </b-btn-group>

      </template>
      <template slot="counters" slot-scope="data">
        <b-card v-for="(counter, index) in data.item.counters">
          <h5>
            <span>{{counter.name}}: {{counter.value}}</span>
            <b-btn-group v-if="canEdit(data)">
              <b-btn size="sm" variant="secondary" title="Редактировать счетчик"
                     v-b-modal.counterModal @click.stop="editCounter(data.item.id, counter)">
                <span class="fa fa-pencil"></span>
              </b-btn>
              <b-btn size="sm" variant="danger" title="Удалить счетчик"
                     @click.stop="deleteCounter({counterId:counter.id, recordId:data.item.id})"><span
                class="fa fa-remove"></span></b-btn>
            </b-btn-group>
          </h5>
          <div class="row">
            <div class="col"></div>
            <div class="col">Предварительный</div>
            <div class="col">Наценочный</div>
            <div class="col">Утвержденный</div>
          </div>
          <div class="row">
            <div class="col">
              Тарифы
            </div>
            <div class="col">
              <b-badge variant="danger" title="Предварительный">{{counter.preliminaryTariff}}</b-badge>
            </div>
            <div class="col">
              <b-badge variant="warning" title="Наценочный">{{counter.testTariff}}</b-badge>
            </div>
            <div class="col">
              <b-badge variant="primary" title="Утвержденный">{{counter.approvedTariff}}</b-badge>
            </div>
          </div>
          <div class="row">
            <div class="col">Сумма</div>
            <div class="col">
              <b-badge variant="danger" title="Предварительный">{{countSumm(counter, data.item, index, 'preliminary',
                data.item.date).toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="warning" title="Наценочный">{{countSumm(counter, data.item, index, 'test',
                data.item.date).toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="primary" title="Утвержденный">{{countSumm(counter, data.item, index, 'approved',
                data.item.date).toLocaleString('ru')}}
              </b-badge>
            </div>
          </div>
          <div class="row">
            <div class="col">Переплата/Прибыль</div>
            <div class="col">
              <b-badge variant="info" title="Переплата">{{countDifference(counter, data.item, index,
                data.item.date).toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="success" title="Прибыль">{{countDifference(counter, data.item, index,
                data.item.date, 'approved','test').toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col"></div>
          </div>
        </b-card>

        <b-card>
          <h5>Итого</h5>
          <div class="row">
            <div class="col">Предварительный</div>
            <div class="col">Наценочный</div>
            <div class="col">Утвержденный</div>
            <div class="col">Переплата</div>
            <div class="col">Прибыль</div>
          </div>
          <div class="row">
            <div class="col">
              <b-badge variant="danger" title="Предварительный">{{calculateTotal(data.item, data.index,
                'preliminary').toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="warning" title="Наценочный">{{calculateTotal(data.item, data.index,
                'test').toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="primary" title="Утвержденный">{{calculateTotal(data.item, data.index,
                'approved').toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="info" title="Переплата">{{calculateTotal(data.item, data.index,
                'difference').toLocaleString('ru')}}
              </b-badge>
            </div>
            <div class="col">
              <b-badge variant="success" title="Прибыль">{{calculateTotal(data.item, data.index,
                'profit').toLocaleString('ru')}}
              </b-badge>
            </div>
          </div>
        </b-card>
      </template>
    </b-table>
    <sms-token-auth-modal action="balance/canEdit" v-bind:params="editItem"></sms-token-auth-modal>
  </div>
</template>

<script>
  import {mapState, mapActions} from 'vuex'
  import Datepicker from 'vue2-datepicker'
  import SmsTokenAuthModal from './SmsTokenAuthModal'

  export default {
    name: 'BalanceTable',
    components: {
      SmsTokenAuthModal
    },
    data(){
      return {
        fields: {
          date: {
            sortable: true,
            label: 'Дата'
          },
          counters: {
            sortable: false,
            label: 'Данные'
          }
        },
        items: [
          {
            id: 1,
            date: 'Январь 2018',
            dateValue: new Date(2018, 1, 0),
            counters: [
              {
                name: 'Счетчик 1',
                preliminaryTariff: 4.2,
                testTariff: 1.2,
                approvedTariff: 4.1,
                value: 56,
                koeff: 80
              },
              {
                name: 'Счетчик 2',
                preliminaryTariff: 2.7,
                testTariff: 1.5,
                approvedTariff: 2.9,
                value: 80,
                koeff: 60
              },
              {
                name: 'Счетчик 3',
                preliminaryTariff: 3.8,
                testTariff: 1.2,
                approvedTariff: 4.0,
                value: 42,
                koeff: 55
              }
            ]
          },

          {
            id: 2,
            date: 'Февраль 2018',
            dateValue: new Date(2018, 2, 0),
            counters: [
              {
                name: 'Счетчик 1',
                preliminaryTariff: 4.2,
                testTariff: 1.2,
                approvedTariff: 4.1,
                value: 66,
                koeff: 80
              },
              {
                name: 'Счетчик 2',
                preliminaryTariff: 2.7,
                testTariff: 1.5,
                approvedTariff: 2.9,
                value: 100,
                koeff: 60
              },
              {
                name: 'Счетчик 3',
                preliminaryTariff: 3.8,
                testTariff: 1.2,
                approvedTariff: 4.0,
                value: 68,
                koeff: 55
              }
            ]
          }
        ],
        editItem: {},
        dateFilter: new Date(Date.now()).getFullYear().toString(),
//        dates: []
      }
    },
    computed: {
      ...mapState('balance', [
        'balanceData',
        'dates',
      ]),
    },
    created(){
      this.fetchBalance()
    },
    methods: {
      ...mapActions('balance', [
        'fetchBalance',
        'setBalanceId',
        'deleteCounterRecord',
        'deleteCounter',
      ]),
      dateFormat(date){
        return Datepicker.fecha.format(new Date(date), 'MMMM YYYY')
      },
      editCounter(recordId, counter){
        this.setBalanceId(recordId)
        this.$store.commit('balance/setModalCounter', counter)
      },
      countSumm(counter, record, index, tariffName, dateValue){
        let sorted = this.balanceData.map(el => el).sort().filter(elem => elem.date < record.date)

        // const prev_item = this.balanceData[id - 1]
        const prev_item = sorted.reverse()[0]
        let value = counter.value
        if (prev_item) {
          const prev_counter = prev_item.counters[index]
          if (prev_counter) {
            value -= prev_counter.value
          }
        }
        const d = new Date(dateValue)
        const day_in_month = new Date(d.getYear(), d.getMonth(), 0).getDate()
        return (value * counter.koefficient * counter[tariffName + 'Tariff'])
      },
      countDifference(counter, record, index, dateValue, first = 'preliminary', second = 'approved'){
        const preliminary = this.countSumm(counter, record, index, first, dateValue)
        const approved = this.countSumm(counter, record, index, second, dateValue)
        return parseFloat(approved) - parseFloat(preliminary)
      },
      calculateTotal(record, index, fieldName){
        const self = this;
        let result = 0;

        record.counters.forEach(function (counter, counterIndex) {
          if (fieldName == 'difference') {
            result += self.countDifference(counter, record, counterIndex, record.date)
          }
          else if (fieldName == 'profit') {
            result += self.countDifference(counter, record, counterIndex, record.date, 'approved', 'test')
          }
          else {
            result += self.countSumm(counter, record, counterIndex, fieldName, record.date)
          }
        })
        return result
      },
      canEdit(record){
        if (record.item.id == this.balanceData[this.balanceData.length - 1].id) {
          return true
        }
        return record.item.canEdit
      },
      setEditItem(record){
        this.editItem = record
        console.log(this.editItem)
      },
      canEditWithAuth(record){
        // Не редактировалась и последние два с конца
        if (record.item.canEdit) {
          return false
        }
        if (record.index == this.balanceData.length - 1) {
          return false
        }
        const d = new Date(record.item.date)
        const last = new Date(this.balanceData[this.balanceData.length - 1].date)
        const numberOfMonths = (last.getFullYear() - d.getFullYear()) * 12 + (last.getMonth() - d.getMonth())

        return numberOfMonths > 0 && numberOfMonths <= 2
      }
    }
  }
</script>

<style>
  .card-body {
    padding: 0.5rem;
  }

  .row {
    margin: 0;
  }

  .balance-table .table-bordered td, .balance-table .table-bordered th, .balance-table .table thead th {
    border: 2px solid #6c757d;
  }
</style>
