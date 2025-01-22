<template>
  <Layout>
    {{warnings}}
  </Layout>
</template>

<script>
  import Layout from '../layouts/main'
  export default{
    name: 'ErrorView',
    components: {
      Layout
    },
    props: {
      warnings: {
        type: Boolean,
        default: false
      }
    }

  }
</script>
