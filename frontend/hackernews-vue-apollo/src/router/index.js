import Vue from 'vue'
import Router from 'vue-router'

import CreateLink from '../components/CreateLink'
import LinkList from '../components/LinkList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: LinkList
    },
    {
      path: '/create',
      component: CreateLink
    }
  ],
  // 3
  mode: 'history'
})
