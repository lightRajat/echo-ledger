<template>
    <header class="home-header">
        <h1>Echo Ledger</h1>
        <p>Real-time AI Inventory Assistant</p>
    </header>

    <div class="card-grid">
        <RouterLink to="/recorder" class="nav-card">
            <div class="icon-box">
                <i class="bi bi-mic-fill"></i>
            </div>
            <div class="card-content">
                <h3>Audio Recorder</h3>
                <p>Stream real-time audio from your device to the AI engine for processing.</p>
            </div>
        </RouterLink>

        <RouterLink to="/dashboard" class="nav-card">
            <div class="icon-box">
                <i class="bi bi-speedometer2"></i>
            </div>
            <div class="card-content">
                <h3>Live Dashboard</h3>
                <p>Monitor database changes in real-time with side-by-side state comparisons.</p>
            </div>
        </RouterLink>
    </div>
</template>

<style scoped>
.home-header {
    margin-bottom: 50px;
}

.home-header h1 {
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 10px;
}

.home-header p {
    color: #7f8c8d;
}

/* Card Grid Layout */
.card-grid {
    display: flex;
    gap: 20px;
}

/* Navigation Card Styles */
.nav-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
    background: #ffffff;
    border-radius: 16px;
    text-decoration: none;
    color: inherit;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid #e0e0e0;
}

.nav-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.icon-box {
    font-size: 3rem;
    color: #42b883;
    /* Vue Green */
    margin-bottom: 20px;
}

.card-content h3 {
    margin-bottom: 12px;
    font-weight: 600;
}

.card-content p {
    font-size: 0.95rem;
    line-height: 1.5;
    color: #636e72;
}

/* Mobile Responsive: Stack Vertically */
@media (max-width: 600px) {
    .card-grid {
        flex-direction: column;
    }

    .home-header {
        margin-bottom: 30px;
    }
}
</style>