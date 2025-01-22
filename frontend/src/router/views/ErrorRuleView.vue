<template>
  <Layout>
    <b-btn variant="primary" v-b-modal.errorRuleModal @click="initErrorRule()">Добавить правило</b-btn>
    <b-table bordered striped responsive :items="errorRules" :fields="fields">
      <template slot="asicType" slot-scope="data">
        <b-btn variant="primary" size="sm" class="font-weight-bold m-1">{{data.item.asicType}}</b-btn>
      </template>
      <template slot="errorLevel" slot-scope="data">
        <b-btn variant="warning" v-if="data.item.errorLevelValue==1" size="sm" class="font-weight-bold m-1 p-1">
          {{data.item.errorLevel}}
        </b-btn>
        <b-btn variant="danger" v-if="data.item.errorLevelValue==2" size="sm" class="font-weight-bold m-1 p-1">
          {{data.item.errorLevel}}
        </b-btn>
      </template>
      <template slot="fieldName" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1">{{data.item.fieldName}}</b-btn>
      </template>
      <template slot="valueType" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1">{{data.item.valueType}}</b-btn>
      </template>
      <template slot="comparisonType" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1">{{data.item.comparisonType}}</b-btn>
      </template>
      <template slot="errorRule" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1" v-if="data.item.errorRule">
          {{data.item.errorRule.shortString}}
        </b-btn>
      </template>
      <template slot="value" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1">{{data.item.value}}</b-btn>
      </template>
      <template slot="percent" slot-scope="data">
        <b-btn size="sm" variant="primary" class="font-weight-bold m-1 p-1" v-if="data.item.percent">
          {{data.item.percent}}
        </b-btn>
      </template>
      <template slot="actions" slot-scope="data">
        <b-btn-group>
          <b-btn variant="secondary" size="sm" class="font-weight-bold m-1" v-b-modal.errorRuleModal
                 @click.stop="initErrorRule(data.item)">
                <span class="fa fa-pencil"></span>
          </b-btn>
          <b-btn size="sm" variant="danger" title="Удалить правило"
                 v-b-modal.deleteErrorRuleModal
                 @click.stop="deletingRule = data.item" class="m-1"><span
            class="fa fa-remove"></span></b-btn>
        </b-btn-group>
      </template>
    </b-table>

    <b-modal id="errorRuleModal" title="Редактирование валидационного правила" @ok="addOrUpdateErrorRule()">
      <b-form-group label="Тип ASIC" label-for="asicType">
        <b-select v-model="asicType" :options="asicTypes"></b-select>
      </b-form-group>
      <b-form-group label="Уровень ошибки" label-for="errorLevel">
        <b-select v-model="errorLevel" :options="errorLevels"></b-select>
      </b-form-group>
      <b-form-group label="Наименование поля" label-for="fieldName">
        <b-select v-model="fieldName" :options="fieldNames"></b-select>
      </b-form-group>
      <b-form-group label="Доп.правило" label-for="errorLevel">
        <b-select v-model="errorRule" :options="errorRulesShort"></b-select>
      </b-form-group>
      <b-form-group label="Тип значения" label-for="valueType">
        <b-select v-model="valueType" :options="valueTypes"></b-select>
      </b-form-group>
      <b-form-group label="Тип сравнения" label-for="comparisonType">
        <b-select v-model="comparisonType" :options="comparisonTypes"></b-select>
      </b-form-group>
      <b-form-group label="Значение" label-for="value">
        <b-input v-model="value"></b-input>
      </b-form-group>
      <b-form-group label="Процент" label-for="percent">
        <b-input type="number" v-model="percent"></b-input>
      </b-form-group>
      <b-form-group label="Сообщение" label-for="message">
        <b-input v-model="message"></b-input>
      </b-form-group>
    </b-modal>

    <b-modal id="deleteErrorRuleModal" title="Удаление валидационного правила" @ok="deleteErrorRule(deletingRule)"
             ok-title="Да" cancel-title="Нет"
    >
      <h4>Вы уверены, что хотите удалить это правило?</h4>
      <span>{{deletingRule.shortString}}</span>
      <div v-if="deletingRule.errorRule">
        Для правила <span>{{deletingRule.errorRule.shortString}}</span>
      </div>

    </b-modal>
  </Layout>
</template>

<script>
  import Layout from '../layouts/main'
  import {mapState, mapActions} from 'vuex'
  import {mapFields} from 'vuex-map-fields'

  export default{
    name: 'ErrorRuleView',
    components: {
      Layout
    },
    computed: {
      ...mapState('errorRules', [
        'errorRules',
        'asicTypes',
        'fieldNames',
        'valueTypes',
        'comparisonTypes',
        'errorLevels',
        'errorRulesShort',
      ]),
      ...mapFields('errorRules', [
        'errorRule.asicType',
        'errorRule.errorLevel',
        'errorRule.fieldName',
        'errorRule.errorRule',
        'errorRule.valueType',
        'errorRule.comparisonType',
        'errorRule.value',
        'errorRule.percent',
        'errorRule.message'
      ]),
      ...mapState('utils', [])
    },
    data(){
      return {
        fields: {
          asicType: {
            sortable: true,
            label: 'Тип ASIC'
          },
          errorLevel: {
            sortable: true,
            label: 'Уровень ошибки'
          },
          fieldName: {
            sortable: true,
            label: 'Наименование поля'
          },
          valueType: {
            sortable: true,
            label: 'Тип значения'
          },
          comparisonType: {
            sortable: true,
            label: 'Тип сравнения'
          },
          errorRule: {
            label: 'Доп. правило',
            sortable: false
          },
          value: {
            sortable: true,
            label: 'Значение'
          },
          percent: {
            sortable: true,
            label: 'Процент'
          },
          message: {
            sortable: true,
            label: 'Сообщение об ошибке'
          },
          actions: {
            label: 'Действия',
            sortable: false
          }
        },
        deletingRule: {}
      }
    },
    created(){
      this.$store.dispatch('errorRules/fetchErrorRules')
    },
    methods: {
      initErrorRule(errorRule){
        const id = errorRule ? errorRule.id : null
        this.$store.dispatch('errorRules/fetchErrorRule', id)
      },
      ...mapActions('errorRules', [
        'addOrUpdateErrorRule',
        'deleteErrorRule'
      ])
    }
  }
</script>
