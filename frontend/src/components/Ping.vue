<template>
    <div class="container">
        <button type="button" class="btn btn-primary">{{msg}}</button>
    </div>
</template>

<script>
 import axios from 'axios';

 export default {
     name: 'Ping',
     data() {
         return {
             msg: '',
         };
     },
     methods: {
         getMessage() {
             const path = 'https://terzeron.com/flask/healthcheck';
             axios.get(path)
                  .then((res) => {
                      this.msg = res.data;
                  })
                  .catch((error) => {
                      console.error(error);
                  });
         },
     },
     created() {
         this.getMessage();
     }
 };
</script>
