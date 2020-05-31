var app = new Vue({
  el: '#app',
  data: {
    streams: [],
    isLoading: true
  },
  methods: {
    isPublishing(stream) {
      return stream.publish_counter > 0
    },
    detailLink(id) {
      return `${id}/`
    },
    deleteLink(id) {
      return `${id}/delete`
    },
    fetchData() {
      axios
        .get('/api/v1/streams/')
        .then(response => {
          this.streams = response.data
          this.isLoading = false
        })
    }
  },
  mounted () {
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
    this.fetchData()
    setInterval(function () {
      this.fetchData();
    }.bind(this), 5000);
  }
})
