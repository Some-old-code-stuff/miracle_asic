<template>
  <div>
    <b-collapse id="search_form">

      <div class="form-group"><label class="control-label" for="id_type">Тип ASIC</label>
        <select name="type" class="form-control" title="" id="id_type" v-model="searchAsicType" @change="search">
          <option v-for="asicType in asicTypes" v-bind:value="asicType.value">{{asicType.text}}</option>
        </select>
      </div>
      <div class="form-group"><label class="control-label" for="id_alg_type">Алгоритм</label>
        <select name="alg_type" class="form-control" title="" id="id_alg_type" v-model="searchAlgType" @change="search">
          <option v-for="algType in algTypes" v-bind:value="algType.value">{{algType.text}}</option>
        </select>
      </div>
      <div class="form-group">
        <label class="control-label" for="id_asic_name">Имя майнера</label>
        <input type="text" name="asic_name" maxlength="100" class="form-control" placeholder="Имя майнера" title=""
               id="id_asic_name" v-model="searchAsicName" @keyup.enter="search">
      </div>
      <div class="form-group">
        <label class="control-label" for="id_pool_status">Статус пула</label>
        <input type="text" name="pool_status" maxlength="100" class="form-control" placeholder="Статус пула" title=""
               id="id_pool_status" v-model="searchPoolStatus" @keyup.enter="search">
      </div>

      <div class="form-group">
        <label class="control-label" for="id_client-name">Имя клиента</label>
        <input type="text" name="client-name" maxlength="100" class="form-control" placeholder="Имя клиента" title=""
               id="id_client-name" v-model="searchClientName" @keyup.enter="search">
      </div>

      <div class="form-group">
        <label class="control-label" for="id_farm-name">Имя фермы</label>
        <input type="text" name="farm-name" maxlength="100" class="form-control" placeholder="Имя фермы" title=""
               id="id_farm-name" v-model="searchFarmName" @keyup.enter="search">
      </div>

      <div class="form-group">
        <label class="control-label" for="id_error_rule-error_level">Уровень ошибки</label>
        <select name="error_rule-error_level" class="form-control" title="" id="id_error_rule-error_level"
                v-model="searchErrorLevel" @change="search">
          <option v-for="errorLevel in errorLevels" v-bind:value="errorLevel.value">{{errorLevel.text}}</option>
        </select>
      </div>
      <div class="form-group">
        <label class="control-label" for="id_error_rule-field_name">Проверяемое значение</label>
        <select name="error_rule-field_name" class="form-control" title="" id="id_error_rule-field_name"
                v-model="searchFieldName" @change="search">
          <option v-for="fieldName in fieldNames" v-bind:value="fieldName.value">{{fieldName.text}}</option>
        </select>
      </div>

      <div class="form-group">
        <b-btn v-b-toggle.search_form variant="primary">
          Скрыть форму поиска
        </b-btn>
      </div>

    </b-collapse>

    <div class="form-group">
        <label class="control-label" for="id_ip_address">IP адрес ASIC</label>
        <input type="text" name="ip_address" maxlength="15" class="form-control" placeholder="IP адрес ASIC" title=""
               id="id_ip_address" v-model="searchIpAddress" @keyup.enter="search">
      </div>
    <div class="form-group"><label class="control-label" for="id_farm">Ферма</label>
      <select name="farm" class="form-control" title="" id="id_farm" v-model="farm" @change="search">
        <option v-for="farm in farms" v-bind:value="farm.value">{{farm.text}}</option>
      </select>
    </div>
    <div class="form-group">
      <label class="control-label" for="id_client">Клиент</label>
      <select name="client" class="form-control" title="" id="id_client" v-model="client" @change="search">
        <option v-for="client in clients" v-bind:value="client.value">{{client.text}}</option>
      </select>
    </div>

    <b-form-checkbox v-model="withDisabledAutoupdate" @input="search">
      С выключенным автообновлением
    </b-form-checkbox>
    <b-form-checkbox v-model="withConnectionErrors" @input="search">
      С ошибками подключения
    </b-form-checkbox>
    <b-form-checkbox v-model="withErrors" @input="search">
      С ошибками
    </b-form-checkbox>
    <b-form-checkbox v-model="withWarnings" @input="search">
      С уведомлениями
    </b-form-checkbox>
    <b-form-checkbox v-model="unregisteredAsics" @input="search">
      Неназначенные асики
    </b-form-checkbox>

    <button class="btn btn-primary not-align" v-on:click="clearSearch" type="button">Сбросить поиск</button>
  </div>
</template>

<script>

  import {mapState} from 'vuex';

  export default {
    name: 'AsicSearchForm',
    computed: {
      ...mapState('utils',[
        'errorLevels',
        'asicTypes',
        'algTypes',
        'farms',
        'clients',
        'fieldNames',
      ]),
      ...mapState('asics', [
        'searchForm'
      ]),
      searchAsicType:{
        get(){
          return this.searchForm.asicType
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'asicType'})
        }
      },
      searchAlgType:{
        get(){
          return this.searchForm.algType
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'algType'})
        }
      },
      searchAsicName:{
        get(){
          return this.searchForm.asicName
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'asicName'})
        }
      },
      searchIpAddress:{
        get(){
          return this.searchForm.ipAddress
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'ipAddress'})
        }
      },
      searchPoolStatus:{
        get(){
          return this.searchForm.poolStatus
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'poolStatus'})
        }
      },
      searchClientName:{
        get(){
          return this.searchForm.clientName
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'clientName'})
        }
      },
      searchFarmName:{
        get(){
          return this.searchForm.farmName
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'farmName'})
        }
      },
      searchErrorLevel:{
        get(){
          return this.searchForm.errorLevel
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'errorLevel'})
        }
      },
      searchFieldName:{
        get(){
          return this.searchForm.fieldName
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'fieldName'})
        }
      },
      farm:{
        get(){
          return this.searchForm.farm
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'farm'})
        }
      },
      client:{
        get(){
          return this.searchForm.client
        },
        set(value){
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'client'})
        }
      },
      withDisabledAutoupdate:{
        get(){
          return this.searchForm.withDisabledAutoupdate
        },
        set(value){
          console.log(value)
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'withDisabledAutoupdate'})
        }
      },
      withConnectionErrors:{
        get(){
          return this.searchForm.withConnectionErrors
        },
        set(value){

            console.log(value)
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'withConnectionErrors'})
        }
      },
      withErrors:{
        get(){
          return this.searchForm.withErrors
        },
        set(value){
            console.log(value)
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'withErrors'})
        }
      },
      withWarnings:{
        get(){
          return this.searchForm.withWarnings
        },
        set(value){
            console.log(value)
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'withWarnings'})
        }
      },
      unregisteredAsics:{
        get(){
          return this.searchForm.unregisteredAsics
        },
        set(value){
            console.log(value)
          this.$store.commit('asics/setSearchFormField', {value, fieldName:'unregisteredAsics'})
        }
      },
    },
    created: function () {
      this.search();
    },
    methods: {
      search: function (e) {
        this.$store.dispatch('asics/searchAsics');
      },
      clearSearch: function (e) {
        this.$store.dispatch('asics/initSearchForm');
        this.search(e)
      }
    }
  }
</script>
