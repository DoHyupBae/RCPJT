<template>
  <div class="chart-container">
    <h1>{{ msg }}</h1>
    <p>소중한 내 차 얼마나 아팠니?</p>
    <VueApexCharts width="800" height="400" type="line" :options="accidentOptions" :series="accidentSeries" />
    <div class="button-group">
      <button class="chart-button" @click="refreshData">데이터 갱신</button>
      <button class="chart-button" @click="showPreviousData">1분 전</button>
      <button class="chart-button" @click="fetchAccidentData">사고 데이터 확인</button>
    </div>
    <VueApexCharts width="800" height="400" type="line" :options="sensorOptions" :series="sensorSeries" />
    <div class="button-group">
      <button class="chart-button" @click="refreshSensorData">센서 데이터 갱신</button>
      <button class="chart-button" @click="showPreviousSensorData">1분 전</button>
      <button class="chart-button" @click="fetchAccidentSensorData">사고 시점 센서 데이터</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import io from "socket.io-client";
import VueApexCharts from "vue3-apexcharts";
import axios from 'axios';
import dayjs from "dayjs";

const times = ref([]);
const isAccident = ref([]);
const pitchValues = ref([]);
const rollValues = ref([]);
const usRangeValues = ref([]);

const accidentOptions = ref({});
const accidentSeries = ref([]);
const sensorOptions = ref({});
const sensorSeries = ref([]);

const props = defineProps({
  msg: String,
});

const socket = io("http://localhost:3000");

const updateAccidentChart = (data) => {
  const length = data.length >= 20 ? 20 : data.length;
  const slicedData = data.slice(0, length).reverse();
  times.value = slicedData.map((x) => dayjs(x.time).format("YYYY-MM-DD HH:mm:ss"));
  isAccident.value = slicedData.map((x) => x.isAccident);
  accidentOptions.value = {
    xaxis: {
      type: 'datetime',
      categories: times.value,
      tickAmount: 20,
      labels: {
        format: 'HH:mm',
        datetimeUTC: false,
        datetimeFormatter: {
          hour: 'HH:mm'
        }
      }
    },
    chart: {
      type: 'line',
      zoom: {
        enabled: true,
        type: 'x',
        autoScaleYaxis: true
      }
    },
    title: {
      text: '사고 추정 시점',
      align: 'left'
    },
    yaxis: {
      title: {
        text: '사고 여부'
      }
    },
    tooltip: {
      x: {
        format: 'dd MMM yyyy HH:mm'
      }
    }
  };
  accidentSeries.value = [
    {
      name: "사고 여부",
      data: isAccident.value,
    },
  ];
};

const updateSensorChart = (data) => {
  const length = data.length >= 20 ? 20 : data.length;
  const slicedData = data.slice(0, length).reverse();
  times.value = slicedData.map((x) => dayjs(x.time).format("YYYY-MM-DD HH:mm:ss"));
  pitchValues.value = slicedData.map((x) => x.pitch_value);
  rollValues.value = slicedData.map((x) => x.roll_value);
  usRangeValues.value = slicedData.map((x) => x.US_range_value);
  sensorOptions.value = {
    xaxis: {
      type: 'datetime',
      categories: times.value,
      tickAmount: 20,
      labels: {
        format: 'HH:mm',
        datetimeUTC: false,
        datetimeFormatter: {
          hour: 'HH:mm'
        }
      }
    },
    chart: {
      type: 'line',
      zoom: {
        enabled: true,
        type: 'x',
        autoScaleYaxis: true
      }
    },
    title: {
      text: '피치, 롤, 초음파센서 전방 거리 데이터',
      align: 'left'
    },
    yaxis: {
      title: {
        text: '센서 값'
      }
    },
    tooltip: {
      x: {
        format: 'dd MMM yyyy HH:mm'
      }
    },
    legend: {
      show: true,
      position: 'top',
      horizontalAlign: 'right'
    }
  };
  sensorSeries.value = [
    {
      name: "피치 값",
      data: pitchValues.value,
    },
    {
      name: "롤 값",
      data: rollValues.value,
    },
    {
      name: "초음파 센서 값",
      data: usRangeValues.value,
    }
  ];
};

const refreshData = async () => {
  try {
    const response = await axios.get('http://localhost:3000/chart-data');
    updateAccidentChart(response.data);
    updateSensorChart(response.data);
  } catch (error) {
    console.error('Error refreshing data:', error);
  }
};

const fetchAccidentData = async () => {
  try {
    const response = await axios.get('http://localhost:3000/accident-data');
    updateAccidentChart(response.data);
  } catch (error) {
    console.error('Error fetching accident data:', error);
  }
};

const fetchAccidentSensorData = async () => {
  try {
    const response = await axios.get('http://localhost:3000/accident-data');
    updateSensorChart(response.data);
  } catch (error) {
    console.error('Error fetching accident sensor data:', error);
  }
};

const showPreviousData = () => {
  const newTimes = times.value.map(time => dayjs(time).subtract(1, 'minute').format("YYYY-MM-DD HH:mm:ss"));
  updateAccidentChart(newTimes.map((time, index) => ({ time, isAccident: isAccident.value[index] })));
};

const showPreviousSensorData = () => {
  const newTimes = times.value.map(time => dayjs(time).subtract(1, 'minute').format("YYYY-MM-DD HH:mm:ss"));
  updateSensorChart(newTimes.map((time, index) => ({
    time,
    pitch_value: pitchValues.value[index],
    roll_value: rollValues.value[index],
    US_range_value: usRangeValues.value[index]
  })));
};

// Initialize the chart with the latest data
refreshData();
</script>

<style scoped>
.chart-container {
  width: 80%;
  margin: 20px auto;
  text-align: center;
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1 {
  color: #007bff;
}
p {
  color: #555;
}
.button-group {
  margin-top: 20px;
}
.chart-button {
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.chart-button:hover {
  background-color: #0056b3;
}
</style>
