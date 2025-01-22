<template>
  <b-collapse id="group_edit_form">
    <div class="form-group"><label class="control-label" for="id_farm">Ферма</label>
      <select name="farm" class="form-control" title="" id="id_farm" v-model="farm">
        <option v-for="farm in farms" v-bind:value="farm.value">{{farm.text}}</option>
      </select>
    </div>
    <div class="form-group">
      <label class="control-label" for="id_client">Клиент</label>
      <select name="client" class="form-control" title="" id="id_client" v-model="client">
        <option v-for="client in clients" v-bind:value="client.value">{{client.text}}</option>
      </select>
    </div>
    <div v-if="selectedAsics.length">
      <span>Выбранные ASIC({{selectedAsics.length}}):</span>
      <ul>
        <li v-for="asic in selectedAsics">
          <b-badge variant="dark">{{asic.asicName}}</b-badge>
          <b-badge variant="info" :href="'http://'+asic.ipAddress" target="_blank">
            {{asic.ipAddress}}
          </b-badge>
        </li>
      </ul>
      <div class="row">
        <span>Текущий клиент: <b-badge variant="primary">{{clientName}}</b-badge></span>
        <span>Текущая ферма: <b-badge variant="primary">{{farmName}}</b-badge></span>
      </div>
    </div>
    <b-btn variant="primary" class="not-align" @click="groupSetClient()">Назначить клиента</b-btn>
    <b-btn variant="primary" class="not-align" @click="groupSetFarm()">Назначить ферму</b-btn>
    <b-btn variant="primary" class="not-align" @click="enableAutoupdate()">Включить автообновление</b-btn>
    <b-btn variant="primary" class="not-align" @click="disableAutoupdate()">Выключить автообновление</b-btn>
    <b-btn v-b-toggle.group_edit_form variant="primary">
        Скрыть форму групповых операций
    </b-btn>
  </b-collapse>
</template>

<script>
  import {mapState, mapGetters, mapActions} from 'vuex';
  export default{
    name: 'GroupEditForm',
    computed: {
      ...mapState('utils', [
        'farms',
        'clients',
      ]),
      ...mapState('asics', [
        'groupEditForm',
        'selectedAsics'
      ]),
      ...mapGetters('asics', [
          'clientName',
          'farmName'
      ]),
      client:{
        get(){
          return this.groupEditForm.client
        },
        set(value){
          this.$store.commit('asics/setGroupEditFormField', {value, fieldName:'client'})
        }
      },
      farm:{
        get(){
          return this.groupEditForm.farm
        },
        set(value){
          this.$store.commit('asics/setGroupEditFormField', {value, fieldName:'farm'})
        }
      }
    },
    methods:{
      groupSetClient(){
        this.$store.dispatch('asics/groupSetClient')
        this.$eventBus.$emit('clearSelected')
      },
      groupSetFarm(){
        this.$store.dispatch('asics/groupSetFarm')
        this.$eventBus.$emit('clearSelected')
      },
      enableAutoupdate(){
        this.$store.dispatch('asics/enableAutoupdateAll')
        this.$eventBus.$emit('clearSelected')
      },
      disableAutoupdate(){
        this.$store.dispatch('asics/disableAutoupdateAll')
        this.$eventBus.$emit('clearSelected')
      }
    }

  }
</script>
