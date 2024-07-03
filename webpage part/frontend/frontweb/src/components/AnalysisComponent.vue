<template>
    <div id="analysis">
      <h2>사고민수야 도와줘~!</h2>
      <div class="analysis-container">
        <button class="analysis-button" @click="generateAnalysis">1일간 사고 이력 분석</button>
        <div v-if="analysis" class="analysis-result-box">
          <p>{{ analysis }}</p>
        </div>
        <p v-if="error" class="error-message">{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AnalysisComponent',
    data() {
      return {
        analysis: '',
        error: ''
      };
    },
    methods: {
      async generateAnalysis() {
        this.analysis = '';
        this.error = '';
        try {
          const response = await axios.post('http://localhost:3000/generate-analysis', {});
          this.analysis = response.data.analysis;
        } catch (error) {
          this.error = 'Error generating analysis: ' + (error.response ? error.response.data.error : error.message);
          console.error('Error generating analysis:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  #analysis {
    width: 80%;
    margin: 20px auto;
    padding: 20px;
    background-color: #f2f2f2;
    border-radius: 8px;
  }
  .analysis-container {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
  }
  .analysis-button {
    display: inline-block;
    margin-right: 20px;
    padding: 10px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .analysis-button:hover {
    background-color: #218838;
  }
  .analysis-result-box {
    flex-grow: 1;
    border: 1px solid #ccc;
    padding: 10px;
    margin-top: 20px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
  }
  .error-message {
    color: red;
    margin-top: 20px;
  }
  </style>
  