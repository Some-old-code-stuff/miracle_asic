<template>
  <div class="col">
    <h4>Для того, чтобы получить доступ к настройкам, необходимо пройти 2FA авторизацию</h4>
    <div v-if="tryCount != null">
      <span>Остал{{tryCount == 2 ? 'ось' : 'ась'}} {{tryCount}} попытк{{tryCount == 2 ? 'и' : 'а'}}!</span>
    </div>
    <div v-if="!isSendSmsToken">
      <b-form-input :value="phone" type="text" placeholder="Введите Ваш телефон" @input="updatePhone"
                    @keyup.enter="sendSmsToken"
      ></b-form-input>
      <b-btn variant="primary" @click="sendSmsToken">Отправить sms токен</b-btn>
    </div>
    <div v-else>
      <b-form-input :value="smsToken" @input="updateSmsToken" type="text"
                    placeholder="Введите токен"></b-form-input>
      <b-btn variant="primary" @click="login()">Авторизоваться</b-btn>
      <b-btn variant="primary" @click="sendSmsToken">Отправить sms токен еще раз</b-btn>
      <b-btn variant="primary" @click="showPhone()">Ввести другой номер телефона</b-btn>
    </div>
  </div>
</template>

<script>
  import {mapState, mapActions} from 'vuex'
  export default{
    name: 'SmsTokenAuth',
    computed: {
      ...mapState('auth', [
        'smsToken',
        'isSendSmsToken',
        'phone',
        'token',
        'tryCount'
      ]),
    },
    props:{
      action:String,
      params:Object
    },
    methods:{
      ...mapActions('auth', [
        'sendSmsToken',
        'showPhone',
        'updatePhone',
        'updateSmsToken',
      ]),
      sendSmsToken(e){
        this.$store.dispatch('auth/sendSmsToken')
      },
      login(){
        this.$store.dispatch('auth/checkSmsToken', {actionName:this.action, params:this.params})
      },
    }
  }
</script>
