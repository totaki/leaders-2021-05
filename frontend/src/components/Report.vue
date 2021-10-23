<template>
    <div>
        <h2>Hello World</h2>
    </div>
</template>
<script>
export default {
    computed: {
        hexReport(){
            return this.$store.getters.hexReport
        }
    },
    mounted() {
        this.$store.dispatch("getHexReport", {isBig: this.$route.params.isBig, ids: {ids: JSON.parse(this.$route.params.ids)}})
    },
}
</script>
<style>
    
</style>