<template>
  <div id="app">
    <Chart msg="자동차 사고 이력 조회 및 분석" />
    <hr class="divider"/>
    <AnalysisComponent />
  </div>
</template>

<script setup>
import Chart from "@/components/Chart.vue";
import AnalysisComponent from "@/components/AnalysisComponent.vue";
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.divider {
  margin: 40px 0;
  border: 0;
  border-top: 1px solid #e0e0e0;
}
</style>
