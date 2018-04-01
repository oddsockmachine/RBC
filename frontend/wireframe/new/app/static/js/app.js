Vue.options.delimiters = ['<<', '>>']
Vue.component('one-list', {
    props: ['item'],
    template: '#template-one'
});

var app_zero = new Vue({
    el: '#app-zero',
    data: {
        ts: {}
    },
    delimiters: ["<<",">>"],
    methods: {
        fetchData: function () {
            this.$http.get('/api/ts')
                .then(function (response) {
                    this.ts = response.data.now;
                }, function (err) {
                    console.log(err);
                });
        }
    },
    mounted: function () {
        setInterval(this.fetchData,
        3000);
    }
});

var app_one = new Vue({
    el: '#app-one',
    data: {
        one_list: []
    },
    delimiters: ["<<",">>"],
    methods: {
        fetchData: function () {
            this.$http.get('/api/one')
                .then(function (response) {
                    this.one_list = response.data.one;
                }, function (err) {
                    console.log(err);
                });
        }
    },
    mounted: function () {
        this.fetchData();
    }
});

var app_two = new Vue({
    el: '#app-two',
    data: {
        two_list: []
    },
    delimiters: ["<<",">>"],
    methods: {
        fetchData: function () {
            this.$http.get('/api/two')
                .then(function (response) {
                    this.two_list = response.data.two;
                }, function (err) {
                    console.log(err);
                });
        }
    },
    mounted: function () {
        this.fetchData();
    }
});



Vue.component('todo-item', {
  props: ['todo'],
  template: '<li><< todo.text >> << Date.now() - todo.time >></li>'
})
var app7 = new Vue({
  el: '#app-7',
  data: {
    newTodo: 'Hello Vue!',
    groceryList: [
      { id: 0, text: 'Temp', time: 1 },
    ]
  },
  mounted: function () {
    console.log(this);
    this.$http.get('/api/all')
        .then(function (response) {
            console.log(response.data);
            this.groceryList = response.data
        }, function (err) {
            console.log(err);
        });
  },
  delimiters: ["<<",">>"],
  methods: {
    addTodo: function () {
      console.log(this.groceryList.length);
      var newID = this.groceryList.length;
      this.groceryList.push({ id: newID, text: this.newTodo, time: Date.now() });
      this.pushTodo(this.newTodo, newID);
    },
    pushTodo: function (newTodo, new_ID) {
        this.$http.post('/api/add', {'newTodo': newTodo, 'id': new_ID})
            .then(function (response) {
                console.log(response.data);
            }, function (err) {
                console.log(err);
            });
    }
  }
})
