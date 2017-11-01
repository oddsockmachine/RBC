// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import { ApolloClient, createNetworkInterface } from 'apollo-client'
import 'tachyons'

import Vue from 'vue'
import VueApollo from 'vue-apollo'

import App from './App'

Vue.config.productionTip = false

const networkInterface = createNetworkInterface({
  uri: 'http://localhost:5000/graphql'
})

const apolloClient = new ApolloClient({
  networkInterface,
  connectToDevTools: true,
  transportBatching: false
})

Vue.use(VueApollo)

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
  defaultOptions: {
    $loadingKey: 'loading'
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  apolloProvider,
  render: h => h(App)
})
