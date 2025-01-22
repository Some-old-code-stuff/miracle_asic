<template>
  <b-modal ref="modal" @hide="resetModal" :title="'Настройки ' + modalAsic.asicName" ok-only>
    <div class="row">
      <div class="col" v-if="showSettingsForm">
        <h5>Текущее имя пользователя: <span>{{settingsForm.currentUsername}}</span></h5>
        <h5>Текущий пароль: <span>{{settingsForm.currentPassword}}</span></h5>
        <div class="form-group" v-if="false">
          <label class="control-label" for="id_username">Имя пользователя</label>
          <input type="text" name="username" maxlength="15" class="form-control" placeholder="Имя пользователя ASIC"
                 title=""
                 id="id_username" v-model="settingsForm.username">
        </div>
        <div class="form-group">
          <label class="control-label" for="id_password">Пароль</label>
          <input type="text" name="password" minlength="4" maxlength="15" class="form-control" placeholder="Пароль ASIC"
                 title=""
                 id="id_password" v-model="settingsForm.password">
        </div>
        <div class="form-group">
          <b-btn variant="primary" @click.stop="changePassword()">Изменить логин\пароль</b-btn>
        </div>
      </div>
      <sms-token-auth action="asicSettings/showSettingsForm"v-else></sms-token-auth>
    </div>
  </b-modal>
</template>

<script>
  import {mapState, mapActions} from 'vuex'
  import SmsTokenAuth from './SmsTokenAuth'
  export default{
    name: 'SettingsModal',
    components:{
        SmsTokenAuth
    },
    computed: {
      ...mapState('asics', [
        'modalAsic'
      ]),
      ...mapState('asicSettings', [
        'showSettingsForm',
        'settingsForm'
      ])
    },
    methods: {
      ...mapActions('asicSettings', [
        'changePassword',
        'hideSettingsForm',
      ]),
      resetModal(){
        this.hideSettingsForm()
      }
    }
  }
</script>
