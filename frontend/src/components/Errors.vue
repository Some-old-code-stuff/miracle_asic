<template>
  <b-modal id="error_modal" @hide="resetModal" title="Ошибки поля" ok-only ref="modal" size="lg">
    <div style="overflow:auto" class="">

      <b-pagination :total-rows="modalErrors.length" :per-page="5" v-model="currentPage"/>
      <b-table striped bordered :items="modalErrors" :fields="fields" id="error_table"
               :current-page="currentPage"
               :per-page="5">

        <template slot="HEAD_id" slot-scope="data">
          <input type="checkbox" id="check_all"/>
        </template>
        <template slot="id" slot-scope="data">
          <input type="checkbox" :name="data.item.id"/>
        </template>
        <template slot="message" slot-scope="data">
          {{data.item.message }}
        </template>
        <template slot="actions" slot-scope="data">
          <!--<b-btn @click.stop="openHistory(data.item.id)" variant="light">История</b-btn>-->
          <b-btn v-if="data.item.statusValue!=2" variant="light" @click.stop="toPending(data.item)">В разработку</b-btn>
          <b-btn v-if="data.item.statusValue==2" variant="light" @click.stop="closeError(data.item)">Решена</b-btn>
          <b-btn v-if="data.item.levelValue==1" variant="light" @click.stop="toError(data.item)">Повысить уровень
          </b-btn>
          <b-btn v-if="data.item.levelValue==2" variant="light" @click.stop="toWarning(data.item)">Понизить уровень
          </b-btn>
        </template>

      </b-table>

    </div>
  </b-modal>
</template>


<script>
  import {mapState} from 'vuex'
  export default {
    name: 'errors',
    computed: {
      ...mapState('errors', [
        'modalErrors'
      ]),
    },
    data(){
      return {
        fields: {
          created: {
            sortable: true,
            label: 'Создана'
          },
          status: {
            sortable: true,
            label: 'Статус'
          },
          message: {
            sortable: true,
            label: 'Сообщение ошибки'
          },
          actions: {
            sortable: false,
            label: 'Действия'
          },
        },
        currentPage: 1
      }

    },
    methods: {
      resetModal () {
        this.$store.dispatch('errors/setModalErrors', [])
      },
      openHistory(error){

      },
      toPending(error){
        this.$store.dispatch('errors/toPending', error)
      },
      closeError(error){
        this.$store.dispatch('errors/closeError', error)
      },
      toError(error){
        this.$store.dispatch('errors/toError', error)
      },
      toWarning(error){
        this.$store.dispatch('errors/toWarning', error)
      },
    }
  }
</script>
