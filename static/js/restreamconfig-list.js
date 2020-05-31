var app = new Vue({
  el: '#app',
  data: {
    cfgs: [],
    isLoading: true
  },
  methods: {
    detailLink(id) {
      return `${id}/`
    },
    deleteLink(id) {
      return `${id}/delete`
    },
    toggleActive(cfg) {
      axios
        .patch('/api/v1/restreamconfigs/' + cfg.id + '/', { active: !cfg.active })
        .then(response => {
            i = this.cfgs.findIndex((obj => obj.id == cfg.id))
            Vue.set(this.cfgs, i, response.data)
          }
        )
    },
    fetchData() {
      axios
        .get('/api/v1/restreamconfigs/')
        .then(response => {
          this.cfgs = response.data
          this.isLoading = false
        })
    }
  },
  mounted () {
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
    this.fetchData()
  }
})
