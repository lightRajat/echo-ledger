<script setup>
import { ref } from 'vue';

const isTransactionRunning = ref(false);
const totalTransactions = ref(0);

// websocket
const websocket = new WebSocket(`${import.meta.env.VITE_BACKEND_URL}/dashboard`);
websocket.onopen = (event) => {
    console.log("Connected to Dashboard Websocket ✅");
};
websocket.onmessage = (event) => {
    const message = event.data;

    if (message === "start ts") {
        isTransactionRunning.value = true;
    } else if (message === "end ts") {
        isTransactionRunning.value = false;
        totalTransactions.value += 1;
    }
};
websocket.onclose = (event) => {
    console.log("Disconnected from Dashboard Websocket ❌");
};
</script>

<template>
    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-label">Total Transactions</span>
            <h2 class="stat-value">{{ totalTransactions }}</h2>
        </div>
    </div>

    <div class="status-card" :class="{ 'active-bg': isTransactionRunning }">
        <div class="status-header">
            <div class="indicator-wrapper">
                <div class="status-dot" :class="isTransactionRunning ? 'online' : 'offline'"></div>
                <i :class="[
                    'bi icon-main',
                    isTransactionRunning ? 'bi-broadcast-pin' : 'bi-pause-circle-fill'
                ]"></i>
            </div>

            <div class="status-text">
                <transition name="fade-slide" mode="out-in">
                    <h3 :key="isTransactionRunning">
                        {{ isTransactionRunning ? 'Transaction Running' : 'System Idle' }}
                    </h3>
                </transition>
                <p>{{ isTransactionRunning ? 'AI is processing speech...' : 'Waiting for connection' }}</p>
            </div>
        </div>

        <button @click="isTransactionRunning = !isTransactionRunning" class="test-btn">
            Toggle Simulation
        </button>
    </div>
</template>

<style scoped>
.stats-grid {
    display: grid;
    grid-template-columns: 1fr;
    margin-bottom: 1.5rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    text-align: left;
    border: 1px solid #eee;
}

.stat-label {
    color: #7f8c8d;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stat-value {
    margin: 5px 0 0;
    font-size: 2rem;
    font-weight: 800;
    color: #2c3e50;
}

/* Status Card Styling */
.status-card {
    background: white;
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid #eee;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.active-bg {
    border-color: #42b88333;
    box-shadow: 0 10px 30px rgba(66, 184, 131, 0.1);
}

.status-header {
    display: flex;
    align-items: center;
    gap: 20px;
}

.indicator-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-main {
    font-size: 2.5rem;
    transition: color 0.3s ease;
    color: #bdc3c7;
}

.active-bg .icon-main {
    color: #42b883;
}

/* The Status Dot & Pulsing */
.status-dot {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid white;
    transition: background-color 0.3s ease;
}

.online {
    background-color: #42b883;
    box-shadow: 0 0 10px #42b883;
}

.offline {
    background-color: #e74c3c;
}

/* Text & Animations */
.status-text {
    text-align: left;
}

.status-text h3 {
    margin: 0;
    font-weight: 700;
    color: #2c3e50;
}

.status-text p {
    margin: 4px 0 0;
    font-size: 0.9rem;
    color: #95a5a6;
}

/* Vue Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.3s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateY(10px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

/* Helper Button for Testing */
.test-btn {
    margin-top: 20px;
    background: transparent;
    border: 1px solid #ddd;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.7rem;
    color: #999;
}
</style>