<template>
  <Layout>
    <div class="row justify-content-center">
      <div class="col-2" v-if="!isSendSmsToken">
        <b-form-input :value="phone" type="text" placeholder="Введите Ваш телефон" @input="updatePhone"
                      @keyup.enter="sendSmsToken"
        ></b-form-input>
        <b-btn variant="primary" @click="sendSmsToken">Отправить sms токен</b-btn>
      </div>
      <div class="col-2" v-if="isSendSmsToken">
        <b-form-input :value="smsToken" @input="updateSmsToken" type="text" placeholder="Введите токен"></b-form-input>
        <b-btn variant="primary" @click="login()">Авторизоваться</b-btn>
        <b-btn variant="primary" @click="sendSmsToken">Отправить sms токен еще раз</b-btn>
        <b-btn variant="primary" @click="showPhone()">Ввести другой номер телефона</b-btn>
      </div>
    </div>
  </Layout>
</template>

<script>
  import Layout from '../layouts/main'
  import {mapState, mapActions} from 'vuex'
  export default{
    name: 'LoginView',
    components: {
      Layout
    },
    computed: {
      ...mapState('auth', [
        'smsToken',
        'isSendSmsToken',
        'phone',
        'token'
      ])
    },
    methods: {
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
          this.$store.dispatch('auth/login').then(()=>{
            this.$store.dispatch('utils/init')
            this.$store.dispatch('asics/init')
            this.$router.push(this.$route.query.redirectFrom || { name: 'home' })
          })
      }
    }
  }
</script>
