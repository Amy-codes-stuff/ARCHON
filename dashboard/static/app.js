const zones = {
    ZONE_A: {
        temperature: document.querySelector("#zone-a-temperature"),
        humidity: document.querySelector("#zone-a-humidity"),
        soil: document.querySelector("#zone-a-soil")
    },
    ZONE_B: {
        temperature: document.querySelector("#zone-b-temperature"),
        humidity: document.querySelector("#zone-b-humidity"),
        soil: document.querySelector("#zone-b-soil")
    },
    ZONE_C: {
        temperature: document.querySelector("#zone-c-temperature"),
        humidity: document.querySelector("#zone-c-humidity"),
        soil: document.querySelector("#zone-c-soil")
    }
};


function connectSensorStream() {

    const socket = new WebSocket(
    "wss://jubilant-goggles-x59759w766543v7pr-8000.app.github.dev"
);

    socket.onopen = function () {
        console.log("[ARCHON] Connected to sensor stream");
    };

    socket.onmessage = function (event) {

        const data = JSON.parse(event.data);

        console.log("[SENSOR DATA]", data);

        const zone = zones[data.zone];

        if (!zone) {
            return;
        }

        zone.temperature.textContent =
            `${data.temperature.toFixed(1)} °C`;

        zone.humidity.textContent =
            `${data.humidity.toFixed(1)} %`;

        zone.soil.textContent =
            `${data.soil_moisture.toFixed(1)} %`;
    };

    socket.onclose = function () {
        console.log("[ARCHON] Sensor stream disconnected");

        setTimeout(connectSensorStream, 3000);
    };

    socket.onerror = function (error) {
        console.error("[ARCHON] WebSocket error:", error);
    };
}


connectSensorStream();