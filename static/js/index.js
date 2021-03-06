RF_GAINS = [
  "0",
  "0.9",
  "1.4",
  "2.7",
  "3.7",
  "7.7",
  "8.7",
  "12.5",
  "14.4",
  "15.7",
  "16.6",
  "19.7",
  "20.7",
  "22.9",
  "25.4",
  "28.0",
  "29.7",
  "32.8",
  "33.8",
  "36.4",
  "37.2",
  "38.6",
  "40.2",
  "42.1",
  "43.4",
  "43.9",
  "44.5",
  "48.0",
  "49.6",
];

function defaultForm() {
  return {
    antenna_altitude_m: "",
    antenna_azimuth_deg: "",
    antenna_latitude: "",
    antenna_longitude: "",
    khz: "14313",
    notes: "",
    rx_antenna: "isotropic",
    scan: "azimuth",
    title: "Airbud",
    rf_gain: "0.0",
  };
}

const vue = new Vue({
  el: "#app",

  data: {
    connected: false,
    form: defaultForm(),
    timestamp: 0,
    starting: false,
    stopping: false,
    status: {
      conditions: {
        antenna_altitude_m: 0.0,
        antenna_azimuth_deg: 0,
        antenna_latitude: 0.0,
        antenna_longitude: 0.0,
        khz: 14313,
        notes: "",
        rx_antenna: "isotropic",
        scan: "azimuth",
        started_at: null,
        title: "Airbud",
        rf_gain: 0.0,
      },
      gps: {
        altitude_m: 0.0,
        course: 0.0,
        latitude: 0.0,
        longitude: 0.0,
        satellites_in_use: 0,
        speed_kmhr: 0.0,
        valid: false,
        look_az: 0,
        look_el: 0,
        look_range: 0,
      },
      rf: {
        dbfs: 0.0,
        khz: 14313,
      },
    },
  },

  methods: {
    async fetchStatus() {
      const abort = new AbortController();

      try {
        const timeout = setTimeout(() => {
          abort.abort();
          this.connected = false;
        }, 500);

        const response = await fetch("/api/status", { signal: abort.signal });
        clearTimeout(timeout);

        this.status = await response.json();
        this.timestamp = Date.now();

        if (!this.connected) {
          this.postConditions();
          this.connected = true;
        }
      } catch {
        this.connected = false;
      }
    },

    copyAntennaHeight() {
      this.form.antenna_altitude_m = this.status.gps.altitude_m;
      this.postConditions();
    },

    copyAntennaCoordinate() {
      this.form.antenna_latitude = this.status.gps.latitude;
      this.form.antenna_longitude = this.status.gps.longitude;
      this.postConditions();
    },

    resetForm() {
      this.form = defaultForm();
      this.postConditions();
    },

    async postConditions() {
      const conditions = {
        antenna_altitude_m: parseFloat(this.form.antenna_altitude_m),
        antenna_azimuth_deg: parseFloat(this.form.antenna_azimuth_deg),
        antenna_latitude: parseFloat(this.form.antenna_latitude),
        antenna_longitude: parseFloat(this.form.antenna_longitude),
        khz: parseInt(this.form.khz),
        notes: this.form.notes,
        rx_antenna: this.form.rx_antenna,
        scan: this.form.scan,
        title: this.form.title,
        rf_gain: parseFloat(this.form.rf_gain),
      };

      const response = await fetch("/api/conditions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(conditions),
      });
    },

    async startAcquisition() {
      this.starting = true;

      this.postConditions();

      const response = await fetch("/api/start", { method: "POST" });
      this.status = await response.json();
      this.starting = false;
    },

    async stopAcquisition() {
      this.stopping = true;

      const response = await fetch("/api/stop", { method: "POST" });
      this.status = await response.json();
      this.stopping = false;
    },
  },

  mounted() {
    setInterval(() => this.fetchStatus(), 1000);

    const form = localStorage.getItem("airbud-form");
    if (form) {
      this.form = JSON.parse(form);
    }
  },

  computed: {
    connectedColor() {
      return this.connected ? "green-500" : "red-500";
    },
    connectedBgColor() {
      return `bg-${this.connectedColor}`;
    },
    connectedTextColor() {
      return `text-${this.connectedColor}`;
    },
    connectedText() {
      return this.connected ? "Connected" : "Disconnected";
    },
    psdImageUrl() {
      return `/images/psd.png?${this.timestamp}`;
    },
    dbfsText() {
      if (this.status.rf.dbfs) {
        return `${this.status.rf.dbfs.toFixed(2)} dBFS`;
      } else {
        return null;
      }
    },
    started() {
      return !!this.status.conditions.started_at;
    },
    satelliteCountText() {
      if (this.status.gps.satellites_in_use) {
        return `${this.status.gps.satellites_in_use} satellites`;
      } else {
        return "No satellites";
      }
    },
    rangeInWavelengths() {
      const wavelengthMeters = 300000 / this.status.conditions.khz;
      return this.status.gps.look_range / wavelengthMeters;
    },
    rangeColor() {
      if (this.rangeInWavelengths < 5) {
        return "text-red-500";
      } else {
        return "text-green-500";
      }
    },
  },

  watch: {
    form: {
      deep: true,
      handler() {
        localStorage.setItem("airbud-form", JSON.stringify(this.form));
      },
    },
  },
});
