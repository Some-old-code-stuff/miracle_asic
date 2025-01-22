<template>
  <Layout>
    <div class="row">
      <div class="col-md-2">
        <b-btn v-b-toggle.search_form variant="primary">
          Показать форму поиска
        </b-btn>
        <div class="clearfix"></div>
        <asic-search-form/>
      </div>
      <div class="col-md-2">
        <div class="well well-sm">
          <b-btn v-b-toggle.group_edit_form variant="primary">
            Скрыть\показать групповые операции
          </b-btn>

          <div class="clearfix"></div>
          <group-edit-form></group-edit-form>
        </div>
      </div>
      <div class="col-md-2">
        <b-btn variant="primary" v-b-modal.addAsicModal @click="initAddAsic()">Добавить ASIC</b-btn>

        <b-modal id="addAsicModal" title="Добавление ASIC" @ok="addAsic()" v-if="true">
          <b-form-group label="IP адрес ASIC" label-for="ipAddress">
            <b-input v-model="ipAddress"></b-input>
          </b-form-group>
          <b-form-group label="Тип ASIC" label-for="type">
            <b-select v-model="type" :options="asicTypes"></b-select>
          </b-form-group>
          <b-form-group label="Алгоритм" label-for="algType">
            <b-select v-model="algType" :options="algTypes"></b-select>
          </b-form-group>
          <b-form-group label="Имя клиента" label-for="client">
            <b-select v-model="client" :options="clients"></b-select>
          </b-form-group>
          <b-form-group label="Имя фермы" label-for="farm">
            <b-select v-model="farm" :options="farms"></b-select>
          </b-form-group>
        </b-modal>
      </div>
    </div>
    <div class="row">
      <asic-table/>
    </div>
  </Layout>
</template>

<script>
  import AsicSearchForm from '../../components/AsicSearchForm'
  import GroupEditForm from '../../components/GroupEditForm'
  import AsicTable from '../../components/AsicTable'
  import Layout from '../layouts/main'

  import {mapState, mapActions} from 'vuex'
  import {mapFields} from 'vuex-map-fields'

  export default{
    name: 'HomeView',
    components: {
      AsicSearchForm,
      AsicTable,
      Layout,
      GroupEditForm
    },
    computed:{
         ...mapState('utils', [
        'asicTypes',
        'algTypes',
        'farms',
        'clients',
      ]),
      ...mapFields('asics', [
        'asic.type',
        'asic.ipAddress',
        'asic.client',
        'asic.farm',
        'asic.algType',
      ]),
    },
    methods:{
      ...mapActions('asics', [
        'addAsic',
        'initAddAsic'
      ])
    }
  }
</script>
