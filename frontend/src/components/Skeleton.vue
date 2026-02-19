<script setup>
import { RouterView } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
</script>

<template>
    <Navbar />
    <div class="home-container">
        <div class="content-wrapper">
            <RouterView />
        </div>
    </div>
</template>

<style scoped>
.home-container {
    display: flex;
    justify-content: center;
    padding: 40px 20px;
    min-height: 100vh;
    background-color: #f8f9fa;
}

.content-wrapper {
    width: 100%;
    max-width: 800px;
    text-align: center;
}
</style>