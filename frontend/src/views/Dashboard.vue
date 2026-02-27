<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isTransactionRunning = ref(false);
const products = ref([]);

let websocket = null;

onMounted(() => {
    websocket = new WebSocket(`${import.meta.env.VITE_BACKEND_URL}/dashboard`);

    websocket.onopen = () => {
        console.log("Connected to Dashboard Websocket ✅");
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WS Data:', data);

        switch (data.type) {
            case 'init':
                products.value = data.products.map(p => ({ ...p, delta: 0 }));
                break;

            case 'start':
                products.value.forEach(p => {
                    if (p.delta > 0) {
                        p.qty -= p.delta;
                        p.delta = 0;
                    }
                });
                isTransactionRunning.value = true;
                break;

            case 'update':
                const product = products.value.find(p => p.id === data.product_id);
                if (product) {
                    product.delta += data.qty;
                }
                break;

            case 'stop':
                isTransactionRunning.value = false;
                break;
        }
    };

    websocket.onclose = () => {
        console.log("Disconnected from Dashboard Websocket ❌");
    };
});

onUnmounted(() => {
    if (websocket) websocket.close();
});
</script>

<template>
    <div class="dashboard-inner">

        <div class="status-bar" :class="{ 'active-bg': isTransactionRunning }">
            <div class="indicator-wrapper">
                <div class="status-dot" :class="isTransactionRunning ? 'online' : 'offline'"></div>
                <i :class="[
                    'bi icon-main',
                    isTransactionRunning ? 'bi-broadcast-pin' : 'bi-pause-circle-fill'
                ]"></i>
            </div>

            <div class="status-text-wrapper">
                <transition name="fade-slide" mode="out-in">
                    <span class="status-title" :key="isTransactionRunning">
                        {{ isTransactionRunning ? 'Transaction Running' : 'System Idle' }}
                    </span>
                </transition>
                <span class="status-sub">
                    {{ isTransactionRunning ? 'Processing speech...' : 'Waiting' }}
                </span>
            </div>
        </div>

        <div class="table-card">
            <div class="table-responsive">
                <table class="modern-table">
                    <thead>
                        <tr>
                            <th class="text-left">Product Name</th>
                            <th class="text-right">Price</th>
                            <th class="text-right">Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="p in products" :key="p.id" :class="{ 'row-active': p.delta > 0 }">
                            <td class="text-left product-name">{{ p.name }}</td>
                            <td class="text-right product-price">₹{{ p.price }}</td>
                            <td class="text-right qty-cell">
                                <span class="base-qty">{{ p.qty }}</span>
                                <transition name="pop">
                                    <span v-if="p.delta > 0" class="delta-tag">
                                        (-{{ p.delta }})
                                    </span>
                                </transition>
                            </td>
                        </tr>
                        <tr v-if="products.length === 0">
                            <td colspan="3" class="empty-state">Loading inventory...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<style scoped>
.dashboard-inner {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

/* --- Compact Status Bar --- */
.status-bar {
    display: flex;
    align-items: center;
    gap: 16px;
    background: white;
    padding: 12px 20px;
    border-radius: 12px;
    border: 1px solid #eee;
    transition: all 0.4s ease;
}

.active-bg {
    border-color: #42b88344;
    box-shadow: 0 4px 20px rgba(66, 184, 131, 0.08);
}

.indicator-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-main {
    font-size: 1.5rem;
    /* Reduced from 2.5rem */
    transition: color 0.3s ease;
    color: #bdc3c7;
}

.active-bg .icon-main {
    color: #42b883;
}

.status-dot {
    position: absolute;
    top: -2px;
    right: -2px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 2px solid white;
    transition: background-color 0.3s ease;
}

.online {
    background-color: #42b883;
    box-shadow: 0 0 8px #42b883;
}

.offline {
    background-color: #e74c3c;
}

.status-text-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.status-title {
    font-weight: 700;
    color: #2c3e50;
    font-size: 0.95rem;
}

.status-sub {
    font-size: 0.75rem;
    color: #95a5a6;
    margin-top: 2px;
}

/* --- Table Styling --- */
.table-card {
    background: white;
    border-radius: 16px;
    border: 1px solid #eee;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

/* Makes table scrollable on small screens */
.table-responsive {
    width: 100%;
    overflow-x: auto;
}

.modern-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 400px;
    /* Ensures it doesn't squish too much on mobile */
}

.modern-table th {
    padding: 16px 20px;
    background: #fafafa;
    color: #a0a0a0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #f0f0f0;
}

.modern-table td {
    padding: 16px 20px;
    border-bottom: 1px solid #f8f8f8;
    vertical-align: middle;
}

.row-active td {
    background-color: #fcfcfc;
}

.text-left {
    text-align: left;
}

.text-right {
    text-align: right;
}

.product-name {
    font-weight: 600;
    color: #2c3e50;
}

.product-price {
    color: #7f8c8d;
    font-variant-numeric: tabular-nums;
}

.qty-cell {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 8px;
}

.base-qty {
    font-weight: 700;
    font-size: 1rem;
    color: #2c3e50;
    font-variant-numeric: tabular-nums;
}

.delta-tag {
    color: #e74c3c;
    /* Red for deduction */
    font-weight: 700;
    font-size: 0.85rem;
    background: #fff0f0;
    padding: 2px 8px;
    border-radius: 6px;
    font-variant-numeric: tabular-nums;
}

.empty-state {
    text-align: center;
    padding: 40px !important;
    color: #95a5a6;
    font-style: italic;
}

/* --- Vue Transitions --- */
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.3s ease;
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateY(5px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-5px);
}

.pop-enter-active {
    animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.pop-leave-active {
    transition: all 0.2s ease;
    opacity: 0;
    transform: scale(0.8);
}

@keyframes pop-in {
    0% {
        transform: scale(0.5);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

/* --- Mobile Responsiveness --- */
@media (max-width: 600px) {

    .modern-table th,
    .modern-table td {
        padding: 12px 16px;
    }

    .status-bar {
        padding: 10px 16px;
    }
}
</style>