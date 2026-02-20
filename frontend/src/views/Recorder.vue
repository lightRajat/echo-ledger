<script setup>
import { ref } from 'vue';

const isRecording = ref(false);
let stream, audioCtx, source, audioWorkletNode, socket;

const toggleRecording = async () => {
    // one time permissions
    if (!stream) {
        if (!window.isSecureContext) {
            alert("Browser is blocking mic access because this connection is not HTTPS or localhost.");
            return;
        }

        try {
            stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    channelCount: { ideal: 1 },
                    sampleSize: { ideal: 16 },
                    echoCancellation: { ideal: true },
                    noiseSuppression: { ideal: true },
                    autoGainControl: { ideal: false },
                },
            });

            // init audio context
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
            await audioCtx.audioWorklet.addModule('/processor.js');
            if (audioCtx.state === 'suspended') {
                await audioCtx.resume();
            }

            // init web socket
            socket = new WebSocket(import.meta.env.VITE_BACKEND_URL);
            socket.binaryType = "arraybuffer";
        } catch (error) {
            console.error("Permission denied or microphone not found:", error);
            return;
        }
    }

    // toggle recording
    if (!isRecording.value) {
        audioWorkletNode = new AudioWorkletNode(audioCtx, 'audio-sender');

        source = audioCtx.createMediaStreamSource(stream);
        source.connect(audioWorkletNode);

        audioWorkletNode.port.onmessage = (event) => {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(event.data);
            }
        };

        console.log("Started recording");
    } else {
        if (source) source.disconnect();
        if (audioWorkletNode) {
            audioWorkletNode.disconnect();
            audioWorkletNode.port.onmessage = null;
        }

        console.log("Stopped recording");
    }

    isRecording.value = !isRecording.value;
};
</script>

<template>
    <div class="recorder-card">
        <div class="status-indicator" :class="{ 'is-active': isRecording }">
            {{ isRecording ? 'Streaming Audio...' : 'Ready to Scan' }}
        </div>

        <button @click="toggleRecording" class="mic-button" :class="{ 'recording': isRecording }">
            <div class="pulse-ring" v-if="isRecording"></div>
            <i :class="isRecording ? 'bi bi-stop-fill' : 'bi bi-mic-fill'"></i>
        </button>

        <h2 class="recording-label">
            {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
        </h2>

        <p class="helper-text">
            {{ isRecording
                ? 'The AI is listening to your inventory updates.'
                : 'Tap the mic to begin voice-based checkout.'
            }}
        </p>
    </div>
</template>

<style scoped>
.recorder-card {
    background: white;
    padding: 3rem 2rem;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    max-width: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: all 0.3s ease;
    margin: 0 auto;
}

/* Status Pill */
.status-indicator {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 6px 16px;
    border-radius: 20px;
    background: #f0f0f0;
    color: #a0a0a0;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.status-indicator.is-active {
    background: #ffeeee;
    color: #ff4757;
}

/* The Big Mic Button */
.mic-button {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: none;
    background: #42b883;
    /* Vue Green */
    color: white;
    font-size: 2.5rem;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 2;
    margin-bottom: 1.5rem;
}

.mic-button.recording {
    background: #ff4757;
    /* Danger Red */
    transform: scale(1.1);
}

.mic-button:active {
    transform: scale(0.9);
}

/* Pulsing Animation */
.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: #ff4757;
    opacity: 0.6;
    z-index: -1;
    animation: pulse-animation 2s;
}

@keyframes pulse-animation {
    0% {
        transform: scale(1);
        opacity: 0.6;
    }

    100% {
        transform: scale(2.5);
        opacity: 0;
    }
}

.recording-label {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #2c3e50;
}

.helper-text {
    color: #95a5a6;
    font-size: 0.9rem;
    max-width: 250px;
    line-height: 1.4;
}
</style>
