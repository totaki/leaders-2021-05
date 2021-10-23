<template>
    <div>
        <h2>Hello World</h2>
    </div>
</template>
<script>
export default {
    mounted() {
        console.log(JSON.parse(this.$route.params.ids))
    },
}
</script>
<style>
    
</style>