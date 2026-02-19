<script setup>
import { RouterLink, useRoute } from 'vue-router';

const route = useRoute();

const maxWidth = '940px';
const navLinks = [
    { link: '/', name: 'Home' },
    { link: '/recorder', name: 'Recorder' },
    { link: '/dashboard', name: 'Dashboard' },
];
</script>

<template>
    <div class="nav-container">
        <nav :style="`max-width: ${maxWidth}`" class="d-flex justify-content-center mx-auto lead">
            <RouterLink v-for="(link, index) in navLinks" :key="index" :to="link.link" class="nav-link p-2" :class="route.path == link.link ? 'fw-medium' : ''">
                <i v-if="index === 0" class="bi bi-house"></i>
                {{ link.name }}
            </RouterLink>
        </nav>
    </div>
</template>

<style scoped>
.nav-container {
    width: 100%;
}
</style>