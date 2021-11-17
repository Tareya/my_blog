<template>
    <div id="header">
        <h1> Tareya's Blog </h1>
        <hr>
    </div>


    <div v-for="article in info.results" v-bind:key="article.url" id="articles">

        <div>
            <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
                  {{ tag }}
            </span>
        </div>  

        <div class="article-title">
            {{ article.title }}
        </div>

        <div> {{ formatted_time(article.create_time)}} </div>
    </div>

    <div id="footer">
        <p>tareya.github.io</p>
    </div>

</template>

<script>
    import axios from 'axios';

    export default {
        name: 'App',
        data: function () {
            return {
                info: ''
            }
        },
        mounted() {
            axios
                .get('/api/article')
                .then(response => (this.info = response.data))
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            }
        }
    }
</script>

<style>
    #articles {
        padding: 10px;
    }

    .article-title {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }

    .tag {
        padding: 2px 5px 2px 5px;
        margin: 5px 5px 5px 0;
        font-family: Georgia, Arial, sans-serif;
        font-size: small;
        background-color: #4e4e4e;
        color: whitesmoke;
        border-radius: 5px;
    }

    #app {
        font-family: Georgia, Arial, sans-serif;
        margin-left: 40px;
        margin-right: 40px;
    }

    #header {
        text-align: center;
        margin-top: 20px;
    }

    #footer {
        position: fixed;
        left: 0;
        bottom: 0;
        height: 50px;
        width: 100%;
        background: whitesmoke;
        text-align: center;
        font-weight: bold;
    }
</style>