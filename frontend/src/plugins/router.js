import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../components/Main'
import Report from '../components/Report'

const routes = [
    { path: '/', component: Main },
    { path: '/report/:ids', component: Report } 
  ]

  const router = new VueRouter({
    routes,
    mode: "history",
  })

  Vue.use(VueRouter)

  export default router