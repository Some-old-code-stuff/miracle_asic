<template>
  <Layout>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <balance-table></balance-table>

        <b-modal id="balanceModal" title="Добавление записи баланса" @ok="addCounterRecord(balanceDate)">
          <datepicker type="month" lang="ru" v-model="balanceDate" format="MMMM YYYY"></datepicker>
        </b-modal>

        <b-modal id="counterModal" title="Добавление счетчика" @ok="addOrUpdateCounter(modalCounter)"
                 @hide="resetModalCounter()">
          <div class="form-group">
            <label class="control-label" for="id_name">Имя счетчика</label>
            <b-input id="id_name" v-model="name"></b-input>
          </div>
          <div class="form-group">
            <label class="control-label" for="id_value">Значение</label>
            <b-input id="id_value" type="number" v-model="value"></b-input>
          </div>
          <div class="form-group">
            <label class="control-label" for="id_preliminary_tariff">Предварительный тариф</label>
            <b-input id="id_preliminary_tariff" type="number" v-model="preliminaryTariff"></b-input>
          </div>
          <div class="form-group">
            <label class="control-label" for="id_approved_tariff">Утвержденный тариф</label>
            <b-input id="id_approved_tariff" type="number" v-model="approvedTariff"></b-input>
          </div>
          <div class="form-group" v-if="modalCounter.id > 0">
            <label class="control-label" for="id_test_tariff">Тестовый тариф</label>
            <b-input id="id_test_tariff" type="number" v-model="testTariff"></b-input>
          </div>
          <div class="form-group">
            <label class="control-label" for="id_koeff">Коэффициент</label>
            <b-input id="id_koeff" type="number" v-model="koefficient"></b-input>
          </div>
        </b-modal>
      </div>
    </div>
  </Layout>
</template>

<script>

  import Layout from '../layouts/main'
  import BalanceTable from '../../components/BalanceTable'
  import Datepicker from 'vue2-datepicker';

  Datepicker.fecha.i18n.monthNamesShort = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
  Datepicker.fecha.i18n.monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


  import {mapState, mapActions} from 'vuex'
  export default{
    name: 'BalanceView',
    components: {
      Layout,
      BalanceTable,
      Datepicker
    },
    computed: {
      ...mapState('balance', [
        'balance',
        'modalCounter'
      ]),
      name: {
        get(){
          return this.modalCounter.name
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'name'})
        }
      },
      value: {
        get(){
          return this.modalCounter.value
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'value'})
        }
      },
      preliminaryTariff: {
        get(){
          return this.modalCounter.preliminaryTariff
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'preliminaryTariff'})
        }
      },
      approvedTariff: {
        get(){
          return this.modalCounter.approvedTariff
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'approvedTariff'})
        }
      },
      testTariff: {
        get(){
          return this.modalCounter.testTariff
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'testTariff'})
        }
      },
      koefficient: {
        get(){
          return this.modalCounter.koefficient
        },
        set(value){
          this.$store.commit('balance/setModalCounterField', {value, fieldName: 'koefficient'})
        }
      }
    },
    data(){
      return {
        balanceDate: null
      }
    },
    methods: {
      ...mapActions('balance', [
        'addCounterRecord',
        'addOrUpdateCounter',
      ]),
      resetModalCounter(){
        this.$store.commit('balance/resetModalCounter')
      }
    }
  }
</script>
