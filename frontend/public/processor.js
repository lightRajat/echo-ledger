class AudioSenderProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.targetSampleRate = 16000;
        // Calculate how many frames to skip (e.g., 48000 / 16000 = 3)
        this.ratio = sampleRate / this.targetSampleRate;

        // Batch size for Silero VAD (512 or 1024)
        this.chunkSize = 512;
        this.buffer = new Float32Array(this.chunkSize);
        this.frameCount = 0;
        this.lastSampleIndex = 0;
    }

    process(inputs, outputs, parameters) {
        // inputs[0][0] is the first channel of the microphone input
        const channelData = inputs[0][0];
        if (!channelData) return true;

        // Loop through the 128 incoming frames
        for (let i = 0; i < channelData.length; i++) {
            this.lastSampleIndex++;

            // Only grab a frame when we hit our target ratio
            if (this.lastSampleIndex >= this.ratio) {
                this.buffer[this.frameCount] = channelData[i];
                this.frameCount++;
                this.lastSampleIndex -= this.ratio;

                // Once we have collected 512 frames, send them
                if (this.frameCount >= this.chunkSize) {
                    // .slice(0) creates a safe copy so we don't overwrite data in transit
                    // .buffer extracts the raw ArrayBuffer for the WebSocket
                    this.port.postMessage(this.buffer.slice(0).buffer);
                    this.frameCount = 0;
                }
            }
        }

        return true;
    }
}

registerProcessor('audio-sender', AudioSenderProcessor);