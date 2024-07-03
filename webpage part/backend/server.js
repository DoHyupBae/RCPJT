const express = require('express');
const app = express();
const port = 3000;
const cors = require("cors");
const pool = require("./db");
const axios = require('axios');
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server, {
  cors: {
    origin: true
  },
  pingInterval: 100,
  pingTimeout: 1
});

const OPENAI_API_KEY = 'openai-api-key'; 
app.use(
  cors({
    origin: true
  })
);

app.use(express.json());

app.get('/chart-data', async (req, res) => {
  try {
    const [rows] = await pool.query("SELECT time, isAccident, pitch_value, roll_value, US_range_value FROM sensing ORDER BY time DESC LIMIT 20");
    res.json(rows);
  } catch (error) {
    console.error('Error fetching chart data:', error);
    res.status(500).json({ error: 'Failed to fetch chart data' });
  }
});

app.get('/accident-data', async (req, res) => {
  try {
    const [rows] = await pool.query("SELECT time, isAccident, pitch_value, roll_value, US_range_value FROM sensing WHERE isAccident IN (1, 2) ORDER BY time DESC LIMIT 20");
    res.json(rows);
  } catch (error) {
    console.error('Error fetching accident data:', error);
    res.status(500).json({ error: 'Failed to fetch accident data' });
  }
});

app.post('/generate-analysis', async (req, res) => {
  const query = "SELECT time, isAccident FROM sensing WHERE time >= NOW() - INTERVAL 1 DAY";
  try {
    const [rows] = await pool.query(query);
    const accidentData = rows.filter(row => row.isAccident === 1 || row.isAccident === 2);
    const significantAccidents = [];
    
    let count = 0;
    for (let i = 0; i < accidentData.length; i++) {
      if (i > 0 && (new Date(accidentData[i].time) - new Date(accidentData[i - 1].time)) <= 60000) { // 60 초 간격
      } else {
        if (count >= 2) { // 사고 발생 기준
          significantAccidents.push(accidentData[i - 1]);
        }
        count = 1;
      }
    }
// 이하 gpt가 분석 할 질문 내용
    const accidentTimes = significantAccidents.map(accident => `시간: ${accident.time}, 사고 여부: ${accident.isAccident}`).join('\n');
    let prompt;
    if (accidentTimes) {
      prompt = `다음 데이터는 가능한 사고를 나타냅니다:\n${accidentTimes}\n이 시간들이 실제 사고를 나타내는지 센서 문제인지 식별해 주세요. 답변은 한국어로 해 주세요.`;
    } else {
      prompt = `지난 24시간 동안은 isAccident 데이터가 대부분 0으로 유지되어 사고가 감지되지 않았습니다. 답변은 한국어로 해 주세요.`;
    }

    console.log("Generated prompt:", prompt);

    const response = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 150
    }, {
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    console.log("OpenAI API response:", response.data);

    res.json({ analysis: response.data.choices[0].message.content.trim() });
  } catch (error) {
    console.error('Error generating analysis:', error.response ? error.response.data : error.message);
    res.status(500).json({ error: 'Failed to generate analysis', details: error.message });
  }
});

io.on("connection", async (socket) => {
  try {
    const [rows] = await pool.query("SELECT time, isAccident, pitch_value, roll_value, US_range_value FROM sensing ORDER BY time DESC LIMIT 20");
    socket.emit("kfc", rows);
  } catch (error) {
    console.error('Error fetching socket data:', error);
  }

  socket.on("bbq", (arg) => {
    console.log(arg);
  });
});

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
